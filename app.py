from flask import Flask
from flask import request      
from flask import redirect     
from flask import render_template  
from flask import session
from flask import url_for
import mysql.connector
import json


app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

app.secret_key = b'\xe8s\xb9\x0e\xddZ \xc3\x80\xa5\x1a\x11\x99J\xe7V'


mydb = mysql.connector.connect(
    host="127.0.0.1",
    username="root",
    password="!nctu820228",
    database="travel_site"
)

mycursor = mydb.cursor()


# Pages
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/api/attractions/")
def attraction_page():

	keyword = request.args.get("keyword", None)
	print(keyword)
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

		if page_id >= (total_page-1):
			dic["nextPage"] = "null"
		else:
			dic["nextPage"] = (page_id)
		dic["data"] = page_list

		return json.dumps(dic, ensure_ascii=False),200

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
				
			detail = {'id':id, 'name':name, 'category':category, 'description':description, 'address':address, 'transport':transport, 'mar':mrt, 'latitude':latitude, 'longitude':longitude, 'images':images}
			page_list.append(detail)
			
		if page_id > total_page-1:
			dic["nextPage"] = "null"
		else:
			dic["nextPage"] = (page_id)
		dic["data"] = page_list

		return json.dumps(dic, ensure_ascii=False),200

@app.route("/api/attractions/<id>")
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
		
		dic["data"] = {'id':id, 'name':name, 'category':category, 'description':description, 'address':address, 'transport':transport, 'mar':mrt, 'latitude':latitude, 'longitude':longitude, 'images':images}
		return json.dumps(dic, ensure_ascii=False),200



	# return render_template("attraction.html")


@app.route("/booking")
def booking():
	return render_template("booking.html")


@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

app.run(port=3000)