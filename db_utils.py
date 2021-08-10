"""
functions for interaction with the database.
"""
from db_secrets import DB_NAME, USER_NAME, PASSWORD, HOST
import pymysql


def create_connection():
    try:
        conn = pymysql.connect(host=HOST,
                               user=USER_NAME,
                               password=PASSWORD,
                               db=DB_NAME,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
        return conn
    except:
        return None


def run_query(query, args=[], conn=None):
    if not conn:
        conn = create_connection()

    with conn.cursor() as cursor:
        if query.lower().startswith("select"):
            cursor.execute(query=query, args=args)
            return cursor.fetchall()
        else:
            cursor.execute(query=query, args=args)
    try:
        conn.commit()
    except Exception as e:
        print("ERROR OCCURED WHILE DB COMMIT --- DB_UTILS: 43", e)


def insert_conversations(input_text, intent):
    sql_query = """insert into conversations(input_text, intent) values(%s, %s)"""
    run_query(sql_query, [input_text, intent])


def get_conversations():
    sql_query = """select input_text, intent from conversations"""
    rows = run_query(sql_query)
    return rows


def get_conversations_by_date(from_date, to_date):
    sql_query = """select input_text, intent from conversations where DATE(create_dt) >= %s and DATE(create_dt) <= %s"""
    return run_query(sql_query, [from_date, to_date])

def get_misses():
    sql_query = """select input_text, intent from conversations where intent='Default Fallback Intent'"""
    rows = run_query(sql_query)
    return rows


def get_misses_by_date(from_date, to_date):
    sql_query = """select input_text, intent from conversations where intent='Default Fallback Intent' and DATE(create_dt) >= %s and DATE(create_dt) <= %s"""
    return run_query(sql_query, [from_date, to_date])

if __name__ == '__main__':
    #insert_conversations('how does covid spread', 'Default Fallback Intent')
    get_misses_by_date('2021-08-10', '2021-08-10')
