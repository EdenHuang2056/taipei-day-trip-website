import re
from flask import Flask
from flask import request      
from flask import redirect     
from flask import render_template  
from flask import session
from flask import url_for
from flask import jsonify
import mysql.connector
import json


app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

app.secret_key = b'\xe8s\xb9\x0e\xddZ \xc3\x80\xa5\x1a\x11\x99J\xe7V'


mydatabase = mysql.connector.connect(
    host="127.0.0.1",
    username="root",
    password="!Anctu820228",
    database="travel_site"
)

mycursor = mydatabase.cursor()


# Pages
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")

@app.route("/booking")
def booking():
	return render_template("booking.html")

@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")


@app.route("/api/user", methods = ["GET"])
def get_user_data():
	if request.method == "GET":
		if "email"in session:
			return jsonify({"data":{
				"id":session["id"],
				"name":session["name"],
				"email":session["email"]
				}
			})
		else:
			return jsonify({"data":None})    			

@app.route("/api/user", methods = ["POST"])
def create_new_user():
	mycursor.execute(f"SELECT * FROM member where email=' {request.values['email']}'")
	result = mycursor.fetchone()
	print(result)
	try:
		if result:
			return jsonify({"error":True, "message":"此信箱已被註冊過,註冊失敗"}),400
		else:
			sql = "INSERT INTO member (name, email, password) VALUES (%s, %s, %s)"
			val = (str(request.values["name"]), str(request.values["email"]), str(request.values["password"]))
			mycursor.execute(sql, val)
			mydatabase.commit()
			return jsonify({"ok":True})
	except:
		return jsonify({"error":True, "message":"伺服器內部錯誤"}),500
	
	
	# data = request.get_json()
	# print(data)
	# print(request.values["name"])
	# print(request.values['email'])
	# print(request.values['password'])

	
	
	# name = data["name"]
	# email = data["email"]
	# password = data["password"]
	# return jsonify({"error":True, "message":"此信箱已被註冊過,註冊失敗"}),400

	# try:
	# 	if name and email and password:
	# 		user = user_tb.query.filter_by(emial = email).first()
	# 		if user:
	# 			return jsonify({"error":True, "message":"此信箱已被註冊過,註冊失敗"}),400
	# 		else:
	# 			new_user = user_tb(name = data["name"], email = data["email"], password = data["password"])
	# 			db.session.add(new_user)
	# 			db.session.dommit()
	# 			return jsonify({"ok":True})
	# 	else:
	# 		return jsonify({"error":True})
	# except:
	# 	return jsonify({"error":True, "message":"伺服器內部錯誤"}),500


@app.route("/api/user", methods = ["PATCH"])
def user_signin():
	data = request.get_json()
	email = data["email"]
	password = data["password"]
	print(data)
	# print(email)
	# print(password)
	mycursor.execute(f"SELECT * FROM member where email = '{email}' and password = '{password}'")
	member_result = mycursor.fetchone()
	print(member_result)
	try:
		if member_result:
			session["id"] = member_result[0]
			session["name"] = member_result[1]
			session["email"] = member_result[2]
			print(member_result)

			return jsonify({"ok":True})
		else:
			return jsonify({"error":True})
	except:
		return jsonify({"error":True, "message":"伺服器內部錯誤"}),500


# data = request.get_json()
# 	email = data["email"]
# 	password = data["password"]

# 	try:
# 		if email and password:
#     		sql = f"select * from member where email = '{email}' and password = '{password}'"
# 			result = db.engine.execute(sql)
# 			for row in result:
#     			session["id"] = row[0]
# 				session["email"] = row[2]
# 				session["name"] = row[1]
# 				return jsonify({"ok":True})
# 		else:
#     		return jsonify({"error":True})
# 	except:
# 			return jsonify({"error":True, "message":"伺服器內部錯誤"}),500

# @app.route("/api/user", methods = ["DELETE"])
# 	def user_signout():
#     	if "email" in session:
#     		session.pop("id")
# 			session.pop("name")
# 			session.pop("email")
# 			return jsonify({"ok":True})

# @app.route("/api/user", methods = ["GET", "POST","PATCH","DELETE"])
# def get_user_data():
# 	if request.method == "GET":
# 		if "email"in session:
# 			return jsonify({"data":{
# 				"id":session["id"],
# 				"name":session["name"],
# 				"email":session["email"]
# 				}
# 			})
# 		else:
# 			return jsonify({"data":None})
# def create_new_user():
# 	if request.method == "POST":
# 		mycursor.execute(f"SELECT * FROM member where email=' {request.values['email']}'")
# 		result = mycursor.fetchone()
# 		print(result)
# 		try:
# 			if result:
# 				return jsonify({"error":True, "message":"此信箱已被註冊過,註冊失敗"}),400
# 			else:
# 				sql = "INSERT INTO member (name, email, password) VALUES (%s, %s, %s)"
# 				val = (str(request.values["name"]), str(request.values["email"]), str(request.values["password"]))
# 				mycursor.execute(sql, val)
# 				mydatabase.commit()
# 				return jsonify({"ok":True})
# 		except:
# 			return jsonify({"error":True, "message":"伺服器內部錯誤"}),500
# def user_signin():	
# 	if request.method == "PATCH":
# 		data = request.get_json()
# 		email = data["email"]
# 		password = data["password"]

# 		print(email)
# 		print(password)
# 		mycursor.execute(f"SELECT * FROM member where email = '{email}' and password = '{password}'")
# 		member_result = mycursor.fetchone()
# 		print(member_result)
# 		try:
# 			if member_result is True:
# 				session["id"] = member_result[0]
# 				session["name"] = member_result[1]
# 				session["email"] = member_result[2]
# 				return jsonify({"ok":True})
# 			else:
# 				return jsonify({"error":True})
# 		except:
# 			return jsonify({"error":True, "message":"伺服器內部錯誤"}),500

# def user_signout():
#     	if request.method == "DELETE":






@app.route("/api/attraction/<id>")
def attraction_id(id):

	mycursor.execute(f"SELECT * FROM spot where id = {id}")
	result = mycursor.fetchone()
	dic = {}

	if result is None:
		dic["data"] = {'error': 'true', 'message':'景點編號不正確'}
		
		return json.dumps(dic, ensure_ascii=False),400
	else:		
		name = result[1]
		category = result[2]
		description = result[3]
		address = result[4]
		transport = result[5]
		mrt = result[6]
		latitude = result[7]
		longitude = result[8]
		images = result[9]
		images = images.split(",")
		images.pop()
		
		dic["data"] = {'id':id, 'name':name, 'category':category, 'description':description, 'address':address, 'transport':transport, 'mrt':mrt, 'latitude':latitude, 'longitude':longitude, 'images':images}
		
		return json.dumps(dic, ensure_ascii=False),200

@app.route("/api/attractions")
def attraction_page():

	keyword = request.args.get("keyword", None)

	if keyword is None:

		page_id = request.args.get("page", None)
		page_id = int(page_id)
		page_id += 1

		dic = {}
		page_id_range = (page_id-1)*12

		mycursor.execute(f"SELECT count(*) FROM spot ")
		number = mycursor.fetchone()
		total_result = number[0]
		total_page = total_result//12
		if total_result%12 > 0:
			total_page += 1

		mycursor.execute(f"SELECT * FROM spot order by id limit 12 offset {page_id_range}")
		page_result = mycursor.fetchall()
		
		page_list = []
		for i in range(len(page_result)):
			id = page_result[i][0]
			name = page_result[i][1]
			category = page_result[i][2]
			description = page_result[i][3]
			address = page_result[i][4]
			transport = page_result[i][5]
			mrt = page_result[i][6]
			latitude = page_result[i][7]
			longitude = page_result[i][8]
			images = page_result[i][9]
			images = images.split(",")
			images.pop()
				
			detail = {'id':id, 'name':name, 'category':category, 'description':description, 'address':address, 'transport':transport, 'mrt':mrt, 'latitude':latitude, 'longitude':longitude, 'images':images}
			page_list.append(detail)

		if page_id >= (total_page):
			dic["nextPage"] = "null"
		else:
			dic["nextPage"] = (page_id)
		dic["data"] = page_list

		# return json.dumps(dic, ensure_ascii=False),200

	else:			
		page_id = request.args.get("page", None)
		page_id = int(page_id)
		page_id += 1

		dic = {}
		page_id_range = (page_id-1)*12
	
		mycursor.execute(f"SELECT count(*) FROM spot where name like '%{keyword}%' ")
		number = mycursor.fetchone()
		total_result = number[0]
		total_page = total_result//12
		if total_result%12 > 0:
			total_page += 1

		mycursor.execute(f"SELECT * FROM spot where name like '%{keyword}%' order by id limit 12 offset {page_id_range} ")
		page_result = mycursor.fetchall()

		page_list = []
		for i in range(len(page_result)):
			id = page_result[i][0]
			name = page_result[i][1]
			category = page_result[i][2]
			description = page_result[i][3]
			address = page_result[i][4]
			transport = page_result[i][5]
			mrt = page_result[i][6]
			latitude = page_result[i][7]
			longitude = page_result[i][8]
			images = page_result[i][9]
			images = images.split(",")
			images.pop()
				
			detail = {'id':id, 'name':name, 'category':category, 'description':description, 'address':address, 'transport':transport, 'mrt':mrt, 'latitude':latitude, 'longitude':longitude, 'images':images}
			page_list.append(detail)
			
		if page_id > total_page-1:
			dic["nextPage"] = "null"
		else:
			dic["nextPage"] = (page_id)
		dic["data"] = page_list

	return json.dumps(dic, ensure_ascii=False),200



# try 

# except Exception as e:
# 	print(e)

app.run(host="0.0.0.0",port=3000)