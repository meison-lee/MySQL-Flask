import sqlite3

def connect_to_db():
  print("try to connect to database")
  conn = sqlite3.connect('database.db')
  return conn

def insert_user(user):
    inserted_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        s = "INSERT INTO user (name, email, password, phone) VALUES('{}','{}','{}','{}')".format(user['name'], user['email'], user['password'], user['phone'])

        cur.execute(s)

        conn.commit()
        print(cur.lastrowid)
        inserted_user = get_user_by_id(cur.lastrowid)
    except:
        return {"status":0, "message":"Fail to create user", "data":inserted_user}

    finally:
        return {"status":200, "message":"Create the user successfully", "data":inserted_user}

def get_users(userId):
    user = {}
    print("in get user function")
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM user where user_id = '{}'".format(userId))
        rows = cur.fetchall()

        # convert row objects to dictionary
        user["user_id"] = rows["user_id"]
        user["name"] = rows["name"]
        user["email"] = rows["email"]
        user["password"] = rows["password"]
        user["phone"] = rows["phone"]

    except:
        user = {}

    return user


def get_user_by_id(user_id):
    user = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE user_id = '{}'".format(user_id))
        row = cur.fetchone()

        user["user_id"] = row["user_id"]
        user["name"] = row["name"]
        user["email"] = row["email"]
        user["phone"] = row["phone"]
        user["password"] = row["password"]
        print("user ", user)
    except:
        user = {}

    return user

def get_userId(name, phone):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        id = cur.execute("select user_id from users where name = '{}' AND phone = '{}'".format(name, phone))
        conn.commit()
    except:
        conn.rollback()
        id = -1
    finally:
        conn.close()
    return id

def update_user(update_user, id):
    item = {}
    try:
        print("id ", id)

        conn = connect_to_db()
        cur = conn.cursor()
        s = "update user set "
        for key in update_user:
            s += "'{}'".format(key) + " = " + "'{}'".format(update_user[key]) + ", "
        s = s[:-2]
        s += " WHERE user_id = '{}'".format(id)
        cur.execute(s)
        conn.commit()
        #return the user
        item = get_user_by_id(id)

    except:
        return {"status":0, "message":"Fail to update the user", "data":item}
    finally:
        return {"status":200, "message":"Update the user successfully", "data":item}

def check_user(information):
    user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        user = cur.execute("select * from user where email = '{}' AND password = '{}'".format(information['email'], information['password']))

        conn.commit()
        user = user.fetchall()
        print("get user from db ", user)
        #return the user

    except:
        conn.rollback()
        user = {}
    finally:
        conn.close()

    return user