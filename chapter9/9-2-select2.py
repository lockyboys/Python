from module_912 import get_Conn

def select_a(name):
    conn = get_Conn()
    cur = conn.cursor()
    cur.execute('''
                SELECT * FROM sj
                WHERE name LIKE %s
                ''', ('%' + name + '%',))
    rs = cur.fetchall()
    if rs:
        disp(rs)
    else:
        print("검색 결과가 없습니다.")
    conn.close()
def disp(rs):
    tot = rs[0][1] + rs[0][2] + rs[0][3]
    # rs는 리스트
    # [('이영희', 75, 85, 95)]
    print(f'국어점수: {rs[0][1]} 영어점수: {rs[0][2]} 수학점수: {rs[0][3]}')
    print('이름 :', rs[0][0])
    print('총점 :', tot)

if __name__ == '__main__':
    select_a('이영희')