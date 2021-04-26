# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 12:55:42 2021

@author: dana.kenney
"""

import json
import psycopg2

def cleanStr4SQL(s):
    return s.replace("'","`").replace("\n"," ")

def flattenList(mylist):
    listt = mylist[1]
    lis = [(k, v) for k, v in listt.items()] #Source: https://www.geeksforgeeks.org/python-convert-dictionary-to-list-of-tuples/
    return lis

def getDict(my_dict, existing_dict):
    for k, v in my_dict.items():
        if not isinstance(v, dict):
            existing_dict[k] = v
        else:
            getDict(v, existing_dict)
    return existing_dict

def joinLists(list1, list2):
    mylist = []
    new1 = ""
    new2 = ""
    for x in list1:
        new1+= x
    for y in list2:
        new2+= y
        
    mylist.append(new1)
    mylist.append(new2)
    
    return(mylist)

def int2BoolStr (value):
    if value == 0:
        return 'False'
    else:
        return 'True'
    
#USER TABLE
def insert2UserTable():
    #reading the JSON file
    with open('./yelp_user.JSON','r') as f:    #TODO: update path for the input file
        #outfile =  open('./yelp_business_out.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        try:
            #TODO: update the database name, username, and password
            conn = psycopg2.connect("dbname='term project' user='postgres' host='localhost' password='danak2000'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            # Generate the INSERT statement for the current business
            # TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statement based on your own table schema and
            # include values for all businessTable attributes
            try:
                cur.execute("INSERT INTO users (userid, average_stars, yelping_since, username, tipcount, totallikes, fans, coolvotes, funnyvotes, usefulvotes, user_latitude, user_longitude)"
                       + " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                         (data['user_id'], data['average_stars'], cleanStr4SQL(data["yelping_since"]), cleanStr4SQL(data["name"]), 0, 0, data["fans"], data["cool"], data["funny"], data["useful"], "0", "0" ) )              
            except Exception as e:
                print("Insert to userTABLE failed!",e)
            conn.commit()

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()
        
    print(count_line)
    f.close()
 
#FRIEND TABLE
def insert2FriendTable():
    #reading the JSON file
    with open('./yelp_user.JSON','r') as f:
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        try:
            #TODO: update the database name, username, and password
            conn = psycopg2.connect("dbname='term project' user='postgres' host='localhost' password='danak2000'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            for i in data['friends']:
                try:
                    cur.execute("INSERT INTO friend (userid, friendid)"
                           + " VALUES (%s, %s)", 
                             (data['user_id'], i) )              
                except Exception as e:
                    print("Insert to friendTABLE failed!",e)
                conn.commit()

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()
    print(count_line)
    f.close()

#TIP TABLE
def insert2TipTable():
    #reading the JSON file
    with open('./yelp_tip.JSON','r') as f:    #TODO: update path for the input file
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        try:
            #TODO: update the database name, username, and password
            conn = psycopg2.connect("dbname='term project' user='postgres' host='localhost' password='danak2000'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            try:
                cur.execute("INSERT INTO tip (tipdate, tiptext, likes, userid, businessid)"
                       + " VALUES (%s, %s, %s, %s, %s)", 
                         (data['date'], cleanStr4SQL(data['text']), data["likes"], cleanStr4SQL(data["user_id"]), cleanStr4SQL(data["business_id"]) ) )             
            except Exception as e:
                print("Insert to tipTABLE failed!",e)
            conn.commit()
            # optionally you might write the INSERT statement to a file.
            # sql_str = ("INSERT INTO businessTable (business_id, name, address, state, city, zipcode, latitude, longitude, stars, numCheckins, numTips, is_open)"
            #           + " VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', {6}, {7}, {8}, {9}, {10}, {11})").format(data['business_id'],cleanStr4SQL(data["name"]), cleanStr4SQL(data["address"]), data["state"], data["city"], data["postal_code"], data["latitude"], data["longitude"], data["stars"], 0 , 0 , [False,True][data["is_open"]] )            
            # outfile.write(sql_str+'\n')

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()
    print(count_line)
    f.close()
    
def insert2BusinessTable():
    with open('yelp_business.JSON','r') as f:
        line = f.readline()
        count_line = 0
        
        try:
            conn = psycopg2.connect("dbname = 'term project' user = 'postgres' host = 'localhost' password = 'danak2000'")

        except:
            print('Unable to connect to the database!')

        cur = conn.cursor()
        while line:
            
            data = json.loads(line)
            try:
                cur.execute("INSERT INTO business (business_id, business_name, address, state, city, zipcode, latitude, longitude, stars, reviews, is_open)" + " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (data['business_id'],cleanStr4SQL(data["name"]), cleanStr4SQL(data['address']), cleanStr4SQL(data['state']), cleanStr4SQL(data['city']), cleanStr4SQL(data['postal_code']), data['latitude'], data['longitude'], data['stars'], data['review_count'], bool(data['is_open'])))   
            except Exception as e:
                print("Insert to business failed!", e)
            conn.commit()
            line = f.readline()  
        
            count_line += 1
                
                            
        cur.close()
        conn.close()
    f.close()
                            
##########################################WORKING CATEGORIES FUNCTION#################################################
def insertCategories():
    with open('yelp_business.JSON', 'r') as f:
        line = f.readline()
        count_line = 0
        try:
            #conn = psycopg2.connect("dbname = '451Project' user = 'gregpedersen' host = 'localhost' password = 'gregory99'")
            conn = psycopg2.connect("dbname = 'term project' user = 'postgres' host = 'localhost' password = 'danak2000'")

        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        
        while line:
            data = json.loads(line)
            categories = list(data['categories'].split(', '))
            for ele in range(len(categories)):        
                try:
                    cur.execute("INSERT INTO categories (category_name, business_id)" + " VALUES (%s, %s)", (cleanStr4SQL(categories[ele]), cleanStr4SQL(data['business_id']))) 
                except Exception as e:
                    print("Insert to categories failed!", e)
                #print(categories[ele], data['business_id'])
            conn.commit()    
            line = f.readline()
            count_line += 1
        
        cur.close()
        conn.close()
            
    f.close()
    

############################################Working Attribute Function#############################################

def insert2Att():
    with open('yelp_business.JSON','r')as f:
        line = f.readline()
        count_line = 0
        try:
            conn = psycopg2.connect("dbname = 'term project' user = 'postgres' host = 'localhost' password = 'danak2000'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        
        while line:
            data = json.loads(line)
            
            empty = []
            attributes = data["attributes"]
            emptyDict = {}
            
            #Use function getDict to flatten all dictionaries inside main dictionary
            update = getDict(attributes, emptyDict)
            
            #Convert dictionary to a list of different tuples
            mylist = [(k, v) for k, v in update.items()]

            for element in mylist:
                try:
                    cur.execute("INSERT INTO attributes (attr_name, value, business_id)" + " VALUES (%s, %s, %s)", (cleanStr4SQL(element[0]), cleanStr4SQL(element[1]), cleanStr4SQL(data['business_id']))) 
                except Exception as e:
                    print("Insert to att failed!", e)
            
            conn.commit()    
            line = f.readline()
            count_line += 1
            
        cur.close()
        conn.close()          
    f.close()
        
#################################################Insert Hours Function#############################################

def insert2Hours():
    with open('yelp_business.JSON','r')as f:
        line = f.readline()
        count_line = 0
        try:
            conn = psycopg2.connect("dbname = 'term project' user = 'postgres' host = 'localhost' password = 'danak2000'")
            #conn = psycopg2.connect("dbname = '451Project' user = 'gregpedersen' host = 'localhost' password = 'gregory99'")

        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        
        while line:
            data = json.loads(line)
            hours = data['hours']
            mylist = [(k, v) for k, v in hours.items()]
            for item in mylist:
                newlist = list(item[1])
                temp = newlist.index('-')
                temp1 = newlist[:temp]
                temp2 = newlist[temp:]
                temp2.pop(0)
                
                times = joinLists(temp1, temp2)
                try:
                    cur.execute("INSERT INTO hours (day_of_week, business_open, business_closed, business_id)" + " VALUES (%s, %s, %s, %s)", (item[0], times[0], times[1], cleanStr4SQL(data['business_id']))) 
                except Exception as e:
                    print("Insert to hours failed!", e)
            
            line = f.readline()
            count_line += 1
                
            
        conn.commit()   
        cur.close()
        conn.close()          
    f.close()
        
def insert2checkins():
    with open('yelp_checkin.JSON','r')as f:
        line = f.readline()
        count_line = 0
        try:
            #conn = psycopg2.connect("dbname = '451Project' user = 'gregpedersen' host = 'localhost' password = 'gregory99'")
            conn = psycopg2.connect("dbname = 'term project' user = 'postgres' host = 'localhost' password = 'danak2000'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        
            
        while line:
            data = json.loads(line)
            dates = data['date']
            split_dates = dates.split(',')
            for element in split_dates:
                new_element = element.split('-')
                new_element2 = new_element[2].split(' ')
                new_element.remove(new_element[2])
                final = new_element + new_element2
                try:
                    cur.execute("INSERT INTO checkins (checkin_year, checkin_month, checkin_day, checkin_time, business_id)" + " VALUES (%s, %s, %s, %s, %s)", (final[0], final[1], final[2], final[3], cleanStr4SQL(data['business_id']))) 
                except Exception as e:
                    print("Insert to checkins failed!", e)
           
            
            
            line = f.readline()
            count_line += 1
            
        conn.commit()
        cur.close()
        conn.close()
    f.close()
    

#insert2BusinessTable()
#insertCategories()
#insert2Att()
insert2Hours()
insert2checkins()