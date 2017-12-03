"""
Получение списка регионов для каждой страны.
"""


import pymysql
import vk


def get_regions(api, country):
    regions = api.database.getRegions(country_id=country, count=1000)['items']

    return [(region['id'], region['title'], country) for region in regions]


if __name__ == '__main__':
    session = vk.Session()
    api = vk.API(session, v='5.62', lang='ru')

    conn = pymysql.connect(host='localhost', user='root', password='vk17', db='vk17', charset='utf8')

    sql_get_countries = '''
        SELECT country_id
        FROM countries'''

    sql_insert_regions = '''
        INSERT INTO regions (region_id, region_title, country_id)
        VALUES (%s, %s, %s)'''

    with conn.cursor() as cur:
        cur.execute(sql_get_countries)

        countries = cur.fetchall()

        for (country,) in countries:
            cur.executemany(sql_insert_regions, get_regions(api, country))

    conn.commit()
    conn.close()
