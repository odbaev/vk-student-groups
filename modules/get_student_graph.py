import pymysql
import vk
import networkx as nx
import igraph
import time
import collections
from datetime import date
from multiprocessing import Pool
from vk.exceptions import VkAPIError
from requests.exceptions import Timeout, ConnectionError, ChunkedEncodingError, HTTPError


session = vk.Session()
api = vk.API(session, v='5.62')


def try_vk_request(request, *args, **kwargs):
    """
    Выполнение запроса (метода) VK API с обработкой возникающих ошибок.

    :param request: запрос
    :param args: позиционные аргументы
    :param kwargs: именованные аргументы
    :return: результат запроса
    """

    while True:
        try:
            response = request(*args, **kwargs)
        except VkAPIError as e:
            if e.code == 6:
                continue
            if e.code == 10:
                time.sleep(30)
                continue
            if e.code == 15:
                return {'items': set()}
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
            return response


def get_friends(user):
    """
    Получение списка друзей пользователя.

    :param user: идентификатор пользователя
    :return: идентификатор пользователя и множество идентификаторов друзей пользователя
    """

    user_friends = try_vk_request(api.friends.get, user_id=user, fields=['deactivated'])['items']
    active_friends = {friend['id'] for friend in user_friends if 'deactivated' not in friend}

    return user, active_friends


def get_school_friends(conn, student_friends, school_id):
    """
    Получение списка друзей пользователя по школе.

    :param conn: соединение с БД профилей пользователей
    :param student_friends: список идентификаторов друзей пользователя
    :param school_id: идентификатор школы пользователя
    :return: множество идентификаторов друзей пользователя по школе
    """

    sql_get_school_friends = '''
        SELECT id
        FROM users
        WHERE id IN ({}) AND school_id = {}
    '''

    placeholders = ', '.join(['%s'] * len(student_friends))
    sql_get_school_friends = sql_get_school_friends.format(placeholders, school_id)

    with conn.cursor() as cur:
        cur.execute(sql_get_school_friends, list(student_friends))
        school_friends = {user for (user,) in cur.fetchall()}

    return school_friends


def get_university_friends(conn, student_friends, university_id, university_faculty=None, university_chair=None):
    """
    Получение списка друзей пользователя по вузу.

    :param conn: соединение с БД профилей пользователей
    :param student_friends: список идентификаторов друзей пользователя
    :param university_id: идентификатор университета
    :param university_faculty: идентификатор факультета
    :param university_chair: идентификатор кафедры
    :return: множество идентификаторов друзей пользователя по вузу
    """

    sql_get_university_friends = '''
        SELECT id
        FROM users
        WHERE id IN ({}) AND university_id = {}
    '''

    placeholders = ', '.join(['%s'] * len(student_friends))
    sql_get_university_friends = sql_get_university_friends.format(placeholders, university_id)

    if university_faculty:
        sql_get_university_friends += ' AND university_faculty = {}'.format(university_faculty)
        if university_chair:
            sql_get_university_friends += ' AND university_chair = {}'.format(university_chair)

    with conn.cursor() as cur:
        cur.execute(sql_get_university_friends, list(student_friends))
        university_friends = {user for (user,) in cur.fetchall()}

    return university_friends


def get_school(conn, student):
    """
    Получение школы из профиля пользователя.

    :param conn: соединение с БД профилей пользователей
    :param student: идентификатор пользователя
    :return: идентификатор школы пользователя
    """

    sql_get_school = '''
        SELECT school_id
        FROM users
        WHERE id = %s AND (school_grad_year >= year(curdate()) OR school_grad_year is null)
    '''

    with conn.cursor() as cur:
        cur.execute(sql_get_school, student)
        school = cur.fetchone()

    return school[0] if school else None


def get_possible_school(conn, student, student_friends):
    """
    Определение возможной школы пользователя.

    :param conn: соединение с БД профилей пользователей
    :param student: идентификатор пользователя
    :param student_friends: список идентификаторов друзей пользователя
    :return: идентификатор школы пользователя
    """

    school = get_school(conn, student)

    if school:
        return school

    sql_get_possible_school = '''
        SELECT school_id
        FROM users
        WHERE id IN ({})
        GROUP BY school_id
        ORDER BY COUNT(school_id) DESC
        LIMIT 1
    '''

    placeholders = ', '.join(['%s'] * len(student_friends))
    sql_get_possible_school = sql_get_possible_school.format(placeholders)

    with conn.cursor() as cur:
        cur.execute(sql_get_possible_school, list(student_friends))
        school = cur.fetchone()[0]

    return school


def get_university(conn, student):
    """
    Получение вуза из профиля пользователя

    :param conn: соединение с БД профилей пользователей
    :param student: идентификатор пользователя
    :return: идентификаторы университета, факультета, кафедры
    """

    sql_get_university = '''
        SELECT university_id, university_faculty, university_chair
        FROM users
        WHERE id = %s AND (university_grad_year >= year(curdate()) OR university_grad_year is null)
    '''

    with conn.cursor() as cur:
        cur.execute(sql_get_university, student)
        university = cur.fetchone()

    return university


def get_possible_university(conn, student, student_friends, need_faculty=True, need_chair=False):
    """
    Определение возможного вуза пользователя.

    :param conn: соединение с БД профилей пользователей
    :param student: идентификатор пользователя
    :param student_friends: список идентификаторов друзей пользователя
    :param need_faculty: True, если требуется определить возможный факультет пользователя
    :param need_chair: True, если требуется определить возможную кафедру пользователя
    :return: идентификаторы университета, факультета, кафедры
    """

    university = get_university(conn, student)

    if university:
        university = university[:1 if not need_faculty else 2 if not need_chair else 3]
        if all(university):
            return university

    university_cols = 'university_id'
    if need_faculty:
        university_cols += ', university_faculty'
        if need_chair:
            university_cols += ', university_chair'

    sql_get_possible_university = '''
        SELECT {}
        FROM users
        WHERE id IN ({})
        GROUP BY {}
        ORDER BY COUNT({}) DESC
        LIMIT 1
    '''

    placeholders = ', '.join(['%s'] * len(student_friends))
    count_expr = ' and'.join(university_cols.split(','))
    sql_get_possible_university = sql_get_possible_university.format(university_cols, placeholders, university_cols, count_expr)

    with conn.cursor() as cur:
        cur.execute(sql_get_possible_university, list(student_friends))
        university = cur.fetchone()

    return university


def get_friends_students_cluster(graph, friends_students, need_spinglass):
    """
    Кластеризация графа друзей пользователя.

    :param graph: граф друзей пользователя
    :param friends_students: список друзей пользователя, имеющих такое же учебное заведение
    :param need_spinglass: True, если требуется использовать комбинацию алгоритмов кластеризации multilevel и spinglass
    :return: выделенный кластер (множество идентификаторов друзей пользователя)
    """

    g = igraph.Graph.TupleList(graph.edges())

    if not need_spinglass or g.ecount() > 4000 or not g.is_connected():
        clusters = g.community_multilevel()
    else:
        clusters = g.community_spinglass()

    membership = clusters.membership

    clusters = collections.defaultdict(set)
    for u, c in zip(g.vs['name'], membership):
        clusters[c].add(u)

    cluster = set()
    for c in clusters:
        if len(clusters[c] & friends_students) != 0:
            cluster |= clusters[c]

    return cluster


def get_student_graph(pool, student, student_friends, friends_students, need_spinglass=False):
    """
    Получение социального графа пользователя.

    :param pool: пул процессов (библиотека multiprocessing)
    :param student: идентификатор пользователя
    :param student_friends: список друзей пользователя
    :param friends_students: список друзей пользователя, имеющих такое же учебное заведение
    :param need_spinglass: True, если требуется использовать комбинацию алгоритмов кластеризации multilevel и spinglass
    :return: социальный граф пользователя (библиотека NetworkX)
    """

    graph = nx.Graph()

    for u, fs in pool.imap_unordered(get_friends, student_friends):
        graph.add_edges_from((u, f) for f in fs & student_friends)

    cluster = get_friends_students_cluster(graph, friends_students, need_spinglass)
    graph = graph.subgraph(cluster)

    for u, fs in pool.imap_unordered(get_friends, graph.nodes()):
        graph.add_edges_from((u, f) for f in fs - student_friends - {student})

    redundant_nodes = {node for node, degree in nx.degree(graph).items() if degree <= 2}
    graph.remove_nodes_from(redundant_nodes)

    foafs = set(graph.nodes()) - student_friends

    for u, fs in pool.imap_unordered(get_friends, foafs):
        graph.add_edges_from((u, f) for f in fs & foafs)

    return graph
