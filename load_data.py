import psycopg2
import argparse
import sys


my_db_conn = psycopg2.connect(dbname="meta_x5", user="postgres", host="localhost", password="password")


def process_param(args, conn):
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f'''INSERT INTO process_param (name, value)
                        VALUES ('{args.p_name}', '{args.p_val}')
                        ON CONFLICT (name) DO UPDATE
                        SET value = EXCLUDED.value
                    ''')

    cursor.execute(f'''INSERT INTO process (
                            id,
                            parameter
                        )
                        VALUES (
                            {args.id},
                            (
                                SELECT process_param.name
                                FROM process_param
                                WHERE process_param.name = '{args.p_name}'
                            ))
                        ON CONFLICT (id) DO UPDATE
                        SET id = EXCLUDED.id,
                            parameter = EXCLUDED.parameter
                        ''')

    conn.commit()
    cursor.close()
    conn.close()
    print(f'Process parameters for processID:{args.id} added or edited')


def process_run_condition(args, conn):
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f'''INSERT INTO process_run_condition (type, value)
                        VALUES ('{args.c_type}', '{args.c_val}')
                        ON CONFLICT (type) DO UPDATE
                        SET value = EXCLUDED.value
                    ''')

    cursor.execute(f'''INSERT INTO process (
                            id,
                            run_condition
                        )
                        VALUES (
                            {args.id},
                            (
                                SELECT process_run_condition.type
                                FROM process_run_condition
                                WHERE process_run_condition.type = '{args.c_type}'
                            ))
                        ON CONFLICT (id) DO UPDATE
                        SET id = EXCLUDED.id,
                            run_condition = EXCLUDED.run_condition
                    ''')

    conn.commit()
    cursor.close()
    conn.close()
    print(f'Process run condition for processID:{args.id} added or edited')


def process_user(args, conn):
    conn.autocommit = True
    cursor = conn.cursor()

    columns_set = {
                'id': 'id = EXCLUDED.id',
                'u_id': 'userID = EXCLUDED.userID',
                'u_name': 'name = EXCLUDED.name',
                'u_descr': 'description = EXCLUDED.description'
                }

    _keys = [key for key, value in vars(args).items() if value is not None]
    _value = [value for key, value in vars(args).items() if value is not None]

    keys_columns_set = [k for k, v in columns_set.items() if k in _keys]
    value_columns_set = [v for k, v in columns_set.items() if k in _keys]

    _str_val_1 = ', '.join(str(elem) for elem in _value[2:3])
    _str_val_2 = ', '.join(repr(str(elem)) for elem in _value[3:])
    _sql_val = (_str_val_1 +', '+_str_val_2)

    _columns_1 = (', '.join(keys_columns_set[1:])).replace('u_id', 'id').replace('u_name', 'name').replace('u_descr', 'description')
    _columns_2 = (', '.join(keys_columns_set[1:3])).replace('u_id', 'id').replace('u_name', 'userID')
    _set_1 = ', '.join(value_columns_set[2:])
    _set_2 = ', '.join(value_columns_set[:2])

    cursor.execute(f'''INSERT INTO process_user ({_columns_1})
                        VALUES ({_sql_val})
                        ON CONFLICT (id) DO UPDATE
                        SET {_set_1}
                    ''')

    cursor.execute(f'''INSERT INTO process ({_columns_2})
                        VALUES (
                            {args.id},
                            (
                                SELECT process_user.id
                                FROM process_user
                                WHERE process_user.id = '{args.u_id}'
                            ))
                        ON CONFLICT (id) DO UPDATE
                        SET {_set_2}
                    ''')

    conn.commit()
    cursor.close()
    conn.close()
    print(f'Process user for processID:{args.id} added or edited')


def process_quota(args, conn):
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f'''INSERT INTO process_quota (type, value)
                        VALUES ('{args.q_type}', '{args.q_val}')
                        ON CONFLICT (type) DO UPDATE
                        SET value = EXCLUDED.value
                    ''')

    cursor.execute(f'''INSERT INTO process (
                            id,
                            qouta
                        )
                        VALUES (
                            {args.id},
                            (
                                SELECT process_quota.type
                                FROM process_quota
                                WHERE process_quota.type = '{args.q_type}'
                            ))
                        ON CONFLICT (id) DO UPDATE
                        SET id = EXCLUDED.id,
                            qouta = EXCLUDED.qouta
                    ''')

    conn.commit()
    cursor.close()
    conn.close()
    print(f'Process quota for processID:{args.id} added or edited')


def create_process(args, conn):
    conn.autocommit = True
    cursor = conn.cursor()

    columns_set = {
            'id': 'id = EXCLUDED.id',
            'name': 'name = EXCLUDED.name',
            'descr': 'description = EXCLUDED.description',
            'flag': 'flag = EXCLUDED.flag'
            }

    _keys = [key for key, value in vars(args).items() if value is not None]
    _value = [value for key, value in vars(args).items() if value is not None]

    keys_columns_set = [k for k, v in columns_set.items() if k in _keys]
    value_columns_set = [v for k, v in columns_set.items() if k in _keys]

    _str_val = ', '.join(repr(str(elem)) for elem in _value[2:-1])
    _sql_val = (str(_value[1])+', '+_str_val+', '+str(_value[-1])).replace(', ,', ',')

    _columns = (', '.join(keys_columns_set)).replace('descr', 'description')
    _set = ', '.join(value_columns_set)

    cursor.execute(f'''INSERT INTO process ({_columns})
                        VALUES ({_sql_val})
                        ON CONFLICT (id) DO UPDATE
                        SET {_set}
                    ''')

    conn.commit()
    cursor.close()
    conn.close()
    print(f'{_columns} added or changed')


def main():

    main_arg_parser = argparse.ArgumentParser(description="parser for x5 processes")
    subparsers = main_arg_parser.add_subparsers(title="subcommands", dest="subcommand")

    process_arg_parser = subparsers.add_parser("process", help="add process")
    process_arg_parser.add_argument(
        "--id", type=int, required=True, help="process id"
        )
    process_arg_parser.add_argument(
        "--name", type=str, help="process name"
        )
    process_arg_parser.add_argument(
        "--descr", type=str, help="process description"
        )
    process_arg_parser.add_argument(
        "--flag", type=int, choices=[0, 1], help="1-process active/ 0-process not active"
        )

    param_arg_parser = subparsers.add_parser("parameter", help="add parameter for process ")
    param_arg_parser.add_argument(
        "--id", type=int, required=True, help="process id"
        )
    param_arg_parser.add_argument(
        "--p_name", type=str, required=True, help="process parameter name"
        )
    param_arg_parser.add_argument(
        "--p_val", type=str, required=True, help="process parameter value"
        )

    cond_arg_parser = subparsers.add_parser("condition", help="add process run condition")
    cond_arg_parser.add_argument(
        "--id", type=int, required=True, help="process id"
        )
    cond_arg_parser.add_argument(
        "--c_type", type=str, required=True, help="run condition"
        )
    cond_arg_parser.add_argument(
        "--c_val", type=str, required=True, help="run condition value"
        )

    user_arg_parser = subparsers.add_parser("user", help="add process user")
    user_arg_parser.add_argument(
        "--id", type=int, required=True, help="process id"
        )
    user_arg_parser.add_argument(
        "--u_id", type=int, required=True, help="process user id"
        )
    user_arg_parser.add_argument(
        "--u_name", type=str, required=True, help="process user name"
        )
    user_arg_parser.add_argument(
        "--u_descr", type=str, help="process user description"
        )

    qouta_arg_parser = subparsers.add_parser("qouta", help="add process qouta")
    qouta_arg_parser.add_argument(
        "--id", type=int, required=True, help="process id"
        )
    qouta_arg_parser.add_argument(
        "--q_type", type=str, required=True, help="process qouta type"
        )
    qouta_arg_parser.add_argument(
        "--q_val", type=int, required=True, help="process qouta value"
        )

    args = main_arg_parser.parse_args()

    if args.subcommand is None:
        print("ERROR: specify either process, parameter, user or qouta \nU can use: -h")
        sys.exit(1)

    if args.subcommand == "process":
        if len([key for key, value in vars(args).items() if value is not None]) == 2:
            print('Enter an additional parameter except ID')
        else:
            create_process(args, my_db_conn)
    elif args.subcommand == "parameter":
        process_param(args, my_db_conn)
    elif args.subcommand == "condition":
        process_run_condition(args, my_db_conn)
    elif args.subcommand == "user":
        process_user(args, my_db_conn)
    elif args.subcommand == "qouta":
        process_quota(args, my_db_conn)


if __name__ == "__main__":
    main()
