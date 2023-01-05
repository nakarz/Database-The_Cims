from django.db import connection
from collections import namedtuple


def make_query(query):
    cursor = connection.cursor()
    try:
        cursor.execute('set search_path to cims')
        cursor.execute(query)
        result = namedtuple_fetch_all(cursor)
    except Exception as e:
        print(f"error: {e}")
        error_msg = str(e).split("CONTEXT")[0]
        return error_msg
    finally:
        cursor.execute('set search_path to public')
        cursor.close()
    return result


def namedtuple_fetch_all(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    if desc is None:
        return None
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]
