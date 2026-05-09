from module_912 import get_Conn

def create_table():
 conn = get_Conn()
 cur = conn.cursor()
 cur.execute('''
 create table sj(
 name varchar(20),
 kor int,
 eng int,
 math int)
 ''')
 conn.commit()
 conn.close()
if __name__ == '__main__':
 create_table()