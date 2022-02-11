from peewee import *


#DataBase connection
conn = SqliteDatabase('data.db')

class BaseModel(Model):
    class Meta:
        database = conn 

# Определяем модель пользователя
class User(BaseModel):
    user_id = AutoField(column_name='userid')
    username = TextField(column_name='username')
    age = TextField(column_name='age')
    sphere = TextField(column_name='sphere')
    date = TextField(column_name='lastnewsupdate')


    class Meta:
        table_name = 'users'

cursor = conn.cursor()



def create_user(user_username, user_age, preferences):
    User.create(username = user_username, age = user_age, sphere = preferences)

def check_user(user_username):
    try:
        sphere = User.get(User.username == user_username)
        return True
    except:
        return False

def get_sphere(user_username):
    sphere = User.get(User.username == user_username)
    return sphere.sphere

def update_date(user_username, user_date):
    user = User(username=user_username)
    user.date = user_date
    user.save()

def get_date(user_username):
    date = User.get(User.username == user_username)
    return date.date



conn.close()