import sqlite3

def connect_to_db():
  print("try to connect to database")
  conn = sqlite3.connect('database.db')
  return conn

def strToArr(str):
  try:
    arr = str.split(',')
  except:
    arr = [str]
  return arr

def arrToStr(arr):
  return ",".join(str(x) for x in arr)

def get_color_byId(colorId):
  print("in func")
  print("color id = ", colorId)
  conn = connect_to_db()
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  cur.execute("select * from color where id in ({})".format(arrToStr(colorId)))
  rows = cur.fetchall()

  colors = []
  for row in rows:
    color = {}
    color['id'] = row['id']
    color['name'] = row['name']
    colors.append(color)


  return colors

def get_size_byId(sizeId):
  print("in func")
  print("size id = ", arrToStr(sizeId))
  conn = connect_to_db()
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  cur.execute("select * from size where id in ({})".format(arrToStr(sizeId)))
  rows = cur.fetchall()

  sizes = []
  for row in rows:
    size = {}
    size['id'] = row['id']
    size['name'] = row['name']
    sizes.append(size)

  return sizes

def get_inventories(id):
  conn = connect_to_db()
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  print("inventory id = ", id)
  cur.execute("select * from inventories where id in ({})".format(arrToStr(id)))
  rows = cur.fetchall()

  inventories = []
  for row in rows:
    inventory = {}
    inventory['color'] = get_color_byId(strToArr(row['colorId']))
    inventory['size'] = get_size_byId(strToArr(row['sizeId']))
    inventory['inventory'] = row['inventory']
    inventories.append(inventory)

  print("inventories ", inventories)
  return inventories