"""
Получение списка городов для каждой страны.
"""


import pymysql
import vk
import time
from multiprocessing import Pool
from multiprocessing.util import Finalize


def get_cities(api, country, regions):
    cs = api.database.getCities(country_id=country, need_all=1, count=1000)

    city_items = cs['items']
    for i in range(1000, cs['count'], 1000):
        city_items += api.database.getCities(country_id=country, need_all=1, offset=i, count=1000)['items']

    cities = []
    for city in city_items:
        region = None
        if 'region' in city:
            region_title = city['region'].strip()
            if region_title in regions:
                region = regions[region_title]

        area = city['area'] if 'area' in city else None

        cities.append((city['id'], city['title'], region, country, area))

    return cities


conn = None
api = None

def pool_close():
    conn.commit()
    conn.close()

def pool_init():
    global conn
    global api

    conn = pymysql.connect(host='localhost', user='root', password='vk17', db='vk17', charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)

    session = vk.Session()
    api = vk.API(session, v='5.62', lang='ru')

    Finalize(conn, pool_close, exitpriority=0)


sql_get_countries = '''
    SELECT country_id
    FROM countries'''

sql_get_regions = '''
    SELECT region_id, region_title
    FROM regions
    WHERE country_id = %s'''

sql_insert_cities = '''
    INSERT INTO cities (city_id, city_title, region_id, country_id, area)
    VALUES (%s, %s, %s, %s, %s)'''


def insert_cities(country):
    with conn.cursor() as cur:
        cur.execute(sql_get_regions, country)
        regions = {region['region_title']: region['region_id'] for region in cur}

        cur.executemany(sql_insert_cities, get_cities(api, country, regions))


if __name__ == '__main__':
    start = time.time()

    conn = pymysql.connect(host='localhost', user='root', password='vk17', db='vk17')

    pool = Pool(processes=8, initializer=pool_init)

    with conn.cursor() as cur:
        cur.execute(sql_get_countries)
        countries = [country for (country,) in cur]

    pool.map(insert_cities, countries)

    pool.close()
    pool.join()

    print('{} sec'.format(time.time() - start))
