-- Keep a log of any SQL queries you execute as you solve the mystery.

.tables

.schema

SELECT description FROM crime_scene_reports
WHERE year = 2020 AND month = 7 AND day = 28;

--Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse.
--Interviews were conducted today with three witnesses who were present at the time
--each of their interview transcripts mentions the courthouse.

SELECT name, transcript FROM interviews
WHERE year = 2020 AND month = 7 AND day = 28;

-- Ruth | Sometime within ten minutes of the theft, I saw the thief get into a car
-- in the courthouse parking lot and drive away. If you have security footage from
-- the courthouse parking lot, you might want to look for cars that left the parking
-- lot in that time frame.


-- Eugene | I don't know the thief's name, but it was someone I recognized. Earlier
-- this morning, before I arrived at the courthouse, I was walking by the ATM on Fifer
-- Street and saw the thief there withdrawing some money.

-- Raymond | As the thief was leaving the courthouse, they called someone who talked to
-- them for less than a minute. In the call, I heard the thief say that they were planning
-- to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person
-- on the other end of the phone to purchase the flight ticket.

SELECT activity, license_plate, minute FROM courthouse_security_logs
WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10;

SELECT name FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
WHERE bank_accounts.account_number IN
(SELECT account_number FROM atm_transactions
WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street");


SELECT destination_airport_id, hour, minute FROM flights
WHERE origin_airport_id IN
(SELECT id FROM airports
WHERE city = "Fiftyville")
AND year = 2020 AND month = 7 AND day = 29
ORDER BY 2;

destination_airport_id | hour | minute
london 4 | 8 | 20
chicago 1 | 9 | 30
san franciso 11 | 12 | 15
tokyo 9 | 15 | 20
boston 6 | 16 | 0

SELECT name, phone_calls.receiver FROM phone_calls
JOIN people ON phone_calls.caller = people.phone_number
WHERE year = 2020 AND month = 7 AND day = 28 AND duration <= 60;

SELECT name, people.license_plate, courthouse_security_logs.minute, courthouse_security_logs.activity FROM people
JOIN courthouse_security_logs ON people.license_plate = courthouse_security_logs.license_plate
WHERE people.license_plate IN
(SELECT license_plate FROM courthouse_security_logs
WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND activity = "exit")
AND courthouse_security_logs.activity = "exit"
ORDER BY 3;



SELECT * FROM airports;

SELECT people.name FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
WHERE bank_accounts.account_number = (SELECT account_number FROM atm_transactions
WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street");
--Danielle

SELECT * FROM people WHERE name = "Danielle";

--id | name | phone_number | passport_number | license_plate
--467400 | Danielle | (389) 555-5198 | 8496433585 | 4328GD8

SELECT passport_number from people
WHERE name = "Danielle"
INTERSECT
SELECT passport_number FROM passengers
WHERE flight_id IN
(SELECT id FROM flights
WHERE origin_airport_id IN
(SELECT id FROM airports
WHERE city = "Fiftyville")
AND year = 2020 AND month = 7 AND day = 29);

SELECT destination_airport_id FROM flights
JOIN passengers ON passengers.flight_id = flights.id
WHERE passport_number = "8496433585" AND year = 2020 AND month = 7 AND day = 29;

SELECT * FROM phone_calls
WHERE receiver = "(389) 555-5198" AND year = 2020 AND month = 7 AND day = 28;
