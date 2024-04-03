USE dealership_backend;

INSERT INTO Cars (VIN_carID, make, model, body, year, color, mileage, details, description, viewsOnPage, pictureLibraryLink, status, price) VALUES
('SALSF2D47CA305941', 'Ford', 'Mustang', 'Coupe', 2023, 'Orange', 35198, 'An iconic American muscle car known for its sleek design and powerful performance.', 'The Ford Mustang is a two-door sports car featuring a sleek and aerodynamic exterior design, with a powerful engine lineup ranging from fuel-efficient options to high-performance V8s, coupled with advanced technology and comfort features, making it a versatile and thrilling driving machine beloved by enthusiasts worldwide.',  7, 'https://pngimg.com/uploads/mustang/mustang_PNG15.png', 'being-watched', 81576.00),
('2G4GU5GV1D9224709', 'Ford', 'Focus', 'Hatchback', 2024, 'Blue', 6980, 'The Ford Focus is a versatile compact car renowned for its fuel efficiency, agile handling, and practical design, making it a popular choice for urban commuters and small families alike.', 'The Ford Focus is a compact car designed with a focus on efficiency and versatility, featuring a sleek exterior design complemented by a comfortable and well-equipped interior, offering ample space for passengers and cargo, while its responsive handling and range of available engines provide a dynamic driving experience suited for city streets or long highway journeys.',  1, 'https://pngimg.com/uploads/ford/ford_PNG12204.png', 'low-mileage', 65203.00),
('WAUEG94F16N011182', 'Toyota', 'RAV4', 'SUV', 2023, 'Silver', 22872, 'The Toyota RAV4 is a highly versatile compact SUV renowned for its reliability, practicality, and impressive off-road capability, making it a top choice for adventurous families and urban commuters alike.', 'The Toyota RAV4 stands as a stalwart in the compact SUV segment, boasting a sleek and modern design coupled with a spacious interior, advanced safety features, and optional all-wheel drive, making it a dependable and versatile choice for both urban and off-road adventures, while its fuel-efficient engines ensure economical journeys for drivers around the globe.',  2, 'https://alcf.s3.us-west-1.amazonaws.com/_custom/2023/toyota/rav4/2023-toyota-rav4-main.png', 'being-watched', 35955.00),
('1G4HP57M79U336833', 'Jeep', 'Compass', 'SUV', 2023, 'Green', 10615, 'The Jeep Compass is a compact SUV known for its rugged yet refined design, off-road capability, and advanced technology features, offering adventurous drivers a blend of versatility and comfort both on and off the beaten path.', 'The Jeep Compass epitomizes the brand''s heritage of adventure with its distinctive styling cues reminiscent of its larger siblings, featuring a spacious cabin outfitted with modern amenities and intuitive technology, while its capable four-wheel-drive system and terrain management options ensure confident performance whether navigating city streets or tackling challenging trails, making it a compelling choice for those seeking versatility and exploration in a compact SUV.',  9, 'https://images.dealer.com/ddc/vehicles/2023/Jeep/Compass/SUV/perspective/front-left/2023_76.png', 'being-watched', 33244.00),
('2T1KE4EEXDC541493', 'Jeep', 'Cherokee', 'SUV', 2023, 'Gray', 17798, 'The Jeep Cherokee is a rugged yet refined midsize SUV, blending off-road capability with modern comforts and technology, offering drivers a versatile vehicle suited for both urban commuting and adventurous excursions.', 'The Jeep Cherokee embodies the spirit of adventure with its iconic seven-slot grille and athletic silhouette, featuring a comfortable and well-appointed interior equipped with advanced tech amenities, while its legendary 4x4 capability, available in various trim levels, ensures confident performance across diverse terrain, making it a standout choice in the competitive midsize SUV segment.',  6, 'https://purepng.com/public/uploads/large/purepng.com-black-jeep-grand-cherokee-carcarvehicletransportjeep-9615246526987jplf.png', 'being-watched', 98131.00),
('WDDHF2EBXBA659567', 'Toyota', 'Camry', 'sedan', 2023, 'Black', 24053, 'The Toyota Camry is a reliable and fuel-efficient midsize sedan, celebrated for its spacious interior, smooth ride, and reputation for long-term durability, making it a top choice for practical-minded drivers seeking comfort and value.', 'The Toyota Camry epitomizes dependability and comfort, boasting a refined exterior design complemented by a spacious and well-appointed cabin featuring advanced technology and safety features, while its efficient yet potent engine options deliver a smooth and enjoyable driving experience, solidifying its position as a perennial favorite in the midsize sedan segment.',  4, 'https://purepng.com/public/uploads/large/purepng.com-toyotatoyotamotor-corporationautomotivemanufactureraichimultinational-1701527678522k1jrm.png', 'being-watched', 86147.00),
('WVWED7AJ7CW030690', 'Chevrolet', 'Silverado', 'SUV', 2023, 'Black', 30517, 'The Chevy Silverado is a rugged and versatile full-size pickup truck renowned for its powerful engine options, robust towing capacity, and advanced technology features, making it a trusted workhorse for demanding jobs and everyday adventures.', 'The Chevy Silverado boasts a robust frame and high-strength steel construction, providing exceptional durability and towing capability, while its range of available trim levels offers options for luxury, performance, and utility, ensuring there''s a Silverado model suited for every driver''s needs. With features like advanced trailering technology, a variety of bed and cab configurations, and a comfortable and tech-savvy interior, the Silverado seamlessly blends capability with comfort, making it a standout choice in the competitive truck market.',  4, 'https://purepng.com/public/uploads/large/purepng.com-chevrolet-silverado-colorado-black-carcarvehicletransportchevroletchevy-961524650954kotq0.png', 'being-watched', 89256.00),
('WBSBR93441E328102', 'Jeep', 'Renegade', 'SUV', 2024, 'Black', 12033, 'The Jeep Renegade is a compact SUV that combines iconic Jeep styling with nimble handling and off-road capability, making it an adventurous choice for urban explorers and outdoor enthusiasts alike.', 'The Jeep Renegade embodies the spirit of exploration with its distinctive and rugged design cues, featuring a compact yet versatile platform that excels both on city streets and off-road trails, while its spacious interior, advanced technology, and available four-wheel-drive systems ensure a comfortable and capable driving experience, solidifying its position as a standout option in the competitive compact SUV segment.',  5, 'https://purepng.com/public/uploads/large/purepng.com-black-jeep-renegade-carcarvehicletransportjeep-961524653966l65bn.png', 'being-watched', 76407.00),
('3VW517AT2FM570847', 'Chevrolet', 'Traverse', 'SUV', 2023, 'Silver', 11965, 'The Chevy Traverse is a spacious and versatile midsize SUV, offering ample seating for up to eight passengers, abundant cargo space, and a smooth ride, making it an ideal choice for families seeking comfort and utility on their journeys.', 'The Chevy Traverse stands out in the midsize SUV category with its combination of generous interior space, refined ride quality, and plethora of family-friendly features, including numerous USB ports, Wi-Fi hotspot capability, and advanced safety technology, ensuring both comfort and peace of mind on every journey, making it a compelling option for those in need of a capable and accommodating vehicle for their daily adventures.',  9, 'https://purepng.com/public/uploads/large/purepng.com-chevrolet-traversecarschevroletchevyautomobile-1701527437601gixkb.png', 'new', 94250.00),
('1G6DJ5ED0B0941154', 'Ford', 'F-150', 'SUV', 2023, 'Gray', 40650, 'The Ford F-150 is a legendary full-size pickup truck renowned for its robust performance, class-leading towing capability, and innovative features, making it a perennial favorite among truck enthusiasts and professionals alike.', 'The Ford F-150, an icon in the realm of pickup trucks, boasts a sturdy yet lightweight aluminum body, paired with a range of powerful engines, including hybrid options, delivering unparalleled towing and hauling capacities while offering a comfortable cabin equipped with cutting-edge technology and safety features, solidifying its status as the best-selling vehicle in America for decades.',  2, 'https://pictures.dealer.com/t/theherbchamberscompanies/0496/4a54066f8dd6f8e4b39af56e792401fcx.jpg', 'new', 45325.00),
('1G4HP52KX44657084', 'Chevrolet', 'Malibu', 'sedan', 2024, 'Silver', 29429, 'The Chevy Malibu is a stylish midsize sedan renowned for its fuel efficiency, spacious interior, and smooth ride, making it a popular choice for both daily commuting and long-distance travel.', 'The Chevy Malibu embodies sophistication and practicality, featuring a sleek exterior design complemented by a spacious and comfortable interior equipped with modern amenities and advanced safety features, while its efficient engine options and smooth ride quality ensure an enjoyable driving experience, making it a standout option in the competitive midsize sedan market.',  3, 'https://www.chevrolet.com/content/dam/chevrolet/na/us/english/index/vehicles/2022/cars/malibu/01-images/colorizer/2022-malibu-1lt-gan-colorizer.jpg?imwidth=1200', 'being-watched', 30995.00);


INSERT INTO Employee (firstname, lastname, email, phone, address, employeeType) VALUES
('Tabby', 'Steger', 'tsteger0@de.vu', '6354591816', '2 Thierer Junction', 'superAdmin'),
('Aleta', 'Clavering', 'aclavering1@desdev.cn', '2208706316', '62405 Merry Plaza', 'technician'),
('Patsy', 'Orchart', 'porchart2@ibm.com', '4734835137', '693 Nova Road', 'technician'),
('Blanche', 'Prophet', 'bprophet3@economist.com', '7763821407', '5173 North Terrace', 'manager'),
('Theda', 'Draper', 'tdraper4@devhub.com', '7041746513', '66 Superior Alley', 'manager'),
('Rafferty', 'Frostdicke', 'rfrostdicke5@ucoz.com', '9805076681', '8 Delladonna Parkway', 'technician'),
('Roi', 'Lamzed', 'rlamzed6@vimeo.com', '8846875214', '5 Sunbrook Plaza', 'manager'),
('Avigdor', 'Mizzi', 'amizzi7@mtv.com', '6554398772', '41326 Hanover Point', 'manager'),
('Glori', 'Cox', 'gcox8@timesonline.co.uk', '9495623767', '6 Dexter Crossing', 'technician'),
('Florenza', 'Schoffel', 'fschoffel9@hud.gov', '2779866316', '84196 Village Green Place', 'technician'),
('Rodie', 'Woollends', 'rwoollendsa@woothemes.com', '9713949393', '44653 Maywood Hill', 'manager'),
('Nikki', 'Craise', 'ncraiseb@smh.com.au', '7595756390', '58946 Drewry Place', 'manager'),
('Delinda', 'Dey', 'ddeyc@ca.gov', '8581258708', '4862 Brickson Park Park', 'technician'),
('Earvin', 'Tregiddo', 'etregiddod@wisc.edu', '2206199554', '03675 Schiller Crossing', 'manager'),
('Licha', 'Abelovitz', 'labelovitze@telegraph.co.uk', '6237294660', '2594 Johnson Plaza', 'manager'),
('Rhett', 'Pawson', 'rpawsonf@t.co', '2434620716', '24632 Elka Parkway', 'technician'),
('Edythe', 'Clementet', 'eclementetg@japanpost.jp', '8435574441', '33222 Crownhardt Terrace', 'technician'),
('Nickie', 'Cuchey', 'ncucheyh@histats.com', '4895517826', '7 Elmside Center', 'manager'),
('Maryanne', 'Wressell', 'mwresselli@shareasale.com', '3963082365', '0 Lotheville Alley', 'manager'),
('Torrence', 'Kibblewhite', 'tkibblewhitej@msn.com', '8928541469', '94556 Hudson Pass', 'technician');


INSERT INTO EmployeeSensitiveInfo (employeeID, password, SSN, driverID, lastModified) VALUES
(1, 'on9vlvku', '$2a$04$W4n2hVTiRg53O9hnTis05uoiRXYptdPU/Fc1xSISvo.MRugD/y88S', 'I96670745983742', '2023-08-06 14:41:01'),
(2, 'ovkkysxn', '$2a$04$siXWpEC1Fi.ijJYH1rpuhO9ipiVwf6cgZdKVDyJYIpPTmB5TuYv1K', 'G23005417297863', '2023-04-08 01:25:21'),
(3, 'p4r0xd5j', '$2a$04$z/qIqAAvhHQ4p695s2m6WuBka.n7oiPFJymYz2zxAxxSQ7vgVh0Dq', 'F25356251439825', '2023-10-15 13:50:22'),
(4, 'kg8b4mrc', '$2a$04$lSXhsSToAunz.Mh19118ne0rkwhD3anhE.Fn6o5Hj.ZRy8ZqjBdva', 'U25064328606142', '2023-10-06 20:13:10'),
(5, 'vye4sn7e', '$2a$04$j8XsPoJAxMwQwX3xDfUnauvHAUwVf.9EN1mmnIDss.8piTp7DHHFa', 'C75881620476833', '2024-03-02 02:57:59'),
(6, 'x5i9gq7k', '$2a$04$fhxamBlGoBufqR3IR856ley9iMaieOkvmj0yh4yrtWOvVY/gPQdJW', 'L45026077556480', '2023-11-16 07:04:38'),
(7, 'k9naqhub', '$2a$04$/4s1GNzme2jjlKbe7O4Miufo61uNVD68gWwLbe/MqTwz1OH5p2uQC', 'V19237356992642', '2023-10-23 07:45:01'),
(8, '4ommnq52', '$2a$04$GkGR6m1OLS3i4zv9dL3w1u6d0l/iOHfMdOPET4/.u3BraIuwLed8a', 'P87226193493909', '2023-06-12 13:41:35'),
(9, 'g2k3u560', '$2a$04$9qLpb2AiRYr6Smrm3TB7dOnRdXF4tfABNnNY/pvy1ea1XfXHu9aLC', 'N56834854481057', '2023-12-19 03:41:34'),
(10, '0aw4dgvg', '$2a$04$lqIckzkRsW3xiai2aRj9FOE27XF3OXVaf.X1M8C4EzKmGOy4X1CmK', 'J87895470258351', '2023-02-03 19:55:06'),
(11, '00fbhmg6', '$2a$04$lLic1DjOedWWnW6FQaiZceQ8jq9OfIBDDe7RPa4qgJ3aqStW6n4mG', 'M90526830311912', '2023-11-04 07:54:15'),
(12, '1e7g31zt', '$2a$04$YlB23oTjCLPI.OY7FDOIou9BA95QrEKA/AE6vKVfkhw31Fo3oe7c2', 'N60004229422223', '2023-09-24 18:12:18'),
(13, 'anwcnvvh', '$2a$04$Hv.LEo8S4BtXzJ6baMruG.zFJIEZJQ8tk1rsXaKYF8SWAgwYeiIIq', 'E73725928843550', '2024-02-15 15:37:33'),
(14, '6g8k0mlr', '$2a$04$S9c0aFQxfKyG3QaH0yr7reV9Ha5CibtI2fwvS1CpLQQhQMRLIroO6', 'U82548510742695', '2023-12-06 04:22:33'),
(15, 'b86w4tog', '$2a$04$kx4mTJoGOZUmoiukIFXbDeH5nDvoHrGFW4.N/9yQF001FhinoGzjW', 'W55496494796644', '2023-02-10 12:50:11'),
(16, '9lie9281', '$2a$04$kDOkz7muQc.mmZxr/WA2Uuz3BBRCMCx2/RbDfVaNWF2/TPYxKjy5y', 'Z11226785662506', '2023-08-20 15:37:39'),
(17, 'ow7a9gcs', '$2a$04$f99z/DJv0Bg9PT1Ld2GaTuTd.3zNZ4QWNZuWCJZ7ScuSnTARI5BAe', 'N87778191930551', '2023-04-07 22:12:22'),
(18, '07xw1cnt', '$2a$04$q/DJZBPuJzvl/N/JGLjzcO8G6ln1ulQithpCKd13LJB8GN4hI1HIW', 'R36578819583636', '2023-11-14 13:31:26'),
(19, 'k20bhxcr', '$2a$04$0VTDoNzeyrk/42Y3kLMVHOnRwOGaSEGkHTfWeQFpBLrcMOiJMbPiG', 'A17046949140707', '2023-04-08 23:03:48'),
(20, 'uveu9bt5', '$2a$04$4Yfo/KdXCgWL97VNF5R./eakmCS8zvGloJJEAJc3iUjJgXtd8Mdxu', 'P84486181854073', '2023-06-06 12:56:11');


INSERT INTO Member (first_name, last_name, email, phone, join_date) VALUES
('John', 'Doe', 'john.doe@example.com', '1234567890', '2024-04-02 15:00:00'),
('Alice', 'Smith', 'alice.smith@example.com', '2345678901', '2024-03-02 11:00:00'),
('Bob', 'Johnson', 'bob.johnson@example.com', '3456789012',  '2024-03-03 12:00:00'),
('Emma', 'Brown', 'emma.brown@example.com', '4567890123', '2024-03-03 13:00:00'),
('Michael', 'Davis', 'michael.davis@example.com', '5678901234', '2024-04-03 14:00:00'),
('Sarah', 'Wilson', 'sarah.wilson@example.com', '6789012345', '2024-04-05 15:00:00'),
('David', 'Martinez', 'david.martinez@example.com', '7890123456', '2024-04-02 16:00:00'),
('Michelle', 'Lopez', 'michelle.lopez@example.com', '8901234567', '2024-04-04 17:00:00'),
('James', 'Taylor', 'james.taylor@example.com', '9012345678', '2024-04-02 18:00:00'),
('Emma', 'Garcia', 'emma.garcia@example.com', '0123456789', '2024-04-02 19:00:00'),
('PLACEHOLDER', 'PLACEHOLDER', 'PLACEHOLDER@example.com', '0000000000', NOW()); -- bids has a placeholder for memberID for customers that buy without bidding, this is meant as a placeholder for customer who do not BID ONLY to be referenced in the BID table


INSERT INTO MemberSensitiveInfo (memberID, SSN, username, password, driverID, lastModified) VALUES
(1,'$2a$04$/p41ed.VM6XMUQUPatQeC.rbt32KlkZXTbJdbTOTPZfEwL6iQNLiO', 'kscinelli0','gi2z9nka','R22313811699913', '2023-01-11 07:54:39'),
(2,'$2a$04$8MsZMk.Gg.M568tLmYG5euCqyDIOBzoCO2PXNlifKcn.iUBQnELkK','jtheyer1','x37eefm6','X95512680606098', '2023-03-14 19:10:16'),
(3,'$2a$04$Nu1AGJhKxzvcnbJJstAZyuVTW2yxmL76xgrY6wv0OdltKCjCqJtkS','rtrahair2','vkhbwl1u','D08707674135194', '2023-08-31 15:46:47'),
(4,'$2a$04$klLi7xerdp4EsAUjg54BL.JbpB9AyOR3wDH/TV6f08iioqPaEVBHK','ggoold3','nawl8b8t','C16041684227955', '2024-02-29 22:48:44'),
(5,'$2a$04$wUm4A8tsXYmZ5PU3zgxMduz.Jtud7QTugW8uo6BL1sdehTXYmZ4V6','hkordas4','a4xjo2w6','K40404256713626','2023-06-08 21:02:47'),
(6,'$2a$04$PtC4Nfmh6NXRShKs75AYVetR02NIbRRECgtAiQjKqZp53C/yKoLTu','jcressingham5','957xnaoj','R95125829361332', '2023-01-27 01:55:00'),
(7,'$2a$04$2bozKetHmKLUG80Qh4eWy.OqI2Eq2p4EQK1Psy9IzIlEgfscN5DnC','gmcguffog6','6kue0cr8','C99938545187865', '2023-06-26 10:14:37'),
(8,'$2a$04$rzqdu619jHkvPjsvytEEvuHb6XTJvBARusNtU/JpQLgAUUcmHN0ES','mcurthoys7','ph759onj','T53807275459626', '2023-01-07 13:34:23'),
(9,'$2a$04$TWARPHI6IG8IeL8AJaDDxuY5.10DyGcOoWlW0FcYNK2uIItf6J242','lroff8','64stqnqd','P93000133288498', '2023-11-28 03:16:19'),
(10,'$2a$04$cQHQtF2/gb3BZWBRz05cU.XAbbn.8l4q/5pm705EERJU5UdJ29A8G','dbaszniak9','430m5kn5','F98941422570001', '2023-01-03 12:55:47');


INSERT INTO Financing (memberID, income, credit_score, loan_total, down_payment, percentage, monthly_sum, remaining_months) VALUES
(1, 50000, 700, 40000, 10000, 10, 1000, 36),
(2, 60000, 720, 45000, 12000, 10, 1100, 24),
(3, 45000, 680, 25000, 8000, 15, 950, 35),
(4, 55000, 710, 42000, 11000, 10, 1050, 36),
(5, 48000, 690, 38000, 9000, 15, 1050, 24);


INSERT INTO Payments (paymentStatus, valuePaid, valueToPay, initialPurchase, lastPayment, paymentType, cardNumber, expirationDate, CVV, routingNumber, bankAcctNumber, memberID, financingID)
VALUES
('Completed', '10000', '40000', '2024-01-15 10:00:00', '2024-02-15 10:00:00', 'Card', '1234567890123456', '12/26', '123', NULL, NULL, 1, 1),
('Pending', '8000', '25000', '2024-02-20 10:00:00', '2024-02-20 10:00:00', 'Check/Bank Account', NULL, NULL, NULL, '123456789', '9876543210987654321', 3, 3),
('Completed', '11000', '42000', '2024-01-10 10:00:00', '2024-01-20 10:00:00', 'Card', '9876543210987654', '11/25', '456', NULL, NULL, 4, 4),
('Completed', '12000', '45000', '2024-02-05 10:00:00', '2024-03-05 10:00:00', 'None', NULL, NULL, NULL, NULL, NULL, 2, 2),
('Pending', '9000', '38000', '2024-03-01 10:00:00', '2024-03-01 10:00:00', 'Check/Bank Account', NULL, NULL, NULL, '987654321', '1234567890123456789', 5, 5);


INSERT INTO Bids (memberID, bidValue, bidStatus, bidTimestamp) VALUES
(6, 30000.00, 'Confirmed', '2024-03-15 10:30:00'),
(9, 19000.00, 'Confirmed', '2024-03-16 11:45:00'),
(8, 25000.00, 'Processing', '2024-03-19 15:00:00'),
(11, 0.00, 'None', NOW()); -- Placeholder bid table for vehicles bought at MSRP or finance without bidding.


INSERT INTO Purchases (bidID, VIN_carID, memberID, confirmationNumber) VALUES
(1, 'SALSF2D47CA305941', 1, 'DIWMINQZFK6I2'),
(NULL, '2T1KE4EEXDC541493', 4, 'HGSEX99HT5EXF'),
(NULL, '3VW517AT2FM570847', 4, 'UB5MJLYEXL0MN'),
(4, 'WAUEG94F16N011182', 2, 'Q68XX5VHXQWO8'),
(NULL, '1G4HP52KX44657084', 5, '1OGNT9EEW8JVA');


INSERT INTO TestDrive (memberID, VIN_carID, appointment_date, confirmation) VALUES
(2, '1G6DJ5ED0B0941154', '2024-04-03 10:00:00', 'Confirmed'),
(5, '2G4GU5GV1D9224709', '2024-04-04 11:00:00', 'Awaiting Confirmation'),
(3, 'WBSBR93441E328102', '2024-04-05 12:00:00', 'Denied'),
(4, '1G6DJ5ED0B0941154', '2024-04-06 13:00:00', 'Cancelled'),
(9, '1G4HP52KX44657084', '2024-04-07 14:00:00', 'Confirmed');


INSERT INTO ServiceAppointment (memberID, appointment_date, service_name) VALUES
(1, '2024-04-10', 'Oil Change'),
(2, '2024-04-11', 'Brake Inspection'),
(3, '2024-04-12', 'Tire Rotation'),
(4, '2024-04-13', 'Battery Replacement');


INSERT INTO Addons (itemName, totalCost) VALUES
('Extended Warranty', 1500.00),
('Maintenance Plans', 800.00),
('GAP Insurance', 400.00),
('Paint Protection Film/Ceramic Coating', 1200.00),
('Wheel and Tire Protection', 800.00),
('Interior Protection Packages', 500.00),
('Security Systems', 300.00),
('Navigation Systems', 1000.00),
('Towing Packages', 1000.00),
('Entertainment Systems', 800.00);
