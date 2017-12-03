"""
Получение профилей пользователей.

Для получения всех профилей пользователей необходим ключ доступа (access token) ВКонтакте.
Используются 64 процесса, при этом достаточно 16 ключей доступа (один ключ доступа на каждые 4 процесса).

В переменной access_tokens_path указывается путь к файлу со списком ключей доступа.
"""


import pymysql
import vk
import re
import time
from datetime import date, datetime, timedelta
from vk.exceptions import VkAPIError
from requests.exceptions import Timeout, ConnectionError, ChunkedEncodingError, HTTPError
from multiprocessing import Pool, Manager, Value, current_process
from multiprocessing.util import Finalize
from modules.count_users import count_users


def get_access_tokens(path):
    with open(path) as f:
        tokens = [token.strip() for token in f if token.strip()]

    return tokens


conn = None
api = None

countries = None
cities = None
count = None

def pool_init(access_tokens, shared_countries, shared_cities, shared_count):
    global conn
    global api
    global countries
    global cities
    global count

    conn = pymysql.connect(host='localhost', user='root', password='vk17', db='vk17', charset='utf8')

    pname, _, pid = current_process().name.partition('-')
    access_token = access_tokens[int(pid) % len(access_tokens)]

    session = vk.Session(access_token=access_token)
    api = vk.API(session, v='5.62', lang='ru')

    countries = shared_countries
    cities = shared_cities
    count = shared_count

    Finalize(conn, conn.close, exitpriority=0)


def try_get_profiles(user_ids, fields):
    while True:
        try:
            profiles = api.users.get(user_ids=user_ids, fields=fields)
            if not isinstance(profiles, list):
                continue
        except VkAPIError as e:
            if e.code == 6:
                continue
            if e.code == 10:
                time.sleep(30)
                continue
            print(e.message)
            raise
        except Timeout:
            continue
        except (ConnectionError, ChunkedEncodingError, HTTPError):
            time.sleep(30)
            continue
        except Exception as e:
            print(e)
            raise
        else:
            return profiles

def filter_text(text):
    return re.sub('[^\u0000-\uD7FF\uE000-\uFFFF]', '', text)


def get_age(bdate):
    today = date.today()
    d, m, *y = bdate.split('.')

    if not y:
        return None

    age = today.year - int(*y) - ((today.month, today.day) < (int(m), int(d)))

    return age if 0 < age < 100 else None

def has_child(relatives):
    for rel in relatives:
        if rel['type'] == 'child' or rel['type'] == 'grandchild':
            return True
    return False

def is_prof_edu(type_id):
    return type_id in {8, 9, 10, 11, 12}

def is_general_edu(type_id):
    return type_id in {0, 1, 2, 3, 4}

def get_school(schools):
    gen = []
    prof = []

    for school in schools:
        if 'type' in school:
            if is_prof_edu(school['type']):
                prof.append(school)
            elif is_general_edu(school['type']):
                gen.append(school)
        else:
            gen.append(school)

    schools = prof if prof else gen

    if not schools:
        return None

    years = []
    schools.reverse()
    for school in schools:
        if 'year_graduated' in school:
            years.append(school['year_graduated'])
        elif 'year_to' in school:
            years.append(school['year_to'])
        elif 'year_from' in school:
            years.append(school['year_from'])
        else:
            years.append(0)

    max_year = max(years)

    for school in schools:
        if 'year_from' in school and school['year_from'] == max_year:
            return school

    if max_year < date.today().year and years[0] == 0:
        return schools[0]

    return schools[years.index(max_year)]

def get_university(universities):
    years = []
    universities.reverse()
    for university in universities:
        grad = university['graduation'] if 'graduation' in university else 0
        years.append(grad)

    max_year = max(years)

    if max_year < date.today().year and years[0] == 0:
        return universities[0]

    return universities[years.index(max_year)]

def age_for_year(bdate, year):
    _, _, *y = bdate.split('.')

    if not y:
        return None

    age = year - int(*y)

    return age if 0 < age < 100 else None

def get_first_job(jobs):
    if not jobs:
        return None

    if 'from' not in jobs[0] and 'until' not in jobs[0]:
        return jobs[0]

    fst_year = jobs[0]['from'] if 'from' in jobs[0] else jobs[0]['until']

    years = []
    for job in jobs:
        if 'from' in job:
            years.append(job['from'])
        elif 'until' in job:
            years.append(job['until'])
        else:
            years.append(fst_year)

    return jobs[years.index(min(years))]

def get_current_job(jobs):
    if not jobs:
        return None

    years = []
    for job in jobs:
        if 'from' in job and 'until' not in job:
            years.append(job['from'])
        else:
            years.append(0)

    max_year = max(years)

    if not max_year:
        return jobs[-1] if 'until' not in jobs[-1] else None

    return jobs[years.index(max_year)]

def add_job_fields(u, p, job, company_field, position_field, city_field, age_field):
    company = filter_text(job['company']) if 'company' in job else 'group_id: {group}'.format(group=job['group_id'])
    u[company_field] = company if len(company) < 100 else None

    position = filter_text(job['position']) if 'position' in job else None
    u[position_field] = position if position and len(position) < 100 else None

    u[city_field] = job['city_id'] if 'city_id' in job and job['city_id'] in cities else None
    u[age_field] = age_for_year(p['bdate'], job['from']) if 'bdate' in p and 'from' in job else None


fields = ['has_photo', 'photo_50', 'sex', 'bdate', 'country', 'city', 'relation', 'relatives', 'occupation', 'schools',
          'universities', 'career', 'personal', 'music', 'movies', 'books', 'games', 'last_seen']

occupation = {'school': 1,
              'university': 2,
              'work': 3
              }

religion = {'Иудаизм': 1,
            'Православие': 2,
            'Католицизм': 3,
            'Протестантизм': 4,
            'Ислам': 5,
            'Буддизм': 6,
            'Конфуцианство': 7,
            'Светский гуманизм': 8,
            'Пастафарианство': 9
            }

def get_users(id_from):
    profiles = try_get_profiles(user_ids=range(id_from, id_from + 1000), fields=fields)

    users = []

    for p in profiles:
        try:
            if 'deactivated' in p:
                continue

            u = {'id': p['id']}

            u['first_name'] = p['first_name'] if p['first_name'].isalpha() and len(p['first_name']) < 50 else None
            u['last_name'] = p['last_name'] if p['last_name'].isalpha() and len(p['last_name']) < 50 else None

            u['last_seen'] = datetime.fromtimestamp(p['last_seen']['time']).date()

            u['photo'] = p['photo_50'] if p['has_photo'] and p['photo_50'] and len(p['photo_50']) < 255 else None

            u['sex'] = p['sex'] if 'sex' in p and p['sex'] in {1, 2} else None
            u['age'] = get_age(p['bdate']) if 'bdate' in p else None
            u['city'] = p['city']['id'] if 'city' in p and p['city']['id'] in cities else None

            if u['city']:
                u['country'] = cities[u['city']]
            else:
                u['country'] = p['country']['id'] if 'country' in p and p['country']['id'] in countries else None

            u['relation'] = p['relation'] if 'relation' in p and p['relation'] in range(1, 9) else None
            u['child'] = has_child(p['relatives']) if 'relatives' in p else None
            u['occupation'] = occupation[p['occupation']['type']] if 'occupation' in p else None

            school = get_school(p['schools']) if 'schools' in p and p['schools'] else None

            if school:
                u['school_id'] = school['id']
                u['school_class'] = school['class'] if 'class' in school and school['class'] and len(school['class']) < 5 else None
                u['school_type'] = school['type'] if 'type' in school and school['type'] in range(0, 14) else 0
                u['school_city'] = school['city'] if school['city'] in cities else None

                if 'year_graduated' in school or 'year_to' in school:
                    year = school['year_graduated'] if 'year_graduated' in school else school['year_to']
                    u['school_grad_year'] = year if 1900 < year < 2100 else None
                    u['school_grad_age'] = age_for_year(p['bdate'], year) if 'bdate' in p else None
                else:
                    u.update(school_grad_year=None, school_grad_age=None)
            else:
                u.update(school_id=None, school_class=None, school_type=None, school_city=None, school_grad_year=None,
                         school_grad_age=None)

            university = get_university(p['universities']) if 'universities' in p and p['universities'] else None

            if university:
                u['university_id'] = university['id']
                u['university_city'] = university['city'] if university['city'] in cities else None
                u['university_faculty'] = university['faculty'] if 'faculty' in university else None
                u['university_chair'] = university['chair'] if 'chair' in university else None

                if 'graduation' in university:
                    year = university['graduation']
                    u['university_grad_year'] = year if 1900 < year < 2100 else None
                    u['university_grad_age'] = age_for_year(p['bdate'], year) if 'bdate' in p else None
                else:
                    u.update(university_grad_year=None, university_grad_age=None)
            else:
                u.update(university_id=None, university_faculty=None, university_chair=None, university_city=None,
                         university_grad_year=None, university_grad_age=None)

            if university:
                u['education'] = 3
            elif school:
                u['education'] = 2 if 'type' in school and is_prof_edu(school['type']) else 1
            else:
                u['education'] = None

            fst_job = get_first_job(p['career']) if 'career' in p else None
            if fst_job:
                add_job_fields(u, p, fst_job, 'first_job_company', 'first_job_position', 'first_job_city', 'first_job_age')
            else:
                u.update(first_job_company=None, first_job_position=None, first_job_city=None, first_job_age=None)

            cur_job = get_current_job(p['career']) if 'career' in p else None
            if cur_job:
                add_job_fields(u, p, cur_job, 'cur_job_company', 'cur_job_position', 'cur_job_city', 'cur_job_age')
            else:
                u.update(cur_job_company=None, cur_job_position=None, cur_job_city=None, cur_job_age=None)

            if 'personal' in p:
                person = p['personal']

                pr = person['religion'] if 'religion' in person else None
                u['religion'] = religion[pr] if pr in religion else None

                u['political'] = person['political'] if 'political' in person and person['political'] in range(1, 10) else None
                u['life_main'] = person['life_main'] if 'life_main' in person and person['life_main'] in range(1, 9) else None
                u['people_main'] = person['people_main'] if 'people_main' in person and person['people_main'] in range(1, 7) else None
                u['smoking'] = person['smoking'] if 'smoking' in person and person['smoking'] in range(1, 6) else None
                u['alcohol'] = person['alcohol'] if 'alcohol' in person and person['alcohol'] in range(1, 6) else None
            else:
                u.update(religion=None, political=None, life_main=None, people_main=None, smoking=None, alcohol=None)

            u['music'] = filter_text(p['music'])[:65535] if 'music' in p and p['music'] else None
            u['movies'] = filter_text(p['movies'])[:65535] if 'movies' in p and p['movies'] else None
            u['books'] = filter_text(p['books'])[:65535] if 'books' in p and p['books'] else None
            u['games'] = filter_text(p['games'])[:65535] if 'games' in p and p['games'] else None

            users.append(u)

        except Exception as e:
            print(e)
            print(p)
            continue

    return users

users_cols = ['id', 'first_name', 'last_name', 'photo', 'sex', 'age', 'country', 'city', 'relation', 'child', 'occupation',
              'education', 'school_id', 'school_class', 'school_type', 'school_city', 'school_grad_year', 'school_grad_age',
              'university_id', 'university_faculty', 'university_chair', 'university_city', 'university_grad_year',
              'university_grad_age', 'first_job_company', 'first_job_position', 'first_job_city', 'first_job_age',
              'cur_job_company', 'cur_job_position', 'cur_job_city', 'cur_job_age', 'religion', 'political', 'life_main',
              'people_main', 'smoking', 'alcohol', 'music', 'movies', 'books', 'games', 'last_seen']

placeholders = ', '.join(['%({col})s'.format(col=col) for col in users_cols])

sql_insert_users = '''
    INSERT INTO users ({columns})
    VALUES ({values})'''.format(columns=', '.join(users_cols), values=placeholders)

def insert_users(id_from):
    with conn.cursor() as cur:
        try:
            cur.executemany(sql_insert_users, get_users(id_from))
        except pymysql.MySQLError as e:
            print('insert error: {}'.format(e))
            print('error in id_from: {}'.format(id_from))

    conn.commit()

    count.value += 1000
    if count.value % 10**6 == 0:
        print('{:,}'.format(count.value))


sql_get_countries = '''
    SELECT country_id
    FROM countries'''

sql_get_cities = '''
    SELECT city_id, country_id
    FROM cities'''

if __name__ == '__main__':
    start_time = time.time()

    access_tokens_path = 'access_tokens.txt'
    access_tokens = get_access_tokens(access_tokens_path)

    users_number = count_users()

    print('users number: {num}'.format(num=users_number))

    conn = pymysql.connect(host='localhost', user='root', password='vk17', db='vk17', charset='utf8')

    with conn.cursor() as cur:
        cur.execute(sql_get_countries)
        countries = {country: 1 for (country,) in cur}

        cur.execute(sql_get_cities)
        cities = {city: country for (city, country) in cur}

    conn.close()

    manager = Manager()
    shared_countries = manager.dict(countries)
    shared_cities = manager.dict(cities)
    shared_count = Value('i', 0)

    pool = Pool(processes=64, initializer=pool_init, initargs=(access_tokens, shared_countries, shared_cities, shared_count))

    try:
        pool.map(insert_users, range(1, users_number, 1000))
    finally:
        pool.close()
        pool.join()

    d = datetime(1, 1, 1) + timedelta(seconds=time.time() - start_time)
    print("--- {hour}:{min}:{sec} ---".format(hour=d.hour, min=d.minute, sec=d.second))
