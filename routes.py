from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
import json
from functools import wraps
from methods.user import *
from methods.product import *
from methods.activity import *
from methods.coupon import *
from methods.order import *
from methods.method import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

jwtM = JWTManager()
# 設定 JWT 密鑰
app.config['JWT_SECRET_KEY'] = "dkla;kdelfkaxcd"
jwtM.init_app(app)



# Route of User
#
#
#
@app.route('/users',  methods = ['POST'])
def api_add_user():
  data =  request.get_data().decode()
  user = json.loads(data)
  return jsonify(insert_user(user))

@app.route('/users/me', methods=['GET', 'PATCH'])
@jwt_required(optional=False)
def users_me():
  # get user by id
  if (request.method == 'GET'):
    id = get_jwt_identity()
    user = get_user_by_id(id)
    if user:
      return jsonify({"status":0, "message":"get me !", "data":user})
    else:
      return jsonify({'status':1, "message":"error! didn't find user"})
  # update user by id with information
  elif(request.method == 'PATCH'):
    data = request.get_data().decode()
    information = json.loads(data)
    return jsonify(update_user(information, get_jwt_identity()))


@app.route('/users/<user_id>', methods=['GET'])
@jwt_required(optional=False)
def api_get_user(user_id):
  user = get_user_by_id(user_id)
  if user:
    return jsonify({"status":0, "message":"get user by id !", "data":user})
  else:
    return jsonify({'status':1, "message":"error! didn't get user"})

@app.route('/users/signIn', methods=['POST'])
def signIn():
  data = request.get_data().decode()
  information = json.loads(data)
  user = check_user(information)
  print(user)
  if user is not None:
    id = user[0][0]
    access_token = create_access_token(identity=id)
    return jsonify({"status":0, "message":"sign in successfully", "data":{"id":id, "token":access_token}})
  else:
    return jsonify({"status":404, "message":"Error ! Sign in fail !"})


# Route of Product
#
#
#
#
@app.route('/sellers/me/products', methods=['POST', 'GET'])
@jwt_required(optional=False)
def create_seller_product():
  if request.method == 'POST':
    data =  request.get_data().decode()
    product = json.loads(data)
    return jsonify(create_product(product, get_jwt_identity()))
  elif request.method == 'GET':
    return jsonify(get_product_by_sellerId(get_jwt_identity()))


@app.route('/sellers/<sellerId>/products', methods=['GET'])
def get_seller_product_withId(sellerId):
  return jsonify(get_product_by_sellerId(sellerId))

@app.route('/products/<productId>', methods=['GET'])
def get_product_withId(productId):
  product = get_product_by_productId(productId)
  if product:
    return jsonify({"message":"Get product successfully !","status":200 , "data":product})
  else:
    return jsonify({"message":"Fail to get product !","status":0 , "data":product})

@app.route('/products/<productId>', methods=['PATCH'])
@jwt_required(optional=False)
def update_product_withId(productId):
  data =  request.get_data().decode()
  product = json.loads(data)
  return jsonify(update_product_by_productId(productId, product, get_jwt_identity()))

@app.route('/products/<productId>/inventories', methods=['PATCH'])
def update_product_inventory(productId):
  data = request.get_data().decode()
  inventory = json.loads(data)
  # inventory is a 2d array
  return jsonify(update_productInventory_by_productId(productId, inventory))



# Route of Activity
#
#
# if scope is specific product
# creater should send the product id
@app.route('/sellers/me/activities', methods=['POST', 'GET'])
@jwt_required(optional=False)
def me_activity():
  if request.method == 'POST':

    data =  request.get_data().decode()
    activity = json.loads(data)

    return jsonify(create_activity(get_jwt_identity(), activity))

  elif request.method == 'GET':

    return jsonify(get_activity(get_jwt_identity()))

@app.route('/sellers/<sellerId>/activities', methods=['GET'])
def get_activities_byId(sellerId):
  return jsonify(get_activity(sellerId))

@app.route('/activities/<activityId>', methods=['PATCH'])
@jwt_required(optional=False)
def get_by_activityId(activityId):
  check = check_activity_owner(activityId, get_jwt_identity())

  if check['value'] == 0:
    return jsonify({"message":"Error ! {}".format(check["msg"]), "status":0})
  data =  request.get_data().decode()
  activity = json.loads(data)
  return jsonify(update_by_activityId(activityId, activity))


# Route of Coupon
#
#
# if scope is specific product
# creater should send the product id
@app.route('/sellers/me/coupons', methods=['POST', 'GET'])
@jwt_required(optional=False)
def seller_me_coupon():
  if request.method == 'POST':
    # create an coupon
    id = get_jwt_identity()
    data =  request.get_data().decode()
    coupon = json.loads(data)
    return jsonify(create_coupon(id, coupon))
  elif request.method == 'GET':
    # get all of my coupon
    return jsonify(get_seller_coupon(get_jwt_identity()))

@app.route('/sellers/<sellerId>/coupons', methods=['GET'])
def get_coupon_byId(sellerId):
  return jsonify(get_seller_coupon(sellerId))

@app.route('/coupons/<couponId>', methods=['PATCH'])
@jwt_required(optional=False)
def update_coupon(couponId):
  data =  request.get_data().decode()
  coupon = json.loads(data)
  return update_by_couponId(couponId, coupon, get_jwt_identity())

@app.route('/buyers/me/coupons', methods=['GET'])
@jwt_required(optional=False)
def buyer_me_coupon():
    # get all of my coupon
    return jsonify(get_user_coupon(get_jwt_identity()))

@app.route('/buyers/me/coupons/<couponId>', methods=['POST'])
@jwt_required(optional=False)
def get_one_coupon(couponId):
  return jsonify(get_coupon(couponId, get_jwt_identity()))


# Route of order
#
#
#
@app.route('/buyers/me/orders', methods=['POST', 'GET'])
@jwt_required(optional=False)
def buyers_order():
  if request.method == 'GET':
    return jsonify(get_buyers_order(get_jwt_identity()))
  elif request.method == 'POST':
    # order a product 下單
    data =  request.get_data().decode()
    order = json.loads(data)
    return jsonify(post_order(get_jwt_identity(), order))

@app.route('/sellers/me/orders', methods=['GET'])
@jwt_required(optional=False)
def seller_order():
  # 看賣出了多少件衣服
  return jsonify(seller_orders(get_jwt_identity()))

@app.route('/orders/<orderId>', methods=['GET', 'PATCH'])
@jwt_required(optional=False)
def by_orderId(orderId):
  if request.method == 'GET':
    return jsonify(get_order_by_orderId(orderId))
  elif request.method == 'PATCH':
    # update the order state, seller side
    data =  request.get_data().decode()
    order = json.loads(data)
    return jsonify(update_order_by_orderId(orderId, order))

if __name__ == "__main__":
    #app.debug = True
    app.run(host='0.0.0.0', port=3000, debug=True)
    print("connect to server")