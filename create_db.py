from db_secrets import DB_NAME, USER_NAME, PASSWORD, HOST
import pymysql


def create_connection(DB_NAME):
    """ create a database connection to the SQLite database
        specified by db_file
    """
    try:
        conn = pymysql.connect(host=HOST,
                               user=USER_NAME,
                               password=PASSWORD,
                               db=DB_NAME,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)

        return conn
    except Exception as e:
        print("Connection to the database could not be created: ", e)
        return None


def create_tables(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Exception as e:
        print("Tables could not be created:", e)


def create_db():
    """
    A function used to create a database file to store all the data
    """
    connection = create_connection(DB_NAME)
    sql_create_conversation_table = """CREATE TABLE IF NOT EXISTS conversations (
                                  conversation_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                                  input_text text,
                                  intent text,
                                  create_dt timestamp DEFAULT CURRENT_TIMESTAMP
                                ); """
    create_tables(conn=connection, create_table_sql=sql_create_conversation_table)


if __name__ == '__main__':
    create_db()
