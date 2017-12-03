"""
Определение города проживания пользователей.

Для каждого пользователя место проживания определяется как наиболее часто встречаемое в группе, к которой он относится.
Вычисляется точность.

В переменной groupmates_dir указывается путь к спискам одногруппников в формате csv.
"""


import os
import csv
import pymysql
from collections import Counter


if __name__ == '__main__':
    conn = pymysql.connect(host='localhost', user='root', password='vk17', db='vk17')

    groupmates_dir = 'groupmates'

    sql_get_users_cities = '''
         SELECT city
         FROM users
         WHERE id IN ({}) AND city IS NOT NULL
     '''

    count_all = 0
    count = 0
    true_predicted = 0

    for file in os.listdir(groupmates_dir):
        with open(os.path.join(groupmates_dir, file), 'r', newline='') as f:
            reader = csv.reader(f, delimiter=';')
            groupmates = {int(g) for (g,) in reader}

        if not groupmates:
            continue

        count_all += len(groupmates)

        with conn.cursor() as cur:
            placeholders = ', '.join(['%s'] * len(groupmates))
            cur.execute(sql_get_users_cities.format(placeholders), list(groupmates))

            cities = [city for (city,) in cur.fetchall()]

        count += len(cities)

        if len(cities) < 2:
            continue

        for city in cities.copy():
            cities.remove(city)

            predicted_city = Counter(cities).most_common(1)[0][0]
            if predicted_city == city:
                true_predicted += 1

            cities.append(city)

    acc = true_predicted / count

    print('count_all: {}'.format(count_all))
    print('count: {}'.format(count))
    print('true_predicted: {}'.format(true_predicted))
    print('acc: {:.2f}'.format(acc))
