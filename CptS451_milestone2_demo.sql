
--GLOSSARY
--table names
business
users
tip
friend
checkins
categories
attributes
hours

--some attribute names
zipcode
business_id
city  (business city)
business_name   (business name)
userid
friendid
numtips
numcheckins

userid
tipcount  (user)
totallikes (user)

tipdate
tiptext
likes  (tip)

checkin_year
checkin_month
checkin_day
checkin_time


--1.
SELECT COUNT(*) 
FROM  business;
SELECT COUNT(*) 
FROM  users;
SELECT COUNT(*) 
FROM  tip;
SELECT COUNT(*) 
FROM  friend;
SELECT COUNT(*) 
FROM  checkins;
SELECT COUNT(*) 
FROM  categories;
SELECT COUNT(*) 
FROM  attributes;
SELECT COUNT(*) 
FROM  hours;



--2. Run the following queries on your business table, checkins table and review table. Make sure to change the attribute names based on your schema. 

SELECT zipcode, COUNT(distinct C.category_name)
FROM business as B, categories as C
WHERE B.business_id = C.business_id
GROUP BY zipcode
HAVING count(distinct C.category_name)>300
ORDER BY zipcode;

SELECT zipcode, COUNT(distinct A.attr_name)
FROM business as B, attributes as A
WHERE B.business_id = A.business_id
GROUP BY zipcode
HAVING count(distinct A.attr_name) = 30;

SELECT users.userid, count(friendid)
FROM users, friend
WHERE users.userid = friend.userid AND 
      users.userid = 'NxtYkOpXHSy7LWRKJf3z0w'
GROUP BY users.userid;


--3. Run the following queries on your business table, checkins table and tips table. Make sure to change the attribute names based on your schema. 


SELECT business_id, business_name, city, numtips, numcheckins
FROM business 
WHERE business_id ='K8M3OeFCcAnxuxtTc0BQrQ';

SELECT userid, username, tipcount, totallikes
FROM users
WHERE userid = 'NxtYkOpXHSy7LWRKJf3z0w';

-----------

SELECT COUNT(*) 
FROM checkins
WHERE business_id ='K8M3OeFCcAnxuxtTc0BQrQ';

SELECT count(*)
FROM tip
WHERE  businessid = 'K8M3OeFCcAnxuxtTc0BQrQ';


--4. 
--Type the following statements. Make sure to change the attribute names based on your schema. 

SELECT business_id,business_name, city, numcheckins, numtips
FROM business 
WHERE business_id ='hDD6-yk1yuuRIvfdtHsISg';

INSERT INTO checkins (business_id, checkin_year,checkin_month, checkin_day,checkin_time)
VALUES ('hDD6-yk1yuuRIvfdtHsISg','2021','04','02','15:00');


--5.
--Type the following statements. Make sure to change the attribute names based on your schema.  

SELECT business_id,business_name, city, numcheckins, numtips
FROM business 
WHERE business_id ='hDD6-yk1yuuRIvfdtHsISg';

SELECT userid, username, tipcount, totallikes
FROM users
WHERE userid = '3z1EttCePzDn9OZbudD5VA';


INSERT INTO tip (userid, businessid, tipdate, tiptext,likes)  
VALUES ('3z1EttCePzDn9OZbudD5VA','hDD6-yk1yuuRIvfdtHsISg', '2021-04-02 13:00','EVERYTHING IS AWESOME',0);

UPDATE tip 
SET likes = likes+1
WHERE userid = '3z1EttCePzDn9OZbudD5VA' AND 
      businessid = 'hDD6-yk1yuuRIvfdtHsISg' AND 
      tipdate ='2021-04-02 13:00';
      