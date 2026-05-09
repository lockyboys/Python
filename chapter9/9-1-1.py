def get_Conn(**con):
    print(type(con))
    for i,j in con.items():
        print(i, j)

config={'user':'root',
         'password':'123456',
         'host':'127.0.0.1',
         'port':'3306'}

get_Conn(**config)

