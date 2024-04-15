import json
import psycopg2
def establish_connection():
    try: 
        conn = psycopg2.connect("dbname='Milestone2DB' user='postgres' host='localhost' password='password'")
    except:
        print('Unable  to connect to database!')
    return conn

def executeQuery(sql_str, conn):
    cur.execute(sql_str)
    conn.commit()
    return None

def close_connection(conn):
    cur.close()
    conn.close()
    return None

def cleanStr4SQL(s):
    return s.replace("'","''").replace("\n"," ")

def getAttributes(attributes):
    L = []
    for (attribute, value) in list(attributes.items()):
        if isinstance(value, dict):
            L += getAttributes(value)
        else:
            L.append((attribute,value))
    return L

def parseBusinessData(conn):
    print("Parsing businesses...")
    #read the JSON file
    with open('dont_push\Yelp-CptS451\yelp_business.JSON','r') as f:
        outfile =  open('dont_push\Yelp-CptS451\yelp_business.txt', 'w')
        line = f.readline()
        count_line = 0
        #read each JSON abject and extract data
        while line:
            data = json.loads(line)
            business = data['business_id'] #business id
            business_str =  "'" + cleanStr4SQL(data['name']) + "'," + \
                            "'" + cleanStr4SQL(data['neighborhood']) + "'," + \
                            "'" + cleanStr4SQL(data['address']) + "'," + \
                            "'" + cleanStr4SQL(data['city']) + "'," +  \
                            "'" + data['state'] + "'," + \
                            "'" + data['postal_code'] + "'," +  \
                            str(data['latitude']) + "," +  \
                            str(data['longitude']) + "," + \
                            "0, 0.0, " + \
                            str(data['stars']) + "," + \
                            str(data['review_count']) + "," + \
                            str(data['is_open'])
            outfile.write(business_str + '\n')

            sql_str = "INSERT INTO Business VALUES ('" + data['business_id'] +  "', " + business_str + ")" 
            executeQuery(sql_str, conn)

            for category in data['categories']:
                category_str = "'" + business + "','" + cleanStr4SQL(category) + "'"
                outfile.write(category_str + '\n')
                sql_str = "INSERT INTO Categories VALUES (" + category_str + ")"
                executeQuery(sql_str, conn)

            # process business hours
            for (day,hours) in data['hours'].items():
                hours_str = "'" + business + "','" + str(day) + "','" + str(hours.split('-')[0]) + "','" + str(hours.split('-')[1]) + "'"
                outfile.write( hours_str +'\n')
                sql_str = "INSERT INTO Hours VALUES (" + hours_str + ")"
                executeQuery(sql_str, conn)

            #process business attributes
            for (attr,value) in getAttributes(data['attributes']):
                attr_str = "'" + business + "','" + str(attr) + "','" + str(value)  + "'"
                outfile.write(attr_str +'\n')
                sql_str = "INSERT INTO Attribute VALUES (" + attr_str + ")"
                executeQuery(sql_str, conn)

            line = f.readline()
            count_line +=1
    print(count_line)
    outfile.close()
    f.close()


def parseReviewData(conn):
    print("Parsing reviews...")
    #reading the JSON file
    with open('dont_push\Yelp-CptS451\yelp_review.JSON','r') as f:
        outfile =  open('dont_push\Yelp-CptS451\yelp_review.txt', 'w')
        line = f.readline()
        count_line = 0
        failed_inserts = 0
        while line:
            data = json.loads(line)
            review_str = "'" + data['review_id'] + "'," +  \
                         "'" + data['user_id'] + "'," + \
                         "'" + data['business_id'] + "'," + \
                         "'" + data['date'] + "'," + \
                         str(data['stars']) + "," + \
                         "'" + cleanStr4SQL(data['text']) + "'," +  \
                         str(data['useful']) + "," +  \
                         str(data['funny']) + "," + \
                         str(data['cool'])
            outfile.write(review_str +'\n')
            line = f.readline()
            count_line +=1
            sql_str = "INSERT INTO Reviews VALUES (" + review_str + ")"
            executeQuery(sql_str, conn)

    print(count_line)
    outfile.close()
    f.close()

def parseUserData(conn):
    print("Parsing users...")
    # reading the JSON file
    with open('dont_push\Yelp-CptS451\yelp_user.JSON','r') as f:
        outfile =  open('dont_push\Yelp-CptS451\yelp_user.txt', 'w')
        outfile2 = open('dont_push\Yelp-CptS451\yelp_friend.txt', 'w')
        line = f.readline()
        count_line = 0
        while line:
            data = json.loads(line)
            user_id = data['user_id']
            user_str = \
                      "'" + user_id + "'," + \
                        str(data["average_stars"]) + "," + \
                        str(data['compliment_cool']) + "," + \
                        str(data['compliment_cute']) + "," + \
                        str(data['compliment_funny']) + "," + \
                        str(data['compliment_hot']) + "," + \
                        str(data['compliment_list']) + "," + \
                        str(data['compliment_more']) + "," + \
                        str(data['compliment_note']) + "," + \
                        str(data['compliment_photos']) + "," + \
                        str(data['compliment_plain']) + "," + \
                        str(data['compliment_profile']) + "," + \
                        str(data['compliment_writer']) + "," + \
                        str(data["cool"]) + "," + \
                        str(data["fans"]) + "," + \
                        str(data["funny"]) + "," + \
                        "'" + cleanStr4SQL(data["name"]) + "'," + \
                        str(data["review_count"]) + "," + \
                        str(data["useful"]) + "," + \
                        "'" + cleanStr4SQL(data["yelping_since"]) + "'"
            outfile.write(user_str+"\n")
            sql_str = "INSERT INTO Users VALUES (" + user_str + ")"
            executeQuery(sql_str, conn)
            
            for friend in data["friends"]:
                friend_str = "'" + user_id + "'" + "," + "'" + friend + "'"
                outfile2.write("INSERT INTO Friends VALUES (" + friend_str + ")\n")


            for value in data["elite"]:
                elite_str = "'" + user_id + "'" + ", '" + str(value) + "'\n"
                outfile.write(elite_str)
                elite_sql = "INSERT INTO Elite VALUES (" + elite_str + ")"
                executeQuery(elite_sql, conn)
            line = f.readline()
            count_line +=1

    print(count_line)
    outfile.close()
    outfile2.close()
    f.close()
    with open('dont_push\Yelp-CptS451\yelp_friend.txt','r') as f:
        line = f.readline()
        while line:
            executeQuery(line, conn)
            line = f.readline()
    f.close()

def parseCheckinData(conn):
    print("Parsing checkins...")
    #reading the JSON file
    with open('dont_push\Yelp-CptS451\yelp_checkin.JSON','r') as f:  # Assumes that the data files are available in the current directory. If not, you should set the path for the yelp data files.
        outfile = open('dont_push\Yelp-CptS451\yelp_checkin.txt', 'w')
        line = f.readline()
        count_line = 0
        #read each JSON abject and extract data
        while line:
            data = json.loads(line)
            business_id = data['business_id']
            for (dayofweek,time) in data['time'].items():
                for (hour,count) in time.items():
                    checkin_str = "'" + business_id + "',"  \
                                  "'" + dayofweek + "'," + \
                                  "'" + hour + "'," + \
                                  str(count)
                    outfile.write(checkin_str + "\n")
                    sql_str = "INSERT INTO Checkin VALUES (" + checkin_str + ")"
                    executeQuery(sql_str, conn)
            line = f.readline()
            count_line +=1
    print(count_line)
    outfile.close()
    f.close()

conn = establish_connection()
cur = conn.cursor()
parseBusinessData(conn)
parseUserData(conn)
parseCheckinData(conn)
parseReviewData(conn)
close_connection(conn)

