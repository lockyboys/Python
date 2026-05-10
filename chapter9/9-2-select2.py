from module_912 import get_Conn
def select_a(name):
    conn = get_Conn()
    cur = conn.cursor()
    cur.execute('''
                select * from sj
                where name like %s
                ''', (name,)) 

    rs = cur.fetchall()
    disp(rs) # 출력함수

    conn.close()

def disp(rs):
    tot = rs[0][1]+rs[0][2]+rs[0][3]
    # rs는 리스트. [('이영희', 75, 85, 95)]
    print('이름: ', rs[0][0])
    print('총점: ', tot)

if __name__ == '__main__':
    select_a('이영희')