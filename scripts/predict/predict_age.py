"""
Определение возраста пользователей.

Алгоритм:
- определение наиболее часто встречаемого возраста в группе;
- вычисление среднего возраста среди пользователей, чей возраст отличается от самого частого не более чем на 3 года;
- округление полученного значения возраста до ближайшего целого.

Вычисляется точность и средняя абсолютная ошибка (MAE) в годах.

В переменной groupmates_dir указывается путь к спискам одногруппников в формате csv.
"""


import os
import csv
import pymysql
from collections import Counter
from statistics import mean


if __name__ == '__main__':
    conn = pymysql.connect(host='localhost', user='root', password='vk17', db='vk17')

    groupmates_dir = 'groupmates'

    sql_get_users_ages = '''
        SELECT age
        FROM users
        WHERE id IN ({}) AND age IS NOT NULL
    '''

    count_all = 0
    count = 0
    true_predicted = 0
    sum_err = 0

    for file in os.listdir(groupmates_dir):
        with open(os.path.join(groupmates_dir, file), 'r', newline='') as f:
            reader = csv.reader(f, delimiter=';')
            groupmates = {int(g) for (g,) in reader}

        if not groupmates:
            continue

        count_all += len(groupmates)

        with conn.cursor() as cur:
            placeholders = ', '.join(['%s'] * len(groupmates))
            cur.execute(sql_get_users_ages.format(placeholders), list(groupmates))

            ages = [age for (age,) in cur.fetchall()]

        count += len(ages)

        if len(ages) < 2:
            continue

        for age in ages.copy():
            ages.remove(age)

            mode = Counter(ages).most_common(1)[0][0]
            predicted_age = round(mean(age for age in ages if abs(age - mode) <= 3))

            if abs(age - predicted_age) <= 0.15 * age:
                true_predicted += 1

            sum_err += abs(age - predicted_age)

            ages.append(age)

    acc = true_predicted / count
    mae = sum_err / count

    print('count_all: {}'.format(count_all))
    print('count: {}'.format(count))
    print('true_predicted: {}'.format(true_predicted))
    print('acc: {:.2f}'.format(acc))
    print('mae: {:.2f}'.format(mae))
