import sqlite3 as s
import logging
import pandas as pd


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
    return True


# update datalabel_requestmodel ready column to ready
@db_connector
def update_status_ready(conn, name):
    cur = conn.cursor()
    cur.execute(f"""UPDATE datalabel_requestmodel SET ready='ready'
                    WHERE projectName='{name}'""")
    return True


@db_connector
def get_top_empty_row(conn, tableName=None):
    cur = conn.cursor()
    cur.execute(f"""SELECT * from {tableName}
                    WHERE category = 'no cat' and locked = '' LIMIT 1""")

    nextItem = cur.fetchone()

    # get category list
    cur.execute(f"""SELECT categories from requestForm
                    WHERE projectName = {tableName}""")
    categoryList = cur.fetchone()

    if nextItem is None or categoryList is None:
        return None
    #check nextItem and nextItem[0] type
    return nextItem[0], categoryList[0]


@db_connector
def check_table_labeling_complete(conn, tableName=None):
    qString = f"""SELECT fullDir, fileName, category from {tableName}"""

    qResult = pd.read_sql(qString, conn)

    if 'no cat' in qResult['category']:
        return False
    else:
        return qResult


@db_connector
def get_table_category(conn, projectName=None):
    qString = f"""SELECT categories from {projectName}"""

    qResult = pd.read_sql(qString, conn)

    if qResult:
        return qResult.loc[0, 'categories'].split(', ')


@db_connector
def update_status_exported(conn, tableName):
    cur = conn.cursor()
    cur.execute(f"""UPDATE datalabel_requestmodel SET ready='exported'
                    WHERE projectName='{tableName}'""")
    return True