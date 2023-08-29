from typing import Generator
import psycopg2
from psycopg2.extensions import connection
from psycopg2.extras import DictCursor, execute_batch
from config import settings
from models import TypesEnum
import json


def create_connection() -> Generator:
    """
    Создает новое подключение к бд PostgreSQL
    """
    conn = psycopg2.connect(
        host=settings.db.host,
        port=settings.db.port,
        dbname=settings.db.database,
        user=settings.db.user,
        password=settings.db.password,
        cursor_factory=DictCursor,
    )
    conn.autocommit = True
    try:
        yield conn
    finally:
        conn.close()


session_maker = create_connection()


def create_test_table(conn: connection):
    """
    Создает тестовую таблицу если она не существует
    :param conn:
    :return:
    """
    with conn.cursor() as cursor:
        cursor.execute("""
        create table if not exists test
        (
            id bigserial constraint pk_test primary key,
            "ParentId" bigint,
            "Name" varchar(512) not null,
            "Type" smallint not null
        );
        """)


def import_data(filepath):
    """
    Импортирует данные из filepath
    :param filepath:
    :return:
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        prepared_data = []
        for item in data:
            prepared_data.append((
                item.get('id', None),
                item.get('ParentId', None),
                item.get('Name', None),
                item.get('Type', None),
            ))

    conn = next(session_maker)
    create_test_table(conn)
    query = 'insert into test (id, "ParentId", "Name", "Type") values (%s, %s, %s, %s)'
    with conn.cursor() as cursor:
        execute_batch(cursor, query, prepared_data)


def get_employees_by_office_id(conn: connection, office_id: int):
    """
    Ищет сотрудников по ID офиса
    :param conn:
    :param office_id:
    :return:
    """
    query = """
        with recursive office_cte as (select id, "ParentId", "Name", "Type"
                                     from test
                                     where "id" = %s
                                     union all
                                     select c.id, c."ParentId", c."Name", c."Type"
                                     from test c
                                              join office_cte p on p.id = c."ParentId")
        select *
        from office_cte
        where "Type" = 3"""
    with conn.cursor() as cursor:
        cursor.execute(query, (office_id,))
        return cursor.fetchall()


def get_office_by_employee_id(conn: connection, employee_id: int):
    """
    Ищет офис, в котором работает сотрудник, по ID сотрудника
    :param conn:
    :param employee_id:
    :return:
    """
    query = """
        with recursive employees_cte as (select id, "ParentId", "Name", "Type"
                                      from test
                                      where "id" = %s
                                        and "Type" = 3
                                      union all
                                      select c.id, c."ParentId", c."Name", c."Type"
                                      from test c
                                               join employees_cte p on p."ParentId" = c."id")
        select *
        from employees_cte WHERE "Type" = 1"""
    with conn.cursor() as cursor:
        cursor.execute(query, (employee_id,))
        return cursor.fetchone()


def get_employee_by_id(conn: connection, employee_id: int):
    """
    Ищет сотрудника по ID
    :param conn:
    :param employee_id:
    :return:
    """
    query = 'select * from test where id = %s and "Type" = 3'
    with conn.cursor() as cursor:
        cursor.execute(query, (employee_id,))
        return cursor.fetchone()