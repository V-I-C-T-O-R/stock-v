import _sqlite3 as sqlite

from stock_choice import settings


class SqliteDB:

    def __init__(self,db_path):
        self.db_path = db_path
        self.__batch_insert_sql = "insert into {0}({1}) values ({2})"

    def __get_conn(self):
        return sqlite.connect(self.db_path)

    def execute_handle(self,sql):
        conn = None
        try:
            conn = self.__get_conn()
            conn.execute(sql)
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            try:
                if conn:
                    conn.close()
            except Exception as e:
                pass

    def execute_handle_file(self,sql_path):
        conn = None
        sql = None
        try:
            with open(sql_path, 'r', encoding='utf8') as f:
                sql = f.read()
            conn = self.__get_conn()
            conn.executescript(sql)
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            try:
                if conn:
                    conn.close()
            except Exception as e:
                pass

    def query_data(self,sql):
        cursor = None
        conn = None
        values = None
        try:
            conn = self.__get_conn()
            cursor = conn.cursor()
            cursor.execute(sql)
            values = cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            try:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
            except Exception as e:
                pass

        return values

    def batch_insert(self, table, item_names, values, batch_num=500):
        batch_sql = self.__batch_insert_sql.format(table,', '.join(item_names),', '.join(['?'] * len(item_names)))

        conn = None
        try:
            conn = self.__get_conn()
            contents = []
            flag = 0
            for v in values:
                contents.append(v)
                flag += 1
                if flag % batch_num == 0:
                    conn.executemany(batch_sql,contents)
                    conn.commit()
                    contents = []
            if contents:
                conn.executemany(batch_sql, contents)
                conn.commit()
                contents = None
        except Exception as e:
            print(e)
        finally:
            try:
                if conn:
                    conn.close()
            except Exception as e:
                pass

if __name__ == '__main__':
    settings.init()
    db = SqliteDB(settings.SQLITE_DB_NAME)

    # db.execute_handle('drop table stock_work_day_data')
    db.execute_handle('create index code_index on stock_work_day_data(code, date_day)')
    # data = db.query_data('select * from stock_work_day_data order by date_day asc limit 1')
    # print(data)
    #
    # data = [('2017-10-13' ,'19.911',20.195,20.400,19.911,80116.0,'000887',0.342840),('2017-10-14' ,'19.911',20.195,20.400,19.911,80116.0,'000887',0.342840)]
    # db.batch_insert('stock_work_day_data', ['date_day', 'open', 'close','high','low','volume','code','p_change'],data)
