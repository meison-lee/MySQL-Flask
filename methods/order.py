import sqlite3
import datetime
from .activity import *
from .coupon import *
from .product import *

def connect_to_db():
  conn = sqlite3.connect('database.db')
  return conn


def get_buyers_order(userId):
  orders = []
  try:
    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    print("user id = ", userId)
    cur.execute("select * from orders where buyerId = '{}'".format(userId))
    rows = cur.fetchall()

    for row in rows:
      order = {}
      order['id'] = row['id']
      order['items'] = get_item_information(row['items'])
      order['totalPrice'] = row['totalPrice']
      order['status'] = row['status']
      order['sellerId'] = row['sellerId']
      order['buyerId'] = row['buyerId']
      order['createAt'] = row['createAt']
      order['updateAt'] = row['updateAt']
      order['CouponUsed'] = row['CouponUsed']
      orders.append(order)

    print("order ", orders)

  except:
    return {"status":0, "message":"Fail to get the order !!", "data":orders}

  return {"status":200, "message":"get the order successfully!!", "data":orders}

def post_order(userId, order):

  item = {}
  try:

    activity = get_activity_by_id(order['activityId'])
    coupon = get_coupon_by_id(order['couponId'])

    print(activity, coupon)

    if check_if_user_have_coupon(coupon, userId) == 0:
      raise ValueError("You don't have the coupon")

    print("you have the coupon")

    products = []
    amounts = []
    colors =[]
    sizes = []
    for i in order['items']:
      # check inventory and available
      if check_inventory(i) and check_available(i['productId']):
        get_product = get_product_by_productId(i['productId'])
        colors.append(i['color'])
        sizes.append(i['size'])
        amounts.append(i['amount'])
        products.append(get_product)
      else:
        print("\ninventory problem\n")
        raise ValueError('No enough inventory for you !!')

    # check if products come from same store(seller)
    result = check_product_same_seller(products)

    if result['check'] == 0:
      raise ValueError("You can only buy products in one store in each order !!")

    sellerId = result['id']
    price = result['price']
    product_ids = result['product_ids']

    print("seller id ", sellerId)
    for i in range(len(price)):
      price[i] *= amounts[i]

    print("price ", price)
    print("all product id ", product_ids)

    # calculate price after activity
    cur = 0
    if activity:
      activity_arr = strToArr(activity['productId'])
      print("arr = ",activity_arr)
      for product in products:
        if str(product['product_id']) in activity_arr:
          if activity['type'] == 'MINUS':
            price[cur] -= int(activity['value'])
          elif activity['type'] == 'MULTIPLY':
            price[cur] *= int(activity['value'])
        cur += 1
    print("price ", price)
    print("amount ", amounts)

    # calculate price after coupon
    cur = 0
    if coupon:
      coupon_arr = strToArr(coupon['productId'])
      print("arr = ",coupon_arr)
      for product in products:
        print("in here ", product['product_id'])
        if str(product['product_id']) in coupon_arr:
          if coupon['type'] == 'MINUS':
            price[cur] -= int(coupon['value'])
          elif coupon['type'] == 'MULTIPLY':
            print(coupon['value'])
            price[cur] *= float(coupon['value'])
        cur += 1
    print("price ", price)

    totalPrice = sum(price)
    print("total = ", totalPrice)

    conn = connect_to_db()
    cur = conn.cursor()

    # create items database
    cur.execute("INSERT INTO items (productId, color, size, amount) VALUES ('{}', '{}', '{}', '{}')".format(arrToStr(product_ids), arrToStr(colors), arrToStr(sizes), arrToStr(amounts)))
    conn.commit()
    item_id = cur.lastrowid
    conn.close()
    print("item id ", item_id)

    conn = connect_to_db()
    cur = conn.cursor()
    # create orders database
    ct = datetime.datetime.now().date()
    cur.execute("insert into orders (items, totalPrice, status, sellerId, buyerId, createAt, updateAt, CouponUsed) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(item_id, totalPrice, "checking", sellerId, userId, ct, ct, coupon['id']))
    conn.commit()
    order_id = cur.lastrowid



    item = get_order_by_orderId(order_id)
    item['items'] = get_item_information(item_id)

  except ValueError as err:
    print(err.args)
    return {"status":0, "message":err.args, "data":item}

  return {"status":200, "message":"Create order successfully !!!", "data":item}

def seller_orders(sellerId):
  orders = []
  try:
    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("select * from orders where sellerId = '{}'".format(sellerId))
    rows = cur.fetchall()

    for row in rows:
      order = {}
      order['id'] = row['id']
      order['items'] = get_item_information(row['items'])
      order['totalPrice'] = row['totalPrice']
      order['status'] = row['status']
      order['sellerId'] = row['sellerId']
      order['buyerId'] = row['buyerId']
      order['createAt'] = row['createAt']
      order['updateAt'] = row['updateAt']
      order['CouponUsed'] = row['CouponUsed']
      orders.append(order)

    print("order ", orders)

  except:
    return {"status":0, "message":"Fail to get the order !!", "data":orders}

  return {"status":200, "message":"get the order successfully!!", "data":orders}

def get_order_by_orderId(orderId):
  order = {}
  try:
    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("select * from orders where id = '{}'".format(orderId))

    row = cur.fetchone()
    order["id"] = row["id"]
    order["items"] = row["items"]
    order["totalPrice"] = row["totalPrice"]
    order["status"] = row["status"]
    order["sellerId"] = row["sellerId"]
    order["buyerId"] = row["buyerId"]
    order["createAt"] = row["createAt"]
    order["updateAt"] = row["updateAt"]
    order["CouponUsed"] = row["CouponUsed"]

    print("order \n", order)
  except:
    return order

  return order


def update_order_by_orderId(orderId, update_item):
  try:
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("update orders set status = '{}' where id = '{}'".format(update_item['status'], orderId))
    conn.commit()

    item = get_order_by_orderId(orderId)
    print("item ", item)
  except:
    return {"message":"fail to update your coupon", "status":"0", "data":item}

  return {"message":"Update your coupon successfully", "status":"200", "data":item}

def check_if_user_have_coupon(coupon, userId):
  try:
    check = 0
    couponId = coupon['id']

    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("select coupon from user where user_id = '{}'".format(userId))
    coupon = cur.fetchone()[0]
    coupon = strToArr(coupon)
    print("arr coupon = ", coupon)

    if str(couponId) in coupon:
      check = 1

  except:
    pass
  finally:
    return check

def check_inventory(item):
  # find inventory by productId and size and color
  # then check if the inventory is enough
  check = 0
  try:
    conn = connect_to_db()
    cur = conn.cursor()

    print("product id ", item['productId'])
    inventory_id = cur.execute("select inventories from products where product_id = '{}'".format(item['productId']))
    inventory_id = inventory_id.fetchone()[0]

    color_id = cur.execute("select id from color where name = '{}'".format(item['color']))
    color_id = cur.fetchone()[0]

    size_id = cur.execute("select id from size where name = '{}'".format(item['size']))
    size_id = cur.fetchone()[0]

    print(color_id, size_id)

    cur.execute("select id from inventories where colorId = ? AND sizeId = ?",(color_id, size_id))

    for id in cur.fetchall():
      print(id[0])
      for i  in strToArr(inventory_id):
        print(id[0])
        if int(i) == id[0]:
          check = 1
          break

  except:
    pass

  return check

def check_available(id):

  product = get_product_by_productId(id)
  if product['available'] == 'True':
    return 1
  else:
    return 0

def check_product_same_seller(products):
  id = -1
  check = 1
  price = []
  product_id = []
  for i in products:
    price.append(i['price'])
    product_id.append(i['product_id'])
    if id == -1:
      id = i['sellerId']
      continue
    if id != i['sellerId']:
      check = 0
  return {"check":check, "id":id, "price":price, "product_ids":product_id}

def get_item_information(item_id):
  try:
    print("get information", item_id)

    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("select * from items where id = '{}'".format(item_id))
    row = cur.fetchone()

    product_id = row['productId']
    product_id = strToArr(product_id)
    products = []
    for i in product_id:
      product = get_product_by_productId(i)
      products.append(product)

    color = row['color']
    color = strToArr(color)

    size = row['size']
    size = strToArr(size)

    amount = row['amount']
    amount = strToArr(amount)

    print(product_id, color, size, amount)

    items = []
    cur = 0
    products, color, size, amount
    for product in products:
      # print("prodcut ", product)
      item = {}
      item['productId'] = product['product_id']
      item['name'] = product['name']
      item['description'] = product['description']
      item['picture'] = product['picture']
      item['price'] = product['price']
      item['color'] = color[cur]
      item['size'] = size[cur]
      item['amount'] = amount[cur]
      cur += 1
      items.append(item)
  except:
    pass
  return items