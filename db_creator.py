import argparse
import sys
import psycopg2

deafult_conn = psycopg2.connect(dbname='postgres', user='postgres', host='localhost', password='password')
my_db_conn = psycopg2.connect(dbname="meta_x5", user="postgres", host='localhost', password='password')


def create_db(conn):
    dbname = "meta_x5"

    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute('CREATE DATABASE ' + dbname)

    cursor.close()
    conn.close()
    print(f'{dbname} created')


def delete_tables(conn):
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute('''DROP TABLE process''')
    cursor.execute('''DROP TABLE process_param''')
    cursor.execute('''DROP TABLE process_run_condition''')
    cursor.execute('''DROP TABLE process_user''')
    cursor.execute('''DROP TABLE process_quota''')
    print('all tables deleted')


def clean_tables(conn):
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute('''DELETE FROM process''')
    cursor.execute('''DELETE FROM process_param''')
    cursor.execute('''DELETE FROM process_run_condition''')
    cursor.execute('''DELETE FROM process_user''')
    cursor.execute('''DELETE FROM process_quota''')
    print('all tables cleaned')


def create_tables(conn):
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute('''
                    CREATE TABLE process_param(
                        name TEXT PRIMARY KEY,
                        value TEXT
                    )''')

    cursor.execute('''
                    CREATE TABLE process_run_condition(
                        type TEXT PRIMARY KEY,
                        value TEXT
                    )''')

    cursor.execute('''
                    CREATE TABLE process_user(
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        description TEXT
                    )''')

    cursor.execute('''
                    CREATE TABLE process_quota(
                        type TEXT PRIMARY KEY,
                        value INTEGER
                    )''')

    cursor.execute('''
                    CREATE TABLE process(
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        description TEXT,
                        flag INTEGER,
                        parameter TEXT REFERENCES process_param (name),
                        run_condition TEXT REFERENCES process_run_condition (type),
                        userID INTEGER REFERENCES process_user (id),
                        qouta TEXT REFERENCES process_quota (type)
                    )''')

    conn.commit()
    cursor.close()
    conn.close()
    print(f'tables created')


def test_data(conn):
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("""
                    INSERT INTO process_param(name, value)
                    VALUES
                        ('param1', '100'),
                        ('param2', '200'),
                        ('param3', '300'),
                        ('param4', '400'),
                        ('param5', '500')
                    """)

    cursor.execute("""
                    INSERT INTO process_run_condition(type, value)
                    VALUES
                        ('time1', '10:00'),
                        ('time2', '11:00'),
                        ('time3', '12:00'),
                        ('time4', '13:00'),
                        ('time5', '14:00')
                    """)

    cursor.execute("""
                    INSERT INTO process_user(id, name, description)
                    VALUES
                        (55, 'Flex_Fom', 'Best_boy'),
                        (44, 'Arny', 'Lol'),
                        (777, 'Hello', 'World'),
                        (12, 'Jony', 'Tot_samyi'),
                        (1337, 'Gpooo', 'description')
                    """)

    cursor.execute("""
                    INSERT INTO process_quota(type, value)
                    VALUES
                        ('aaa', 10),
                        ('bbb', 7),
                        ('ccc', 5),
                        ('ddd', 2),
                        ('eee', 15)
                    """)

    cursor.execute('''
                    INSERT INTO process(
                        id, name, description, flag,
                        parameter, run_condition, userID, qouta
                        )
                    VALUES
                        (1, 'Start_server', 'first', 1, 'param1', 'time1', 1337, 'aaa'),
                        (2, 'Start_server2', 'second', 0, 'param2', 'time2', 12, 'bbb'),
                        (3, 'Stop_server', 'descr1', 0, 'param3', 'time3', 777, 'ccc'),
                        (4, 'Kek', 'lol', 0, 'param4', 'time4', 44, 'ddd'),
                        (5, 'Privet', 'da', 1, 'param5', 'time5', 55, 'eee')
                    ''')
    conn.commit()
    cursor.close()
    conn.close()
    print(f'test data loaded')


def main():
    main_arg_parser = argparse.ArgumentParser(description="parser for db")
    subparsers = main_arg_parser.add_subparsers(title="subcommands", dest="subcommand")

    subparsers.add_parser("create_db", help="parser for create db")
    subparsers.add_parser("create_tab", help="parser for create tables")
    subparsers.add_parser("clean", help="parser for clean tables")
    subparsers.add_parser("del", help="parser for del tables")
    subparsers.add_parser("test_data", help="parser for test data load")

    args = main_arg_parser.parse_args()

    if args.subcommand is None:
        print("ERROR: specify either create, del or clean")
        sys.exit(1)

    if args.subcommand == "create_db":
        create_db(deafult_conn)
    elif args.subcommand == "create_tab":
        create_tables(my_db_conn)
    elif args.subcommand == "clean":
        clean_tables(my_db_conn)
    elif args.subcommand == "del":
        delete_tables(my_db_conn)
    elif args.subcommand == "test_data":
        test_data(my_db_conn)


if __name__ == "__main__":
    main()
