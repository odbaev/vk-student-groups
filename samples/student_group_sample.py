import pymysql
import vk
import networkx as nx
import igraph
import time
import os
import csv
from datetime import datetime, timedelta
from multiprocessing import Pool
from modules.get_student_graph import *
from modules.get_student_group import *


if __name__ == '__main__':
    start_time = time.time()

    session = vk.Session()
    api = vk.API(session, v='5.62')

    # Соединение с БД профилей пользователей
    conn = pymysql.connect(host='localhost', user='root', password='vk17', db='vk17')
    pool = Pool(processes=64)

    # Путь хранения списка друзей пользователя
    friends_dir = 'friends'

    # Путь хранения списка друзей пользователя, имеющих такое же учебное заведение
    friends_students_dir = 'friends_students'

    # Путь хранения социального графа пользователя
    graphs_dir = 'graphs'

    # Путь хранения учебной группы пользователя
    groups_dir = 'groups'

    os.makedirs(friends_dir, exist_ok=True)
    os.makedirs(friends_students_dir, exist_ok=True)
    os.makedirs(graphs_dir, exist_ok=True)
    os.makedirs(groups_dir, exist_ok=True)

    # Получаем список одногруппников
    with open('group.csv', 'r', newline='') as f:
        reader = csv.reader(f, delimiter=';')
        groupmates = {int(g) for (g,) in reader}

    students = groupmates

    count = 0
    no_group_count = 0
    stats = []

    for student in students:
        count += 1

        # Пропускаем деактивированных пользователей (страница удалена или заблокирована)
        if 'deactivated' in try_vk_request(api.users.get, user_id=student)[0]:
            print('deactivated {}'.format(student))
            continue

        # Получаем список друзей пользователя
        student_friends = get_friends(student)[1]

        # Определяем возможную школу пользователя
        school = get_possible_school(conn, student, student_friends)

        # Получаем список друзей пользователя по школе
        friends_students = get_school_friends(conn, student_friends, school)

        # # Определяем возможный вуз пользователя
        # university = get_possible_university(conn, student, student_friends)
        #
        # # Получаем список друзей пользователя по вузу
        # friends_students = get_university_friends(conn, student_friends, *university)

        # Пропускаем пользователей, для которых не удалось найти друзей, имеющих такое же учебное заведение
        if not friends_students:
            print('no friends students for {}'.format(student))
            continue

        # Получаем социальный граф пользователя
        graph = get_student_graph(pool, student, student_friends, friends_students)

        # Пропускаем пользователей, для которых не удалось получить социальный граф
        if not graph:
            print('no graph for {}'.format(student))
            continue

        # Сохраняем список друзей пользователя в формате csv
        with open(os.path.join(friends_dir, '{}.csv'.format(student)), 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows((friend,) for friend in student_friends)

        # Сохраняем список друзей пользователя, имеющих такое же учебное заведение, в формате csv
        with open(os.path.join(friends_students_dir, '{}.csv'.format(student)), 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows((friend,) for friend in friends_students)

        # Сохраняем социальный граф пользователя в формате csv (список рёбер)
        nx.write_edgelist(graph, os.path.join(graphs_dir, '{}.csv'.format(student)), delimiter=';', data=False)

        # # Указываем пути к файлам с данными в формате csv
        # student_friends = os.path.join(friends_dir, '{}.csv'.format(student))
        # friends_students = os.path.join(friends_students_dir, '{}.csv'.format(student))
        # graph = os.path.join(graphs_dir, '{}.csv'.format(student))

        # Выделяем учебную группу пользователя
        group = get_student_group(student, student_friends, friends_students, graph)

        # Сохраняем выделенную группу в формате csv (список рёбер)
        nx.write_edgelist(group, os.path.join(groups_dir, '{}.csv'.format(student)), delimiter=';', data=False)

        # Получаем статистику по выделенной группе (размер группы, точность, полнота, F1-мера)
        statistics = get_statistics(group, groupmates)

        # # Выводим статистику по выделенной группе
        # print_statistics(statistics)

        # Если в выделенной группе не было ни одного одногруппника, увеличиваем количество невыделенных групп
        if statistics:
            stats.append(statistics)
        else:
            no_group_count += 1

        print('{}/{}'.format(count, len(students)))

    # Выводим количество невыделенных групп
    print('no_group_count: {}'.format(no_group_count))

    # Выводим средние значения статистики для выделенных групп
    print('mean values')
    statistics = [sum(vals) / len(stats) for vals in zip(*stats)]
    print_statistics(statistics)

    conn.close()
    pool.close()
    pool.join()

    d = datetime(1, 1, 1) + timedelta(seconds=time.time() - start_time)
    print("--- {hour}:{min}:{sec} ---".format(hour=d.hour, min=d.minute, sec=d.second))
