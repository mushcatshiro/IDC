import sqlite3 as s
import logging


logging.basicConfig(filename="db_operations.log",
                    level=logging.INFO,
                    format="%(asctime)s:%(levelname)s:%(message)s")


def db_connector(func):
    def with_connection_(*args, **kwargs):
        conn = s.connect("db.sqlite3")
        try:
            rv = func(conn, *args, **kwargs)
        except Exception:
            conn.rollback()
            logging.error("Database connection error")
            raise
        else:
            conn.commit()
        finally:
            conn.close()
        return rv
    return with_connection_


# get all files in the given directory
# create a DataFrame including index, full dir, filename, category
# save dataframe to database
@db_connector
def initialize_project(conn, dataframe, name):
    dataframe.to_sql(name, conn)


# update datalabel_requestmodel ready column to ready
@db_connector
def update_status(conn, name):
    cur = conn.cursor()
    cur.execute(f"""UPDATE datalabel_requestmodel SET ready='ready'
                    WHERE projectName='{name}'""")


@db_connector
def get_top_empty_row(conn, tableName=None):
    cur = conn.cursor()
    cur.execute(f"""SELECT * from {tableName} WHERE category IS NULL LIMIT 1""")

    nextItem = cur.fetchone()

    if nextItem is None:
        return None
    #check nextItem and nextItem[0] type
    return nextItem[0]