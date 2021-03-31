--totallikes
SELECT userid, sum(likes) as total
INTO temp1
FROM tip
GROUP BY userid;

UPDATE users
SET totallikes = COALESCE((
	SELECT total
	FROM temp1
	WHERE temp1.userid = users.userid),0);

DROP TABLE temp1;

--tipcount
SELECT userid, count(distinct tip) as total
INTO temp1
FROM tip
GROUP BY userid;

UPDATE users
SET tipcount = COALESCE((
	SELECT total
	FROM temp1
	WHERE temp1.userid = users.userid),0);

DROP TABLE temp1;

--numCheckins
SELECT business_id, count(distinct checkins) as total
INTO temp1
FROM checkins
GROUP BY business_id;

UPDATE business
SET numcheckins = COALESCE((
	SELECT total
	FROM temp1
	WHERE temp1.business_id = business.business_id),0);

DROP TABLE temp1;

--numTips
SELECT businessid, count(distinct tip) as total
INTO temp1
FROM tip
GROUP BY businessid;

UPDATE business
SET numtips = COALESCE((
	SELECT total
	FROM temp1
	WHERE temp1.businessid = business.business_id
),0);

DROP TABLE temp1;
