from module_912 import get_Conn
def delete_a(name):
    conn = get_Conn()
    cur = conn.cursor()
    cur.execute('''
    delete from sj where name = %s
    ''', (name,))
    conn.commit()
    conn.close()

if __name__ == '__main__': 
    delete_a('김철수')