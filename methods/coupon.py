import sqlite3

def connect_to_db():
  conn = sqlite3.connect('database.db')
  return conn

# seller mode method
#
def create_coupon(sellerId, coupon):
  # seller create new coupon
  try:

    conn = connect_to_db()
    cur = conn.cursor()

    s = "INSERT INTO coupon ("
    for key in coupon:
      s += key
      s += ","
    s += "sellerId) VALUES("
    for key in coupon:
      s += "'{}'".format(coupon[key])
      s += ","
    s += "'{}')".format(sellerId)
    cur.execute(s)
    conn.commit()

    print(cur.lastrowid)
    item = get_coupon_by_id(cur.lastrowid)
    print(item)

  except:
    return {"message":"fail to create a coupon", "status":"0", "data":item}
  finally:
    return {"message":"Create the Coupon Successfully", "status":"200", "data":item}

def get_seller_coupon(sellerId):
  # find all coupons one seller releases
  # find coupon in coupon database where sellerId match
  coupons = []
  try:
    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("select * from coupon where sellerId = '{}'".format(sellerId))
    rows = cur.fetchall()

    for row in rows:
      coupon = {}
      coupon['id'] = row['id']
      coupon['name'] = row['name']
      coupon['scope'] = row['scope']
      coupon['type'] = row['type']
      coupon['value'] = row['value']
      coupon['amount'] = row['amount']
      coupon['startAt'] = row['startAt']
      coupon['endAt'] = row['endAt']
      coupon['productId'] = row['productId']
      coupon['sellerId'] = row['sellerId']
      coupons.append(coupon)

    print(coupons)

  except:
    return {"message":"fail to get your coupon", "status":"0", "data":coupons}
  finally:
    return {"message":"Get All Of Your Store Coupons", "status":"200", "data":coupons}

def update_by_couponId(couponId, coupon, userId):
  # seller can only update his own coupon so we need to check if sellerId == userId
  # seller update his coupon by couponId
  item = {}
  check = check_coupon_owner(couponId, userId)
  if check['value'] == 0:
    print("you are not allow to modify this coupon!!")
    return {"status":0, "message":check['msg'], "data":item}
  try:

    conn = connect_to_db()
    cur = conn.cursor()

    s = "update coupon set "
    for key in coupon:
      s += "'{}'".format(key) + " = " + "'{}'".format(coupon[key]) + ", "
    s = s[:-2]
    s += " WHERE id = '{}'".format(couponId)

    cur.execute(s)
    conn.commit()

    item = get_coupon_by_id(couponId)
    print("item ", item)
  except:
    return {"message":"fail to update your coupon", "status":"0", "data":item}
  finally:
    return {"message":"Update your coupon successfully", "status":"200", "data":item}


# buyer mode method
#
def get_user_coupon(userId):
  # find coupon in user database where userId = userId
  coupons = []
  try:
    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("select coupon from user where user_id = '{}'".format(userId))
    coupon = cur.fetchone()[0]

    if coupon is None:
      return {"message":"you don't have any coupon", "status":"0"}

    s = "select * from coupon where id in ({})".format(coupon)
    print(s)
    cur.execute(s)
    conn.commit()
    rows = cur.fetchall()

    for row in rows:
      coupon = {}
      coupon['id'] = row['id']
      coupon['name'] = row['name']
      coupon['scope'] = row['scope']
      coupon['type'] = row['type']
      coupon['value'] = row['value']
      coupon['amount'] = row['amount']
      coupon['startAt'] = row['startAt']
      coupon['endAt'] = row['endAt']
      coupon['productId'] = row['productId']
      coupon['sellerId'] = row['sellerId']
      coupons.append(coupon)
    print(coupons)

  except:
    return {"message":"failes to get the coupon", "status":"0", "data":coupons}
  finally:
    return {"message":"Get all of your coupons successfully", "status":"200", "data":coupons}

def get_coupon(couponId, userId):
  # get a coupon 領取優惠卷
  # find the coupon by couponId
  # update user database[coupon] with userId
  try:
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("select coupon from user where user_id = '{}'".format(userId))
    coupon = cur.fetchone()[0]
    print(coupon)
    if coupon is None:
      coupon = "{}".format(couponId)
    else:

      coupon += ",{}".format(couponId)
    print("coupon arr = ", coupon)
    cur.execute("update user set coupon = '{}' where user_id = '{}'".format(coupon, userId))
    conn.commit()

  except:
    return {"message":"faile to get the coupon", "status":"0"}
  finally:
    return {"message":"Get the coupon successfully", "status":"200", "data":{"coupon":coupon}}

def update_usercoupon(couponId, userId):
  try:
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("select coupon from user where user_id = '{}'".format(userId))
    coupon = cur.fetchone()[0]
    print(coupon)
  except:
    pass


def get_coupon_by_id(coupon_id):
  coupon = {}
  try:
    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("select * from coupon where id = '{}'".format(coupon_id))
    rows = cur.fetchone()

    coupon['id'] = rows['id']
    coupon['name'] = rows['name']
    coupon['scope'] = rows['scope']
    coupon['type'] = rows['type']
    coupon['value'] = rows['value']
    coupon['amount'] = rows['amount']
    coupon['startAt'] = rows['startAt']
    coupon['endAt'] = rows['endAt']
    coupon['productId'] = rows['productId']
    coupon['sellerId'] = rows['sellerId']

    print("coupon ", coupon)

  except:
    return coupon
  finally:
    return coupon

def check_coupon_owner(coupon_id, user_id):
  try:
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("select sellerId from coupon where id = '{}'".format(coupon_id))
    id = cur.fetchone()
    print("id = ", id)

    msg = ""
    if id[0] == user_id:
      msg = "seller id match, allow to update the coupon"
      return {"value":1, "msg" : msg}
    else:
      msg = "you are not the raiser of this coupon"
      return {"value":0, "msg" : msg}
  except:
    msg = "Error during checking"
    return {"value":0, "msg":msg}