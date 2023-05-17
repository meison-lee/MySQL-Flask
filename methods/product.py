import sqlite3
from .method import *

def connect_to_db():
  print("try to connect to database")
  conn = sqlite3.connect('database.db')
  return conn

def create_product(product, sellerId):
    inserted_product = {}
    try:
        conn = connect_to_db()
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        # get the colorId array
        colors = []
        for i in product['colors']:
            print(i)
            exist = cur.execute("select * from color where name = '{}'".format(i))
            exist = exist.fetchone()
            if exist is not None:
                colors.append(exist[0])
                # color_id = exist[0]
            else:
                s = "INSERT INTO color (name) VALUES('{}')".format(i)
                cur.execute(s)
                conn.commit()
                temp = cur.execute("select * from color where id = '{}'".format(cur.lastrowid))
                temp = temp.fetchone()
                colors.append(temp[0])
        print("color id = ", colors)


        # get the size id array
        sizes = []
        for i in product['sizes']:
            print(i)
            exist = cur.execute("select * from size where name = '{}'".format(i))
            exist = exist.fetchone()
            if exist is not None:
                sizes.append(exist[0])
                # color_id = exist[0]
            else:
                s = "INSERT INTO size (name) VALUES('{}')".format(i)
                cur.execute(s)
                conn.commit()
                temp = cur.execute("select * from size where id = '{}'".format(cur.lastrowid))
                temp = temp.fetchone()
                sizes.append(temp[0])
        print("size id = ", sizes)

        # find different combination of color and size
        # and store them to iventories database
        inventory = []
        for i in colors:
            for j in sizes:
                cur.execute("INSERT INTO inventories (colorId, sizeId, inventory) VALUES ('{}' ,'{}', '{}')".format(i, j, 1))
                conn.commit()
                inventory.append(cur.lastrowid)

        print("inventory ", inventory)
        cur.execute("INSERT INTO products (name, description, picture, colors, sizes, price, available, inventories, startAt, endAt, sellerId) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(product['name'],product['description'],product['picture'],arrToStr(colors) ,arrToStr(sizes) ,product['price'],product['available'],arrToStr(inventory),product['startAt'],product['endAt'],sellerId))

        conn.commit()
        print("color id = ", colors)
        print("color id = ", sizes)
        print("color id = ", inventory)
        inserted_product = get_product_by_productId(cur.lastrowid)
        inserted_product['colors'] = get_color_byId(colors)
        inserted_product['sizes'] = get_size_byId(sizes)
        inserted_product['inventories'] = get_inventories(inventory)

    except:
        return {"status":200, "message":"Fail to create the products ", "data":inserted_product}
    finally:
        return {"status":200, "message":"Create the products successfully", "data":inserted_product}

def get_user_product(user):
    products = []
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        sellerId = user[0][0]
        # find name = username and get the products
        pass
    except:
        products = []
    return products

def get_product_by_sellerId(sellerId):
    products = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        print("seller id = ", sellerId)
        cur.execute("select * from products where sellerId = {}".format(sellerId))
        rows = cur.fetchall()
        print(rows)
        print("get all")

        for i in rows:
            product = {}
            product["product_id"] = i["product_id"]
            product["name"] = i["name"]
            product["description"] = i["description"]
            product["picture"] = i["picture"]
            product["colors"] = get_color_byId(strToArr(i["colors"]))
            product["sizes"] = get_size_byId(strToArr(i["sizes"]))
            product["price"] = i["price"]
            product["available"] = i["available"]
            product["startAt"] = i["startAt"]
            product["endAt"] = i["endAt"]
            product["sellerId"] = i["sellerId"]
            product["inventories"] = get_inventories(strToArr(i['inventories']))
            products.append(product)
        print(products)
    except:
        return {"status":0, "message":"Fail to get your products ", "data":products}
    finally:
        return {"status":200, "message":"Get your products successfully", "data":products}

def get_product_by_productId(productId):
    product = {}
    try:

        # find productId = productId in product database
        print("get product by product id")
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("select * from products where product_id = {}".format(productId))
        row = cur.fetchone()

        print("clor ", row["product_id"])
        product["product_id"] = row["product_id"]
        product["name"] = row["name"]
        product["description"] = row["description"]
        product["picture"] = row["picture"]
        product["colors"] = get_color_byId(strToArr(row["colors"]))
        product["sizes"] = get_size_byId(strToArr(row["sizes"]))
        product["price"] = row["price"]
        product["available"] = row["available"]
        product["startAt"] = row["startAt"]
        product["endAt"] = row["endAt"]
        product["sellerId"] = row["sellerId"]
        product["inventories"] = get_inventories(strToArr(row['inventories']))

        print("product ", product)
    except:
        product = {}
    return product

def update_product_by_productId(productId, update_product, user_id):
    product = {}
    if get_product_by_productId(productId)["sellerId"] != user_id:
        print("you are not the creator of the product")
        return {"status":0, "message":"Don't have permission to update the product", "data":product}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("UPDATE products SET available = '{}' WHERE product_id = '{}'".format(update_product['available'], productId))
        conn.commit()

        product = get_product_by_productId(productId)
    except:
        return {"status":0, "message":"Fail to update the product", "data":product}
    finally:
        return {"status":200, "message":"Update the product available successfully", "data":product}


def update_productInventory_by_productId(productId, update_inventory):
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        inventory_id = cur.execute("select inventories from products where product_id = '{}'".format(productId))
        inventory_id = inventory_id.fetchone()[0]


        for i in update_inventory:
            print(i)
            color_id = i['colorId']
            size_id = i['sizeId']
            inventory = i['inventory']

            cur.execute("select id from inventories where colorId = ? AND sizeId = ?",(color_id, size_id))
            for id in cur.fetchall():
                print(id[0])
                for i  in strToArr(inventory_id):
                    if int(i) == id[0]:
                        target_id = int(i)
                        break

            cur.execute("UPDATE inventories SET inventory = ? where id = ?", (inventory, target_id))
            conn.commit()

        product = get_product_by_productId(productId)
        print(product)


    except:
        return {"message":"failes to update the inventories", "status":"0", "data":product}
    finally:
        return {"message":"Update the inventories successfully", "status":"200", "data":product}
