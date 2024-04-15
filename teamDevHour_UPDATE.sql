UPDATE Business
SET numCheckins = (
    SELECT SUM(count)
    FROM Checkin
    WHERE Checkin.business_id = Business.business_id
    GROUP BY Checkin.business_id
);

UPDATE Business
SET numCheckins = 0
WHERE numCheckins IS NULL;

UPDATE Business
SET review_count = count 
FROM   (SELECT business_id, COUNT(*)
		FROM Reviews
		GROUP BY business_id) AS Review
WHERE Review.business_id = Business.business_id

UPDATE Business
SET reviewrating = avg 
FROM    (SELECT business_id, AVG(stars)
         FROM Reviews
         GROUP BY business_id) AS Review
WHERE Review.business_id = Business.business_id