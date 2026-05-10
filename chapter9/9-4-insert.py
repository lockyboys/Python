from module_912 import get_Conn

def insert_aa():
    conn = get_Conn()
    cur = conn.cursor()
    ins_query = '''
    insert into sj values(%s,%s,%s,%s,%s)
    '''
    li = [('김철수',71,81,91,3),('이영희',78,88,98,2),('강창수',79,89,99,4), ('이영희',78,88,98,2)] 
    cur.executemany(ins_query, li)
    conn.commit()
    conn.close()

if __name__ == '__main__':
 insert_aa()