# pip install mysql-connector -> mysql-connector-2.2.9.tar.gz (11.9 MB)
import mysql.connector # mysql 모듈 import

# pydb에 접속하기 위한 정보를 생성.
config={'user':'root',      
         'password':'4577',
         'host':'127.0.0.1',
         'database':'test',
         'port':'3306'}

def get_Conn():             # config 딕셔어리를 connect메서드의 인자로 넣는다 생성 된 커넥션을 리턴.
    conn = mysql.connector.connect(**config)
    return conn 