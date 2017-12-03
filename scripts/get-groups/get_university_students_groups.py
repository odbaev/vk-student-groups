"""
Выделение учебных групп для 1000 случайных студентов.

Берутся только пользователи, имеющие от 10 до 300 друзей и не меньше трёх друзей из того же учебного заведения.
Полученные данные сохраняются в формате csv по путям, указанным в соответствующих переменных:
friends_dir - списки друзей пользователей;
friends_students_dir - списки друзей пользователей, имеющих такие же учебные заведения;
graphs_dir - социальные графы пользователей;
groups_dir - учебные группы пользователей;
groupmates_dir - списки одногруппников.
"""


import pymysql
import vk
import networkx as nx
import igraph
import time
import os
import csv
from datetime import datetime, timedelta
from modules.get_student_graph import *
from modules.get_student_group import *


if __name__ == '__main__':
    start_time = time.time()

    session = vk.Session()
    api = vk.API(session, v='5.62')

    conn = pymysql.connect(host='localhost', user='root', password='vk17', db='vk17')
    pool = Pool(processes=64)

    friends_dir = 'friends'
    friends_students_dir = 'friends_students'
    graphs_dir = 'graphs'
    groups_dir = 'groups'
    groupmates_dir = 'groupmates'

    os.makedirs(friends_dir, exist_ok=True)
    os.makedirs(friends_students_dir, exist_ok=True)
    os.makedirs(graphs_dir, exist_ok=True)
    os.makedirs(groups_dir, exist_ok=True)
    os.makedirs(groupmates_dir, exist_ok=True)

    sql_get_university_students_rand = '''
        SELECT student_id
        FROM university_students
        ORDER BY RAND()
        LIMIT 10000'''

    with conn.cursor() as cur:
        cur.execute(sql_get_university_students_rand)
        students = {student for (student,) in cur.fetchall()}

    count = 0

    for student in students:
        if 'deactivated' in try_vk_request(api.users.get, user_id=student)[0]:
            continue

        student_friends = get_friends(student)[1]

        if len(student_friends) < 10 or len(student_friends) > 300:
            continue

        university = get_university(conn, student)
        friends_students = get_university_friends(conn, student_friends, *university)

        if len(friends_students) < 3:
            continue

        graph = get_student_graph(pool, student, student_friends, friends_students)

        if not graph:
            continue

        with open(os.path.join(friends_dir, '{}.csv'.format(student)), 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows((friend,) for friend in student_friends)

        with open(os.path.join(friends_students_dir, '{}.csv'.format(student)), 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows((friend,) for friend in friends_students)

        nx.write_edgelist(graph, os.path.join(graphs_dir, '{}.csv'.format(student)), delimiter=';', data=False)

        group = get_student_group(student, student_friends, friends_students, graph)

        nx.write_edgelist(group, os.path.join(groups_dir, '{}.csv'.format(student)), delimiter=';', data=False)

        with open(os.path.join(groupmates_dir, '{}.csv'.format(student)), 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows((groupmate,) for groupmate in group.nodes())

        count += 1

        if count % 10 == 0:
            print(count)

        if count == 1000:
            break

    conn.close()
    pool.close()
    pool.join()

    d = datetime(1, 1, 1) + timedelta(seconds=time.time() - start_time)
    print("--- {hour}:{min}:{sec} ---".format(hour=d.hour, min=d.minute, sec=d.second))
