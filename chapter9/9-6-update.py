from module_912 import get_Conn

def update_a(name, jum):
    conn = get_Conn()
    cur = conn.cursor()
    cur.execute('''
    update sj set kor=%s
    where name=%s''', (jum, name))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    update_a('김철수',100)