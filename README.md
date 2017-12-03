# vk-student-groups

Выделение учебных групп на основе социального графа и информации из профилей пользователей социальной сети ВКонтакте.

Определение возраста и места проживания пользователей.

## Построение базы профилей пользователей

Для построения базы профилей необходимо использовать sql и python скрипты в следующем порядке:
1. [db_structure.sql](sql/db_structure.sql) - создание БД MySQL
2. [db_data.sql](sql/db_data.sql) - заполнение таблиц БД, необходимых для построения базы профилей
3. [get_countries.py](scripts/get-users/get_countries.py) - получение списка всех стран
4. [get_regions.py](scripts/get-users/get_regions.py) - получение списка регионов для каждой страны
5. [get_cities.py](scripts/get-users/get_cities.py) - получение списка городов для каждой страны
6. [get_users.py](scripts/get-users/get_users.py) - получение и обработка профилей

Для определения общего количества пользователей используется python-модуль [count_users](modules/count_users.py).

## Выделение учебных групп

Модули:
* [get_student_graph](modules/get_student_graph.py) - получение социального графа пользователя
* [get_student_group](modules/get_student_group.py) - выделение учебной группы пользователя

Пример использования модулей представлен в [student_group_sample.py](samples/student_group_sample.py).

## Определение возраста и места проживания пользователей

Для получения предполагаемых одногруппников необходимо использовать скрипты в следующем порядке:
1. [insert_school_students.sql](sql/insert_school_students.sql) и 
   [insert_university_students.sql](sql/insert_university_students.sql) - 
   заполнение таблиц БД идентификаторами школьников и студентов соответственно
2. [get_school_students_groups.py](scripts/get-groups/get_school_students_groups.py) и 
   [get_university_students_groups.py](scripts/get-groups/get_university_students_groups.py) - 
   выделение учебных групп для 1000 случайных школьников и студентов соответственно

Определение возраста и места проживания пользователей по полученным спискам одногруппников:
* [predict_age.py](scripts/predict/predict_age.py) - определение возраста
* [predict_city.py](scripts/predict/predict_city.py) - определение города проживания
* [predict_region.py](scripts/predict/predict_region.py) - определение региона проживания

## Используемые библиотеки

* [pymysql](https://pypi.python.org/pypi/PyMySQL)
* [vk](https://pypi.python.org/pypi/vk/2.0.2)
* [networkx](https://pypi.python.org/pypi/networkx)
* [igraph](http://igraph.org/python)
