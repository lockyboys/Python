from module_912 import get_Conn

def select_a():
    conn = get_Conn()
    cur = conn.cursor()
    cur.execute('select * from sj')
    rs = cur.fetchall()
    for i in rs:
        print(f"{i}\n")
    conn.close()
    print(rs)

if __name__ == '__main__':
    select_a()