import mysql.connector as connection

mydb = connection.connect(
  host="localhost",
  user="root",
   #auth_plugin='mysql_native_password',
  password="welcome",
  database="item"
)

mycursor = mydb.cursor()

def insert_item(item):
    sql = "INSERT INTO item (name, value,date) VALUES ('{}', 1,curdate()) ON DUPLICATE KEY UPDATE value=value+1".format(str(item))
    mycursor.execute(sql)
    mydb.commit()
    
def insert_bank(bank):
    sql = "INSERT INTO bank (name, value,date) VALUES ('{}', 1,curdate()) ON DUPLICATE KEY UPDATE value=value+1".format(str(bank))
    mycursor.execute(sql)
    mydb.commit()

def get_high():
    sql = "SELECT name FROM item WHERE value >=  ALL (SELECT value FROM item);"                                                                            
    mycursor.execute(sql)
    x=mycursor.fetchall()
    return x

def insert_user(un,pwd):
    sql="insert into user(email,password) values ('{}','{}')".format(str(un),str(pwd))
    mycursor.execute(sql)
    mydb.commit()
    
def check_user(un,pwd):
    sql="select password from user where email='{}'".format(str(un))
    mycursor.execute(sql)
    result=mycursor.fetchone()
    if pwd in result:
        return True
    else :
        return False
    mydb.commit()
    


