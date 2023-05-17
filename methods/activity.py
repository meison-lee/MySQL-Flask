import sqlite3
from .product import *

def connect_to_db():
  conn = sqlite3.connect('database.db')
  return conn

def create_activity(sellerId, activity):
  # insert new activity to the table
  # with sellerId and activity infromation
  try:

    conn = connect_to_db()
    cur = conn.cursor()

    # product_arr = []
    # if activity['scope'] == "STORE":
    #   for product in get_product_by_sellerId(sellerId):
    #     product_arr.append(product['product_id'])
    # else:
    #   product_arr.append(activity[''])

    s = "INSERT INTO activity ("
    for key in activity:
      s += key
      s += ","
    s += "sellerId) VALUES("
    for key in activity:
      s += "'{}'".format(activity[key])
      s += ","
    s += "'{}')".format(sellerId)
    cur.execute(s)
    conn.commit()

    print(cur.lastrowid)
    item = get_activity_by_id(cur.lastrowid)
    print(item)

  except:
    return {"message":"Fail to Create your Activities ", "status":"0", "data":item}
  finally:
    return {"message":"Create your Activities successfully", "status":"200", "data":item}

def get_activity(sellerId):
  #return array of activities
  activities = []
  try:
    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("select * from activity where sellerId = '{}'".format(sellerId))
    rows = cur.fetchall()

    for row in rows:
      activity = {}
      activity['name'] = row['name']
      activity['scope'] = row['scope']
      activity['type'] = row['type']
      activity['value'] = row['value']
      activity['available'] = row['available']
      activity['startAt'] = row['startAt']
      activity['endAt'] = row['endAt']
      activity['productId'] = row['productId']
      activity['sellerId'] = row['sellerId']
      activities.append(activity)
  except:
    return {"message":"fail to get seller's activities", "status":"0", "data":activities}
  finally:
    return {"message":"Get seller's Activities", "status":"200", "data":activities}

def update_by_activityId(activityId, activity):
  try:
    print("activity = ", activity)
    conn = connect_to_db()
    cur = conn.cursor()

    s = "update activity set "
    for key in activity:
      s += "'{}'".format(key) + " = " + "'{}'".format(activity[key]) + ", "
    s = s[:-2]
    s += " WHERE id = '{}'".format(activityId)

    cur.execute(s)
    conn.commit()

    item = get_activity_by_id(activityId)
    print(item)

  except:
    return {"message":"fail to update the activity", "status":"0", "data":item}
  finally:
    return {"message":"Update activity by it id", "status":"200", "data":item}

def get_activity_by_id(id):
  activity = {}
  try:
    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM activity where id = '{}'".format(id))
    rows = cur.fetchone()

    activity['id'] = rows['id']
    activity['name'] = rows['name']
    activity['scope'] = rows['scope']
    activity['type'] = rows['type']
    activity['value'] = rows['value']
    activity['available'] = rows['available']
    activity['startAt'] = rows['startAt']
    activity['endAt'] = rows['endAt']
    activity['productId'] = rows['productId']
    activity['sellerId'] = rows['sellerId']

    # print("activity ", activity)

  except:
    return activity
  finally:
    return activity


def check_activity_owner(activity_id, seller_id):
  try:
    conn = connect_to_db()
    cur = conn.cursor()
    id = cur.execute("select sellerId from activity where id = '{}'".format(activity_id))
    id = id.fetchone()

    msg = ""
    print("\n{}\n".format(id[0]))
    if id[0] == seller_id:
      msg = "seller id match, allow to update the activities"
      return {"value":1, "msg" : msg}
    else:
      msg = "you are not the raiser of this activity"
      return {"value":0, "msg" : msg}
  except:
    msg = "Error during checking"
    return {"value":0, "msg" : msg}