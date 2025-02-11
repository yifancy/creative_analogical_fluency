import pymysql


def init_db():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='analogy', charset='utf8mb4', port=3306)
    cursor = conn.cursor()
    return conn, cursor
