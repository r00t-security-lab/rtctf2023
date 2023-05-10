import sqlite3
from pathlib import Path

SQL_PATH = 'sql.db'


def get_back_filename(filename: str):
    def get_filename(no): return filename.split('.')[0] + f'.bak{no}.' + filename.split('.')[1]
    for i in range(10000):
        if not (path := Path(get_filename(i))).is_file():
            return path
    raise


if __name__ == '__main__':
    get_back_filename(SQL_PATH).write_bytes(Path(SQL_PATH).read_bytes())
    db_sess = sqlite3.connect(SQL_PATH)
    tables = db_sess.execute( '''select name from sqlite_master WHERE type='table' ''').fetchall()
    [db_sess.execute(f'drop table {table[0]}')
     for table in tables if table[0] != 'amis']
