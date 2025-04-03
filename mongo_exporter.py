import time
import mariadb
from prometheus_client import start_http_server, Gauge

db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'mysql',
    'port': 3306 
}

connection_status = Gauge('mariadb_connection_status', 'Status of MariaDB connection (1 if connected, 0 otherwise)')

def check_connection():
    try:
        conn = mariadb.connect(**db_config)
        conn.close()
        connection_status.set(1)
    except mariadb.Error as err:
        print(f"Error connecting to MariaDB: {err}")
        connection_status.set(0)

def main():
    start_http_server(8000) 
    while True:
        check_connection()
        time.sleep(10)

if __name__ == '__main__':
    main()
