import networkx as nx
import igraph
import csv
import collections


def get_student_cluster(graph, friends_students, need_spinglass):
    """
    Кластеризация социального графа пользователя.

    :param graph: социальный граф пользователя
    :param friends_students: список друзей пользователя, имеющих такое же учебное заведение
    :param need_spinglass: True, если требуется использовать комбинацию алгоритмов кластеризации multilevel и spinglass
    :return: выделенный кластер (множество идентификаторов пользователей)
    """

    if not need_spinglass or graph.ecount() > 4000 or not graph.is_connected():
        clusters = graph.community_multilevel()
    else:
        clusters = graph.community_spinglass()

    membership = clusters.membership

    clusters = collections.defaultdict(set)
    for u, c in zip(graph.vs['name'], membership):
        clusters[c].add(u)

    return max(clusters.values(), key=lambda cluster: len(cluster & friends_students))


def get_student_group(student, student_friends, friends_students, student_graph, min_group_size=10, max_group_size=30, need_spinglass=False):
    """
    Выделение учебной группы пользователя.

    :param student: идентификатор пользователя
    :param student_friends: список друзей пользователя или путь к файлу с данными в формате csv
    :param friends_students: список друзей пользователя, имеющих такое же учебное заведение, или путь к файлу с данными в формате csv
    :param student_graph: социальный граф пользователя (библиотека NetworkX) или путь к файлу с данными в формате csv (список рёбер)
    :param min_group_size: предполагаемый минимальный размер учебной группы
    :param max_group_size: предполагаемый максимальный размер учебной группы
    :param need_spinglass: True, если требуется использовать комбинацию алгоритмов кластеризации multilevel и spinglass
    :return: учебная группа пользователя в виде графа (библиотека NetworkX)
    """

    if type(student_friends) is str:
        with open(student_friends, 'r', newline='') as f:
            reader = csv.reader(f, delimiter=';')
            student_friends = {int(friend) for (friend,) in reader}

    if type(friends_students) is str:
        with open(friends_students, 'r', newline='') as f:
            reader = csv.reader(f, delimiter=';')
            friends_students = {friend for (friend,) in reader}
    else:
        friends_students = {str(friend) for friend in friends_students}

    if type(student_graph) is str:
        with open(student_graph, 'r', newline='') as f:
            reader = csv.reader(f, delimiter=';')
            graph = igraph.Graph.TupleList(reader)
    else:
        graph = igraph.Graph.TupleList((str(u), str(f)) for (u, f) in student_graph.edges())

    cluster = set()
    prev_cluster = set()
    while True:
        prev_cluster = cluster
        cluster = get_student_cluster(graph, friends_students, need_spinglass)

        if len(cluster) < max_group_size:
            if len(cluster) > min_group_size:
                graph = graph.subgraph(cluster)
            else:
                cluster = prev_cluster
            break

        if len(cluster) == len(prev_cluster):
            break

        graph = graph.subgraph(cluster)

    redundant_vs = graph.vs.select(_degree_le=3)
    graph.delete_vertices(redundant_vs)

    edges = []
    for edge in graph.es:
        edges.append((int(graph.vs[edge.source]['name']), int(graph.vs[edge.target]['name'])))

    group = nx.Graph(edges)

    group_friends = set(group.nodes()) & student_friends
    group.add_edges_from((student, friend) for friend in group_friends)

    return group


def get_statistics(group, groupmates):
    """
    Получение статистики.

    :param group: учебная группа пользователя в виде графа (библиотека NetworkX)
    :param groupmates: список одногруппников
    :return: размер группы, точность, полнота, F1-мера
    """

    group = set(group.nodes())

    size = len(group)
    rel = len(group & groupmates)

    if rel <= 1:
        return None

    precision = rel / size
    recall = rel / len(groupmates)
    f1 = 2 * precision * recall / (precision + recall)

    return size, precision, recall, f1


def print_statistics(statistics):
    """
    Вывод статистики.

    :param statistics: статистика
    :return:
    """

    print('size: {:.2f}'.format(statistics[0]))
    print('precision: {:.2f}'.format(statistics[1]))
    print('recall: {:.2f}'.format(statistics[2]))
    print('f1: {:.2f}'.format(statistics[3]))
