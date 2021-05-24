
import urllib.request as request
import json
import mysql.connector


def main():

    mydatabase = mysql.connector.connect(
    host = "127.0.0.1",
    username = "root",
    password = "!Anctu820228",
    database = "travel_site"
    )

    mycursor = mydatabase.cursor()


    file = "taipei-attractions.json"
    with open (file, 'r') as response:
        data = json.load(response)

    big_list = data["result"]["results"]
    # print(type(big_list))
    # print(big_list)

    # with open("data.txt", "w", encoding="utf-8") as file:

    for travel in big_list:

        id_number = travel["_id"]
        name = travel["stitle"]
        category = travel["CAT2"]
        description = travel["xbody"]
        address = travel["address"]
        transport = travel["info"]
        mrt = travel["MRT"]
        latitude = travel["latitude"]
        longitude = travel["longitude"]
        images = travel["file"]
        images = images.split("http")
        # print(images)
        website = ''
        for web in images:
            # print(type(web))
                # print(web)
                if ".jpg" in web:  
                    website = website + "http" + web + ","
                
                elif ".JPG" in web:
                    website = website + "http" + web + ","

                elif ".PNG" in web:
                    website = website + "http" + web + ","
                else:
                    pass
    

        sql = "INSERT INTO spot (id, name, category, description, address, transport, mrt, latitude, longitude, images) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (id_number, name, category, description, address, transport, mrt, latitude, longitude, website)
        mycursor.execute(sql, val)
        mydatabase.commit()


if __name__ == '__main__':
    main()