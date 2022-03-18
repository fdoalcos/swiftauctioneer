-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.
--Littering took place at 16:36. No known witnesses.
SELECT description FROM crime_scene_reports WHERE year = 2021 OR month = 7 OR day = 28 OR street = "Humphrey Street";

-- Ruth | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, 
--you might want to look for cars that left the parking lot in that time frame.

--Eugene | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, 
--I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.

--Raymond | As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say
--that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.

--Emma | I'm the bakery owner, and someone came in, suspiciously whispering into a phone for about half an hour. They never bought anything.
SELECT name, transcript FROM interviews WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE "%bakery%"; 

--(130) 555-0289 | (996) 555-8899
--(499) 555-9472 | (892) 555-8872
--(367) 555-5533 | (375) 555-8161
--(499) 555-9472 | (717) 555-1342
--(286) 555-6063 | (676) 555-6554
--(770) 555-1861 | (725) 555-3243
--(031) 555-6622 | (910) 555-3251
--(826) 555-1652 | (066) 555-9701
--(338) 555-6650 | (704) 555-2131

SELECT caller, receiver FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;

--id | account_number | year | month | day | atm_location | transaction_type | amount
--246 | 28500762 | 2021 | 7 | 28 | Leggett Street | withdraw | 48
--264 | 28296815 | 2021 | 7 | 28 | Leggett Street | withdraw | 20
--266 | 76054385 | 2021 | 7 | 28 | Leggett Street | withdraw | 60
--267 | 49610011 | 2021 | 7 | 28 | Leggett Street | withdraw | 50
--269 | 16153065 | 2021 | 7 | 28 | Leggett Street | withdraw | 80
--288 | 25506511 | 2021 | 7 | 28 | Leggett Street | withdraw | 20
--313 | 81061156 | 2021 | 7 | 28 | Leggett Street | withdraw | 30
--336 | 26013199 | 2021 | 7 | 28 | Leggett Street | withdraw | 35
SELECT * FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw";

--5P2BI95
FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 9 AND minute >= 15;

--id | origin_airport_id | destination_airport_id | year | month | day | hour | minute
--36 | 8 | 4 | 2021 | 7 | 29 | 8 | 20
sqlite> SELECT * FROM flights WHERE month = 7 AND day = 29 AND year = 2021 ORDER BY hour;

--to know what number theyre going
SELECT destination_airport_id FROM flights, airports
WHERE airports.id = destination_airport_id
AND city LIKE "%New York City%";

--7214083635
--1695452385
--5773159633
--1540955065
--8294398571
--1988161715
--9878712108
--8496433585
ELECT passport_number, seat FROM passengers, flights
WHERE passengers.flight_id = flights.id
AND origin_airport_id = 8 AND destination_airport_id = 4 AND year = 2021 AND month = 7 AND day = 29
AND hour = 8 AND minute = 20;