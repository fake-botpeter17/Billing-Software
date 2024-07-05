CREATE TABLE users (
    uid varchar(60) PRIMARY KEY,
    designation VARCHAR(80),
    hashed_pwd VARCHAR(150),
    salt VARCHAR(100),
    name VARCHAR(50)
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50),
    cp INTEGER,
    qnty INTEGER,
    added INTEGER,
    sp INTEGER
);

CREATE TABLE bills (
    bill_no INTEGER PRIMARY KEY,
    bill_date VARCHAR(50),
    bill_amount INTEGER,
    billed_by VARCHAR(40)
);


INSERT INTO public.bills VALUES (10001, '24 May, 2024', 650, 'Nelson');
INSERT INTO public.bills VALUES (10002, '24 May, 2024', 3250, 'Nelson');
INSERT INTO public.items VALUES (1011, 'Girls Western Set', 445, 5, 476, 650);
INSERT INTO public.items VALUES (1012, 'SGT W Cotton Shirt - FS', 350, 55, 375, 499);
INSERT INTO public.items VALUES (1013, 'SGT W Cotton Shirt - HS', 350, 18, 375, 499);
INSERT INTO public.items VALUES (1014, 'White Cotton Vesti', 125, 10, 134, 225);
INSERT INTO public.items VALUES (1015, 'Lehenga', 455, 16, 487, 850);
INSERT INTO public.items VALUES (1016, 'Lehenga', 1075, 1, 1150, 1900);
INSERT INTO public.items VALUES (1017, 'Lungi', 125, 17, 134, 199);
INSERT INTO public.items VALUES (1018, 'Ladies - Jeans', 270, 6, 289, 625);
INSERT INTO public.items VALUES (1019, 'Ladies - Jean', 390, 6, 417, 750);
INSERT INTO public.items VALUES (1020, 'White Top', 830, 3, 888, 1250);
INSERT INTO public.items VALUES (1021, 'Premium Top', 351, 10, 376, 725);
INSERT INTO public.items VALUES (1022, 'School Bag', 220, 10, 235, 425);
INSERT INTO public.items VALUES (1024, 'Mens - T Shirt', 140, 23, 150, 349);
INSERT INTO public.items VALUES (1023, 'Ramraj Towel', 100, 10, 107, 140);
INSERT INTO public.items VALUES (1025, 'Night-Wear Set - Ladies', 335, 5, 358, 499);
INSERT INTO public.items VALUES (1026, 'Gents - Jeans', 420, 4, 449, 1100);
INSERT INTO public.items VALUES (1027, 'Gents - Jeans', 320, 2, 342, 690);
INSERT INTO public.items VALUES (1028, 'Gents - Jeans', 320, 1, 342, 650);
INSERT INTO public.items VALUES (1029, 'Gents - Jeans', 320, 3, 342, 675);
INSERT INTO public.items VALUES (1030, 'Gents - Jeans', 420, 4, 449, 875);
INSERT INTO public.items VALUES (1031, 'Gents - Jeans', 320, 1, 342, 690);
INSERT INTO public.items VALUES (1032, 'Pant-Shirt Material', 149, 11, 159, 299);
INSERT INTO public.users VALUES ('Nelson', 'Admin', 'b''$2b$12$xw7sfXL6XPNZ4fFOd4Mfvu7D6tAZtLECOUwsqsxdwIRFoz0jdJ2NS''', 'cJw-k6TbPQU2q8AvWWN8j1rl24qyZYDhgC4Q4kQRWPw', 'Nelson C');
INSERT INTO public.users VALUES ('Employee', 'Staff', 'b''$2b$12$WnnDjLu9d5b66paderniLeJSoWf/Dh9H0KlcHZ503Xms6UvW.H3YO''', 'gmKBUbHrAzeZClYABAGTQA69AT3gJGZDm9VAOO5QI68', 'Someone');
INSERT INTO public.users VALUES ('q', 'Python Developer', 'b''$2b$12$XJ1GGCbkIROMAY.3U8dzSeuxKkqQ3H44ijK.1JmlmzC5fvqEWa2.G''', 'XcXGWAICsSRCvjuZDRsZiSlCTkvwzW9NGOkIyqbXATE', 'Peter');