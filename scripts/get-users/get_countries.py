"""
Получение списка всех стран.
"""


import pymysql
import vk


def get_countries(api):
    countries = api.database.getCountries(need_all=1, count=1000)['items']

    return [(country['id'], country['title']) for country in countries]


if __name__ == '__main__':
    session = vk.Session()
    api = vk.API(session, v='5.62', lang='ru')

    conn = pymysql.connect(host='localhost', user='root', password='vk17', db='vk17', charset='utf8')

    sql = '''
        INSERT INTO countries (country_id, country_title)
        VALUES (%s, %s)'''

    with conn.cursor() as cur:
        cur.executemany(sql, get_countries(api))

    conn.commit()
    conn.close()
