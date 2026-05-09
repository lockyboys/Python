def abc(*con):
    print(type(con))
    for i in con:
        print(i, end =" ")

abc(1,2,3,4,5)
def abc(**con):
    print(type(con))
    for i,j in con.items():
        print(i, j, end ="  ")

abc(a=1,b=2,c=3,d=4,e=5)