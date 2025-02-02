USE dealership_backend;

INSERT INTO Member (first_name, last_name, email, phone, address, city, state, zipcode, join_date) VALUES
('John', 'Doe', 'john.doe@example.com', '1234567890', '123 Main St', 'Los Angeles', 'CA', '12345', '2024-04-02 15:00:00'),
('Alice', 'Smith', 'alice.smith@example.com', '2345678901', '456 Elm St', 'New York City', 'NY', '23456', '2024-03-02 11:00:00'),
('Bob', 'Johnson', 'bob.johnson@example.com', '3456789012', '789 Oak St', 'Houston', 'TX', '34567', '2024-03-03 12:00:00'),
('Emma', 'Brown', 'emma.brown@example.com', '4567890123', '101 Pine St', 'Miami', 'FL', '45678', '2024-03-03 13:00:00'),
('Michael', 'Davis', 'michael.davis@example.com', '5678901234', '202 Elm St', 'San Francisco', 'CA', '56789', '2024-04-03 14:00:00'),
('Sarah', 'Wilson', 'sarah.wilson@example.com', '6789012345', '303 Maple St', 'Buffalo', 'NY', '67890', '2024-04-05 15:00:00'),
('David', 'Martinez', 'david.martinez@example.com', '7890123456', '505 Oak St', 'Austin', 'TX', '78901', '2024-04-02 16:00:00'),
('Michelle', 'Lopez', 'michelle.lopez@example.com', '8901234567', '707 Cedar St', 'Orlando', 'FL', '89012', '2024-04-04 17:00:00'),
('James', 'Taylor', 'james.taylor@example.com', '9012345678', '909 Pine St', 'San Diego', 'CA', '90123', '2024-04-02 18:00:00'),
('Emma', 'Garcia', 'emma.garcia@example.com', '0123456789', '111 Walnut St', 'Albany', 'NY', '01234', '2024-04-02 19:00:00'),
('George', 'Washington', 'Mr1st@example.com', '0000000000', '123 Sesame Street', 'Cincinnati', 'OH', '00000', NOW());  -- bids has a placeholder for memberID for customers that buy without bidding, this is meant as a placeholder for customer who do not BID ONLY to be referenced in the BID table
-- add city for the members -> (DONE)

INSERT INTO CarVINs(VIN_carID, purchase_status, memberID) VALUES
('SALSF2D47CA305941', 'Dealership - Not Purchased', NULL), -- cars on the lot
('2G4GU5GV1D9224709', 'Dealership - Not Purchased', NULL),
('WAUEG94F16N011182', 'Dealership - Not Purchased', NULL),
('1G4HP57M79U336833', 'Dealership - Not Purchased', NULL),
('2T1KE4EEXDC541493', 'Dealership - Not Purchased', NULL),
('WDDHF2EBXBA659567', 'Dealership - Not Purchased', NULL),
('WVWED7AJ7CW030690', 'Dealership - Not Purchased', NULL),
('WBSBR93441E328102', 'Dealership - Not Purchased', NULL),
('3VW517AT2FM570847', 'Dealership - Not Purchased', NULL),
('1G6DJ5ED0B0941154', 'Dealership - Not Purchased', NULL),
('1G4HP52KX44657084', 'Dealership - Not Purchased', NULL),
('JN8AZ2KRXAT240808', 'Dealership - Not Purchased', NULL),
('3C4PDCABXCT526082', 'Dealership - Not Purchased', NULL),
('WA1DKBFP7BA136094', 'Dealership - Not Purchased', NULL),
('2T1KE4EE8BC840347', 'Dealership - Not Purchased', NULL),
('WAUJT54B03N038966', 'Dealership - Not Purchased', NULL),
('WAUBFBFL5AN763430', 'Dealership - Not Purchased', NULL),
('SCFBF04B27G426214', 'Dealership - Not Purchased', NULL),
('5N1AA0NE2FN817354', 'Dealership - Not Purchased', NULL),
('KNALN4D74F5929503', 'Dealership - Not Purchased', NULL),
('JTDZN3EU7FJ029990', 'Dealership - Not Purchased', NULL),
('KM8JT3AB0BU232473', 'Dealership - Not Purchased', NULL),
('ZHWGU5AU9CL270811', 'Dealership - Not Purchased', NULL),
('KMHHT6KD5DU114602', 'Dealership - Not Purchased', NULL),
('ZHWGU5BZ8CL986853', 'Dealership - Not Purchased', NULL),
('JN1BJ0HP7EM887736', 'Dealership - Not Purchased', NULL),
('1FT8W3BT0NEA56299', 'Dealership - Not Purchased', NULL),

('5YJYGDEF7DF485512', 'Dealership - Purchased', 1), -- new spot for Dealership purchased vehicles
('7YJSKDVF8MF475533', 'Dealership - Purchased', 2),
('5YJYCDED8MF475533', 'Dealership - Purchased', 2),
('4YJSA1DG9MF395318', 'Dealership - Purchased', 3),
('WA1YD64B23N299063', 'Dealership - Purchased', 3),
('5G3S2DKL1MR150912', 'Dealership - Purchased', 4),
('3GTU2NEC7JG152638', 'Dealership - Purchased', 5),
('NM0LS7E23J1365787', 'Dealership - Purchased', 9),
('5N1AA0ND2EN467326', 'Dealership - Purchased', 5),
('JN1CV6FE1FM347717', 'Dealership - Purchased', 5),
('3FA6P0LU7ER984703', 'Dealership - Purchased', 6),
('WD3PE8CB6D5769421', 'Dealership - Purchased', 7),
('WAUKH98E87A124721', 'Dealership - Purchased', 7),
('19UUA66298A039588', 'Dealership - Purchased', 1),
('WBADN53481G171888', 'Dealership - Purchased', 2),
('SAJWA1EK7EM977306', 'Dealership - Purchased', 3),
('WAUJEGF4E87465621', 'Dealership - Purchased', 4),
('WBAVA37567N303400', 'Dealership - Purchased', 5),
('1C3BC4FBXBN521723', 'Dealership - Purchased', 6),
('JH4DC54895S001234', 'Dealership - Purchased', 7), --
('1FTMF1E85AK857700', 'Dealership - Purchased', 8),
('1GYS4DKL7MR225532', 'Dealership - Purchased', 9),
('1G4HP54K74U724821', 'Dealership - Purchased', 10),
('WAUUFAFH4AN515152', 'Dealership - Purchased', 1),
('JTDJTUD38ED022075', 'Dealership - Purchased', 2), -- add info for tthese into the db for car info bruh
('1G6DE5EG4A0418636', 'Dealership - Purchased', 3),
('1FTEW1E8XAK386177', 'Dealership - Purchased', 4),
('WBAAX134X4P941020', 'Dealership - Purchased', 5),
('WAUHF78P19A929792', 'Dealership - Purchased', 6), --
('WBXPA93444W811966', 'Dealership - Purchased', 7), --
('ZFBCFADH1EZ980832', 'Dealership - Purchased', 8),
('WAUNF98P37A160773', 'Dealership - Purchased', 9),
('WUATNAFG2EN786809', 'Dealership - Purchased', 10),
('1B3CC5FBXAN551956', 'Dealership - Purchased', 1),
('1G6DV1EP4F0840180', 'Dealership - Purchased', 2),
('1D7RW3BK8BS446576', 'Dealership - Purchased', 3),
('JTHKD5BH1C2538310', 'Dealership - Purchased', 4),
('WAULT58E03A107692', 'Dealership - Purchased', 5),
('SCFEBBAK9EG600978', 'Dealership - Purchased', 6),
('1LNHL9DR1CG561984', 'Dealership - Purchased', 7),
('WBA4J3C56KB000100', 'Dealership - Purchased', 9),
('4T1BK1EB3EU579953', 'Dealership - Purchased', 8),
('3D73Y4EL4BG548166', 'Dealership - Purchased', 8),
('WAUDF48H57A145781', 'Dealership - Purchased', 7),
('1B3CB3HA6AD530751', 'Dealership - Purchased', 6),
('5FRYD3H48FB697538','Outside Dealership', 1), -- customer added cars *--
('WA1CMAFE1CD332305','Outside Dealership', 2),
('WA1MYAFE8AD005776','Outside Dealership', 3),
('1FTNF2A59AE274535','Outside Dealership', 4),
('4USBU33577L779003','Outside Dealership', 5),
('1YVHZ8AHXA5361715','Outside Dealership', 6),
('JN8AZ2KRXET870589','Outside Dealership', 7),
('WAUAF78E35A401889','Outside Dealership', 8),
('1G6DA8E5XC0766424','Outside Dealership', 9),
('5UXWX9C54D0838067','Outside Dealership', 10),
('WVWED7AJ6DW427020','Outside Dealership', 1),
('WBAAX13423P051870','Outside Dealership', 2),
('1FTSW2B58AE824132','Outside Dealership', 3),
('WUARL48H58K525655','Outside Dealership', 4),
('WVWAA7AH3AV482448','Outside Dealership', 5),
('WBAVM5C59EV711847','Outside Dealership', 6),
('SCBLC37F43C179911','Outside Dealership', 7);
-- make up mock data for vins of dealership purchased cars -> (DONE)


INSERT INTO CarInfo (VIN_carID, make, model, body, year, color, mileage, details, description, viewsOnPage, pictureLibraryLink, status, price) VALUES
('SALSF2D47CA305941', 'Toyota', 'RAV4', 'SUV', 2023, 'Silver', 22872, 'The Toyota RAV4 is a highly versatile compact SUV renowned for its reliability, practicality, and impressive off-road capability, making it a top choice for adventurous families and urban commuters alike.', 'The Toyota RAV4 stands as a stalwart in the compact SUV segment, boasting a sleek and modern design coupled with a spacious interior, advanced safety features, and optional all-wheel drive, making it a dependable and versatile choice for both urban and off-road adventures, while its fuel-efficient engines ensure economical journeys for drivers around the globe.',  2, 'https://alcf.s3.us-west-1.amazonaws.com/_custom/2023/toyota/rav4/2023-toyota-rav4-main.png', 'being-watched', 35955.00),
('2G4GU5GV1D9224709', 'Toyota', 'Camry', 'Sedan', 2023, 'Black', 24053, 'The Toyota Camry is a reliable and fuel-efficient midsize sedan, celebrated for its spacious interior, smooth ride, and reputation for long-term durability, making it a top choice for practical-minded drivers seeking comfort and value.', 'The Toyota Camry epitomizes dependability and comfort, boasting a refined exterior design complemented by a spacious and well-appointed cabin featuring advanced technology and safety features, while its efficient yet potent engine options deliver a smooth and enjoyable driving experience, solidifying its position as a perennial favorite in the midsize sedan segment.',  4, 'https://purepng.com/public/uploads/large/purepng.com-toyotatoyotamotor-corporationautomotivemanufactureraichimultinational-1701527678522k1jrm.png', 'being-watched', 86147.00),
('WAUEG94F16N011182', 'Toyota', 'Tacoma', 'Pickup Truck', 2023, 'Silver', 5000, 'The Toyota Tacoma is a rugged midsize Pickup Truck known for its off-road capability, reliability, and versatile design, making it a trusted companion for outdoor adventures and daily tasks.', 'The Toyota Tacoma is built to conquer tough terrain with its robust construction, powerful engine options, and available off-road features, all wrapped in a practical Pickup Truck body style that\'s perfect for hauling gear, towing trailers, or exploring off the beaten path, making it a top choice for adventure seekers and weekend warriors.',  30, 'https://www.freepnglogos.com/uploads/toyota-logo-png/toyota-logo-emblem-symbol-png-transparent-17.png', 'new', 33000.00),
('1G4HP57M79U336833', 'Toyota', 'Corolla', 'Sedan', 2024, 'White', 100, 'The Toyota Corolla is a compact sedan known for its reliability, fuel efficiency, and practicality, offering a comfortable ride and a host of standard safety features.', 'The Toyota Corolla has a long-standing reputation for durability and value, featuring a spacious and well-appointed interior, advanced safety technology, and excellent fuel economy, making it an ideal choice for budget-conscious buyers and urban commuters.',  9, 'https://www.freepnglogos.com/uploads/toyota-logo-png/toyota-logo-emblem-symbol-png-transparent-17.png', 'new', 25000.00),
('2T1KE4EEXDC541493', 'Toyota', 'Prius', 'Hatchback', 2024, 'Silver', 200, 'The Toyota Prius is known for its exceptional fuel efficiency and eco-friendly design. With its sleek hatchback body style and advanced hybrid technology, the Prius offers a comfortable and environmentally conscious driving experience. Equipped with modern features and cutting-edge safety technology, this Prius is perfect for eco-conscious drivers looking for a reliable and fuel-efficient vehicle.', 'Experience the future of driving with the Toyota Prius. Its innovative hybrid powertrain combines a gasoline engine with an electric motor, delivering impressive fuel economy without sacrificing performance. Step inside the spacious and well-appointed interior, where advanced technology and premium materials create a comfortable and enjoyable driving environment. Whether you\'re commuting to work or embarking on a road trip, the Toyota Prius offers a smooth and efficient ride every time.', 4, 'https://static.foxdealer.com/742/2023/01/LE-prius.png','new', 32000.00),
('WDDHF2EBXBA659567', 'Toyota', 'Yaris', 'Hatchback', 2024, 'Black', 450, 'The Toyota Yaris is a versatile and efficient hatchback that\'s perfect for urban commuting and weekend adventures. With its compact size and nimble handling, the Yaris offers a fun and agile driving experience. Equipped with modern features and advanced safety technology, this Yaris delivers peace of mind on every journey.', 'Elevate your daily drive with the Toyota Yaris. Its sporty exterior design and aerodynamic profile make a bold statement on the road, while its efficient engine delivers impressive performance and fuel efficiency. Inside, the Yaris offers a comfortable and stylish cabin, with plenty of room for passengers and cargo. Whether you\'re navigating city streets or cruising down the highway, the Toyota Yaris offers a dynamic driving experience that\'s sure to impress.', 4, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSCSaJUq-Sn__Bz3dwu9Wd0I3yp1qbUkOIPf537H2Ccjw&s', 'new', 26000.00),
('WVWED7AJ7CW030690', 'Jeep', 'Compass', 'SUV', 2023, 'Green', 10615, 'The Jeep Compass is a compact SUV known for its rugged yet refined design, off-road capability, and advanced technology features, offering adventurous drivers a blend of versatility and comfort both on and off the beaten path.', 'The Jeep Compass epitomizes the brand\'s heritage of adventure with its distinctive styling cues reminiscent of its larger siblings, featuring a spacious cabin outfitted with modern amenities and intuitive technology, while its capable four-wheel-drive system and terrain management options ensure confident performance whether navigating city streets or tackling challenging trails, making it a compelling choice for those seeking versatility and exploration in a compact SUV.',  9, 'https://images.dealer.com/ddc/vehicles/2023/Jeep/Compass/SUV/perspective/front-left/2023_76.png', 'being-watched', 33244.00),
('WBSBR93441E328102', 'Jeep', 'Cherokee', 'SUV', 2023, 'Gray', 17798, 'The Jeep Cherokee is a rugged yet refined midsize SUV, blending off-road capability with modern comforts and technology, offering drivers a versatile vehicle suited for both urban commuting and adventurous excursions.', 'The Jeep Cherokee embodies the spirit of adventure with its iconic seven-slot grille and athletic silhouette, featuring a comfortable and well-appointed interior equipped with advanced tech amenities, while its legendary 4x4 capability, available in various trim levels, ensures confident performance across diverse terrain, making it a standout choice in the competitive midsize SUV segment.',  6, 'https://purepng.com/public/uploads/large/purepng.com-black-jeep-grand-cherokee-carcarvehicletransportjeep-9615246526987jplf.png', 'being-watched', 98131.00),
('3VW517AT2FM570847', 'Jeep', 'Renegade', 'SUV', 2024, 'Black', 12033, 'The Jeep Renegade is a compact SUV that combines iconic Jeep styling with nimble handling and off-road capability, making it an adventurous choice for urban explorers and outdoor enthusiasts alike.', 'The Jeep Renegade embodies the spirit of exploration with its distinctive and rugged design cues, featuring a compact yet versatile platform that excels both on city streets and off-road trails, while its spacious interior, advanced technology, and available four-wheel-drive systems ensure a comfortable and capable driving experience, solidifying its position as a standout option in the competitive compact SUV segment.',  5, 'https://purepng.com/public/uploads/large/purepng.com-black-jeep-renegade-carcarvehicletransportjeep-961524653966l65bn.png', 'being-watched', 76407.00),
('1G6DJ5ED0B0941154', 'Jeep', 'Grand Cherokee', 'SUV', 2024, 'Gray', 150, 'The Jeep Grand Cherokee is a legendary SUV known for its rugged capability and refined interior. With its spacious cabin and advanced technology features, the Grand Cherokee offers a comfortable and connected driving experience. Whether you\'re navigating city streets or tackling off-road trails, this Grand Cherokee is ready for any adventure.', 'Experience the pinnacle of SUV performance with the Jeep Grand Cherokee. Its bold design and iconic Jeep styling make a statement on the road, while its powerful engine and advanced four-wheel-drive system deliver exceptional capability in any terrain. Inside, the Grand Cherokee offers a luxurious and versatile interior, with premium materials and innovative technology features that enhance comfort and convenience for both driver and passengers. From daily commuting to weekend getaways, the Jeep Grand Cherokee is the ultimate SUV for those who demand the best.', 4, 'https://images.dealer.com/ddc/vehicles/2022/Jeep/Grand%20Cherokee%20WK/SUV/perspective/front-left/2022_24.png', 'new', 64000.00),
('1G4HP52KX44657084', 'Jeep', 'Grand Cherokee', 'SUV', 2024, 'Blue', 400, 'The Jeep Grand Cherokee is a legendary SUV known for its rugged capability and refined interior. With its spacious cabin and advanced technology features, the Grand Cherokee offers a comfortable and connected driving experience. Whether you\'re navigating city streets or tackling off-road trails, this Grand Cherokee is ready for any adventure.', 'Experience the pinnacle of SUV performance with the Jeep Grand Cherokee. Its bold design and iconic Jeep styling make a statement on the road, while its powerful engine and advanced four-wheel-drive system deliver exceptional capability in any terrain. Inside, the Grand Cherokee offers a luxurious and versatile interior, with premium materials and innovative technology features that enhance comfort and convenience for both driver and passengers. From daily commuting to weekend getaways, the Jeep Grand Cherokee is the ultimate SUV for those who demand the best.', 4, 'https://www.greenbriercdjr.com/static/dealer-23595/aronson/2024/Grand_Cherokee/24Jeep-GrandCherokee-Overland-HydroBlue-Jellybean.png', 'new', 65000.00),
('JN8AZ2KRXAT240808', 'Jeep', 'Wrangler', 'Convertible', 2024, 'Gray', 200, 'The Jeep Wrangler is an iconic off-road vehicle known for its rugged capability and open-air driving experience. With its removable roof and doors, the Wrangler offers unparalleled freedom and adventure. Whether you\'re tackling rocky trails or cruising around town, this Wrangler is ready for any terrain.', 'Unleash your sense of adventure with the Jeep Wrangler. Its classic design and rugged construction make it the ultimate off-road companion, capable of conquering even the toughest terrain. With its powerful engine and advanced four-wheel-drive system, the Wrangler delivers unmatched performance and capability in any environment. Step inside the spacious and versatile cabin, where you\'ll find comfort and convenience features designed to enhance every journey. Whether you\'re exploring the wilderness or navigating city streets, the Jeep Wrangler offers a thrilling and unforgettable driving experience.', 4, 'https://www.creativefabrica.com/wp-content/uploads/2023/05/09/Jeep-Wrangler-Convertible-Graphic-69201202-1.png','new', 47000.00),
('3C4PDCABXCT526082', 'Chevrolet', 'Traverse', 'SUV', 2023, 'Silver', 11965, 'The Chevy Traverse is a spacious and versatile midsize SUV, offering ample seating for up to eight passengers, abundant cargo space, and a smooth ride, making it an ideal choice for families seeking comfort and utility on their journeys.', 'The Chevy Traverse stands out in the midsize SUV category with its combination of generous interior space, refined ride quality, and plethora of family-friendly features, including numerous USB ports, Wi-Fi hotspot capability, and advanced safety technology, ensuring both comfort and peace of mind on every journey, making it a compelling option for those in need of a capable and accommodating vehicle for their daily adventures.',  9, 'https://purepng.com/public/uploads/large/purepng.com-chevrolet-traversecarschevroletchevyautomobile-1701527437601gixkb.png', 'new', 94250.00),
('WA1DKBFP7BA136094', 'Chevrolet', 'Silverado', 'SUV', 2023, 'Black', 30517, 'The Chevy Silverado is a rugged and versatile full-size Pickup Truck renowned for its powerful engine options, robust towing capacity, and advanced technology features, making it a trusted workhorse for demanding jobs and everyday adventures.', 'The Chevy Silverado boasts a robust frame and high-strength steel construction, providing exceptional durability and towing capability, while its range of available trim levels offers options for luxury, performance, and utility, ensuring there\'s a Silverado model suited for every driver\'s needs. With features like advanced trailering technology, a variety of bed and cab configurations, and a comfortable and tech-savvy interior, the Silverado seamlessly blends capability with comfort, making it a standout choice in the competitive truck market.',  4, 'https://purepng.com/public/uploads/large/purepng.com-chevrolet-silverado-colorado-black-carcarvehicletransportchevroletchevy-961524650954kotq0.png', 'being-watched', 89256.00),
('2T1KE4EE8BC840347', 'Chevrolet', 'Malibu', 'Sedan', 2024, 'Silver', 29429, 'The Chevy Malibu is a stylish midsize sedan renowned for its fuel efficiency, spacious interior, and smooth ride, making it a popular choice for both daily commuting and long-distance travel.', 'The Chevy Malibu embodies sophistication and practicality, featuring a sleek exterior design complemented by a spacious and comfortable interior equipped with modern amenities and advanced safety features, while its efficient engine options and smooth ride quality ensure an enjoyable driving experience, making it a standout option in the competitive midsize sedan market.',  3, 'https://www.chevrolet.com/content/dam/chevrolet/na/us/english/index/vehicles/2022/cars/malibu/01-images/colorizer/2022-malibu-1lt-gan-colorizer.jpg?imwidth=1200', 'being-watched', 30995.00),
('WAUJT54B03N038966', 'Chevrolet', 'Colorado', 'SUV', 2024, 'Blue', 200, 'The Chevrolet Colorado is a versatile and capable SUV designed to tackle any adventure. With its rugged construction and powerful engine options, the Colorado offers impressive performance both on and off the road. Whether you\'re hauling gear for a weekend getaway or navigating city streets, this Colorado is ready for whatever comes your way.', 'Experience the freedom of the open road with the Chevrolet Colorado. Its bold design and durable build make it the perfect SUV for outdoor enthusiasts and urban adventurers alike. With its spacious interior and versatile cargo space, the Colorado offers plenty of room for passengers and gear, ensuring a comfortable and convenient ride every time. Whether you\'re exploring the great outdoors or running errands around town, the Chevrolet Colorado delivers the performance and versatility you need to make every journey unforgettable.', 4, 'https://www.chevrolet.com/content/dam/chevrolet/na/us/english/vdc-collections/2024/trucks/colorado/01-images/2024-colorado-14h43-4zr-glt-trimselector.png?imwidth=960', 'new', 42000.00),
('WAUBFBFL5AN763430', 'Chevrolet', 'Corvette', 'Convertible', 2024, 'Red', 300, 'The Chevrolet Corvette is an iconic sports car that combines breathtaking performance with striking design. With its powerful engine and precise handling, the Corvette offers an exhilarating driving experience unlike any other. Whether you\'re cruising down the highway or tearing up the track, this Corvette is sure to turn heads wherever you go.', 'Unleash the power of the Chevrolet Corvette. Its sleek and aerodynamic design hints at the incredible performance that lies beneath the surface. With its advanced technology and precision engineering, the Corvette delivers heart-pounding acceleration and razor-sharp handling that will leave you breathless. Step inside the luxurious interior, where premium materials and cutting-edge technology', 4, 'https://di-sitebuilder-assets.s3.amazonaws.com/GMimages/gmMLP/chevrolet/Corvette/1LT+Convertible.jpg', 'new', 96000.00),
('SCFBF04B27G426214', 'Chevrolet', 'Tahoe', 'SUV', 2024, 'Black', 2500, 'The Chevrolet Tahoe is a full-size SUV known for its spacious interior, powerful performance, and advanced technology, offering comfort and capability for the whole family.', 'The Chevrolet Tahoe is the perfect blend of luxury and utility, featuring a refined interior, potent engine options, and cutting-edge technology, all wrapped in a versatile SUV body style that\'s perfect for hauling passengers, towing trailers, or exploring off-road trails, making it a top choice for families and adventurers alike.',  28, 'https://www.freepnglogos.com/uploads/chevrolet-silverado-png/2003-chevrolet-tahoe-1lt-4dr-suv-logo-chevrolet-suburban-16.png', 'new', 68000.00),
('5N1AA0NE2FN817354', 'Chevrolet', 'Suburban', 'SUV', 2024, 'White', 3500, 'The Chevrolet Suburban is a full-size SUV known for its cavernous interior, robust towing capacity, and advanced safety features, offering luxury and utility in equal measure.', 'The Chevrolet Suburban is the ultimate family hauler, featuring seating for up to nine passengers, a spacious cargo area, and a host of entertainment and convenience features, all powered by a powerful engine that\'s perfect for towing boats, trailers, or campers, making it the perfect vehicle for road trips, family vacations, or everyday adventures.',  35, 'https://www.freepnglogos.com/uploads/chevrolet-silverado-png/2003-chevrolet-tahoe-1lt-4dr-suv-logo-chevrolet-suburban-16.png', 'new', 72000.00),
('KNALN4D74F5929503', 'Chevrolet', 'Express Cargo', 'Van', 2024, 'White', 150, 'The Chevrolet Express Cargo van is designed to handle the demands of your business with ease. With its spacious cargo area and robust construction, the Express Cargo van offers ample space for transporting goods and equipment. Whether you\'re making deliveries or hauling tools to the job site, this van is built to get the job done.', 'Get the job done right with the Chevrolet Express Cargo van. Its durable construction and reliable performance make it the perfect vehicle for businesses of all sizes. With its versatile cargo space and customizable interior options, the Express Cargo van offers the flexibility and capability you need to tackle any task. From deliveries to service calls, trust the Chevrolet Express Cargo van to keep your business moving forward.', 4, 'https://inv.assets.ansira.net/ChromeColorMatch/us/TRANSPARENT_cc_2024CHV340039_01_1280_GAZ.png', 'new', 54000.00),
('JTDZN3EU7FJ029990', 'Chevrolet', 'Express Passenger', 'Van', 2024, 'Black', 220, 'The Chevrolet Express Passenger van is designed to transport passengers in comfort and style. With its spacious interior and configurable seating options, the Express Passenger van offers plenty of room for passengers and cargo alike. Whether you\'re shuttling clients to meetings or taking the family on a road trip, this van is equipped to handle it all.', 'Travel in comfort and style with the Chevrolet Express Passenger van. Its versatile interior and premium amenities make it the perfect vehicle for both business and pleasure. With its spacious seating and advanced entertainment options, the Express Passenger van ensures a smooth and enjoyable ride for all passengers. Whether you\'re on the job or on vacation, trust the Chevrolet Express Passenger van to get you there safely and comfortably.', 4, 'https://images.carprices.com/pricebooks_data/usa/colorized/2024/Chevrolet/View2/Express_Passenger_Van/Base/CG33706_GBA.png', 'new', 58000.00),
('KM8JT3AB0BU232473', 'Ford', 'Focus', 'Hatchback', 2024, 'Blue', 6980, 'The Ford Focus is a versatile compact car renowned for its fuel efficiency, agile handling, and practical design, making it a popular choice for urban commuters and small families alike.', 'The Ford Focus is a compact car designed with a focus on efficiency and versatility, featuring a sleek exterior design complemented by a comfortable and well-equipped interior, offering ample space for passengers and cargo, while its responsive handling and range of available engines provide a dynamic driving experience suited for city streets or long highway journeys.',  1, 'https://pngimg.com/uploads/ford/ford_PNG12204.png', 'low-mileage', 65203.00),
('ZHWGU5AU9CL270811', 'Ford', 'Mustang', 'Coupe', 2023, 'Orange', 35198, 'An iconic American muscle car known for its sleek design and powerful performance.', 'The Ford Mustang is a two-door sports car featuring a sleek and aerodynamic exterior design, with a powerful engine lineup ranging from fuel-efficient options to high-performance V8s, coupled with advanced technology and comfort features, making it a versatile and thrilling driving machine beloved by enthusiasts worldwide.',  7, 'https://pngimg.com/uploads/mustang/mustang_PNG15.png', 'being-watched', 81576.00),
('KMHHT6KD5DU114602', 'Ford', 'Mustang', 'Coupe', 2024, 'Red', 150, 'An iconic American muscle car known for its sleek design and powerful performance.', 'The Ford Mustang is a two-door sports car featuring a sleek and aerodynamic exterior design, with a powerful engine lineup ranging from fuel-efficient options to high-performance V8s, coupled with advanced technology and comfort features, making it a versatile and thrilling driving machine beloved by enthusiasts worldwide.', 4, 'https://vehicle-images.dealerinspire.com/stock-images/chrome/d4ccfa4f8e74dfdf9d7766d55c963ab5.png','new', 55000.00),
('ZHWGU5BZ8CL986853', 'Ford', 'F-150', 'SUV', 2023, 'Gray', 40650, 'The Ford F-150 is a legendary full-size Pickup Truck renowned for its robust performance, class-leading towing capability, and innovative features, making it a perennial favorite among truck enthusiasts and professionals alike.', 'The Ford F-150, an icon in the realm of Pickup Trucks, boasts a sturdy yet lightweight aluminum body, paired with a range of powerful engines, including hybrid options, delivering unparalleled towing and hauling capacities while offering a comfortable cabin equipped with cutting-edge technology and safety features, solidifying its status as the best-selling vehicle in America for decades.',  2, 'https://pictures.dealer.com/t/theherbchamberscompanies/0496/4a54066f8dd6f8e4b39af56e792401fcx.jpg', 'new', 45325.00),
('JN1BJ0HP7EM887736', 'Ford', 'F-250', 'Pickup Truck', 2024, 'Black', 50, 'The Ford F-250 is a heavy-duty Pickup Truck designed to tackle the toughest jobs. With its robust construction and powerful engine options, the F-250 offers impressive towing and hauling capability. Whether you\'re on the job site or off the beaten path, this F-250 is built to handle whatever comes your way.', 'Dominate the road with the Ford F-250. Its rugged exterior design and durable construction make it the perfect vehicle for work or play. With its spacious and comfortable interior, the F-250 offers a refined driving experience for both driver and passengers. With advanced technology features and innovative safety systems, the F-250 delivers peace of mind on every journey. Whether you\'re towing a trailer or exploring the great outdoors, trust the Ford F-250 to get the job done right.', 4, 'https://build.ford.com/dig/Ford/SuperDuty/2024/HD-TILE/Image%5B%7CFord%7CSuperDuty%7C2024%7C1%7C1.%7C603A.F2B.142.PUM.LSC.883.89S.A7AAK.CBC.XLT.~AASBA.924.BBHAB.BLDAE.54K.91X.66B.REC.CLFAE.SRW.648.TCH.4X4.99N.FBFAB.91Z.GTDAB.67D.43C.585.IEVAR.595.250.44G.X37.CLO.%5D/EXT/1/vehicle.png', 'new', 72000.00),
('1FT8W3BT0NEA56299', 'Ford', 'Super Duty F-350', 'Pickup Truck', 2024, 'Black', 200, 'The Ford Super Duty F-350 is a powerhouse of a Pickup Truck, offering unmatched capability and durability. With its heavy-duty construction and powerful engine options, the F-350 is built to handle the toughest tasks with ease. Whether you\'re towing a trailer or hauling a heavy load, this F-350 delivers the performance and reliability you need to get the job done right.', 'Conquer any challenge with the Ford Super Duty F-350. Its bold design and rugged features make it the ultimate workhorse for demanding jobs. With its spacious and comfortable interior, the F-350 offers a refined driving experience for both work and play. With advanced technology features and innovative safety systems, the F-350 provides peace of mind on even the toughest jobs. Whether you\'re on the job site or on the road, trust the Ford Super Duty F-350 to deliver the performance and capability you need to tackle any task.', 4, 'https://build.ford.com/dig/Ford/SuperDuty/2024/HD-TILE/Image%5B%7CFord%7CSuperDuty%7C2024%7C1%7C1.%7C613A.F3B.142.PUM.LSC.883.89S.A7AAK.CBC.XLT.~AASBA.924.BBHAB.BLDAE.54K.91X.66B.REC.CLFAE.SRW.648.TCH.4X4.99N.FBFAB.91Z.GTDAB.67D.43C.585.IEVAR.595.350.44G.X3E.CLO.%5D/EXT/1/vehicle.png', 'new', 78000.00),
# ('NM0LS7E23J1365784', 'Ford', 'Transit Connect', 'Van', 2024, 'Blue', 200, 'The Ford Transit Connect is a versatile and practical van designed for commercial and personal use. With its spacious cargo area and efficient engine options, the Transit Connect offers plenty of room for transporting goods or passengers. Whether you\'re making deliveries or running errands around town, this Transit Connect is up to the task.', 'Meet your business needs with the Ford Transit Connect. Its compact size and maneuverable handling make it ideal for navigating crowded city streets, while its spacious cargo area provides ample room for hauling goods and equipment. With its efficient engine options and advanced technology features, the Transit Connect delivers both performance and productivity. Whether you\'re a small business owner or a busy family on the go, the Ford Transit Connect offers the versatility and reliability you need to get the job done.', 4, 'https://inv.assets.ansira.net/ChromeColorMatch/us/TRANSPARENT_cc_2023FOV320066_01_1280_TY.png', 'new', 38000.00),
# ('WA1YD64B23N299062', 'BMW', 'BMW 4 Series Convertible', 'Convertible', 2024, 'Green', 100, 'The BMW 4 Series Convertible combines sporty performance with luxurious comfort in a sleek and stylish package. With its retractable hardtop roof and powerful engine options, the 4 Series Convertible offers an exhilarating driving experience. Whether you\'re cruising along the coast or exploring winding mountain roads, this convertible delivers thrills at every turn.', 'Experience the thrill of open-air driving with the BMW 4 Series Convertible. Its dynamic design and sophisticated features make it the perfect choice for drivers who demand both style and performance. With its luxurious interior and advanced technology, the 4 Series Convertible offers a driving experience unlike any other. Whether you\'re enjoying a weekend getaway or commuting to work, the BMW 4 Series Convertible is sure to make every journey memorable.', 15, 'https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-7331cqgv2Z7d%25i02uCaY3MuO2kOHUtWPfbYf6JWl10tLhu1XzWVo7puMLWFmdkAj5DOP7tpmZ8XgY1nTNIowJ4HO3zkyXq%25sGM8snpq6v6ODubLz2aKqfkSRjmB2fJj5DOP5Eagd%25kcWExHWpbl8FO2k3Hy2o24mB%25TQBrXpFpDjlZ24riIikascpF4HvHnJ0KiIFJGJdZABHvIT9PvrO2JGvloMLUgpT9GsLDSbUilo90yYt3bHsLoACtq2hJ0yLOEfm%25qTACygNS3umlOECUkdXJ7sgNEbnQrg10UkNh56x4VAbnkq8wmFzOh5nmP%25TFagq857Mu0kRUmP81D4VWxb7MPVYFMnWh1DMztIDQeqVYDafv06jmztYRSGBP67aftxd92gw1RSfWQopq%25VxdSeZLK5uzWQdjcyA83aeZQ6KCofXRjcZwBELsrx6Kc%252ZKz4WwBKupcBhFe%252B3iKHvIjup2XHBysv63iprJ2CrGwXHi4TpEX9%25rJHFliNPou4TJIsHkTL3FlTv0JnYyXIslGATwJCrv0s9Ol%25LE4GA0og8ZTNF9OALUP6XkIogOybM%255nvLUgChDYE5GybUEqYtI89ChbNmtf2PoEqhk7f6vMLNmqn1SwtDyk7m5Vd3%25YCn178zQBvtE5V1PaZ2SfN8zVMRcbcSkPazDxM07dnMRaYWDAQQ5DxRteYVVZ8YWxfjt4ncPteWS6Wy3KM4eJOiwWNRbsj43aJzMxQUdqfoLkW', 'new', 28985.00),

# ('5YJYGDEF7DF485512', 'Tesla', 'Model X', 'SUV', 2024, 'White', 150, 'The Tesla Model S Sedan is a flagship electric vehicle that sets the standard for performance, luxury, and innovation. With its sleek exterior design and minimalist interior, the Model S exudes sophistication and refinement. Its dual-motor all-wheel drive and Ludicrous Mode acceleration deliver exhilarating performance, while its long-range battery ensures you can travel with confidence.', 'Experience the pinnacle of electric luxury with the Tesla Model S Sedan. From its premium materials to its state-of-the-art technology, every aspect of the Model S is designed with the driver in mind. Whether you\'re cruising on the highway or navigating city streets, the Model S offers a comfortable and connected driving experience. With its industry-leading range and advanced autopilot features, the Model S redefines what a sedan can be.', 4, 'https://platform.cstatic-images.com/xlarge/in/v2/stock_photos/681a042f-9795-4768-bbf3-84d76f80285e/6ad54efb-efc7-46c9-b132-22f508d43abe.png', 'new', 97000.00),
# ('7YJSKDVF8MF475533', 'Tesla', 'Model Y', 'SUV', 2024, 'Blue', 50, 'The Tesla Model Y SUV is a versatile and efficient electric vehicle that offers a perfect blend of performance and practicality. Its compact size makes it ideal for navigating city streets, while its spacious interior provides ample room for passengers and cargo. With its dual-motor all-wheel drive and advanced safety features, the Model Y delivers confident handling and peace of mind on every journey.', 'Redefine your expectations of an SUV with the Tesla Model Y. Whether you\'re running errands around town or embarking on a weekend adventure, the Model Y offers the versatility and capability you need. Its responsive acceleration and agile handling make every drive enjoyable, while its long-range battery ensures you can go the distance without compromise. With its sleek design and advanced technology, the Model Y is ready to take you wherever life leads.', 4, 'https://platform.cstatic-images.com/xlarge/in/v2/stock_photos/39b7a783-dad2-4fa0-81a3-ba21292caaf6/acab7439-a66d-4f78-8ab9-d917268b4a7d.png', 'new', 96000.00),
# ('4YJSA1DG9MF395318', 'Tesla', 'Model S', 'Sedan', 2024, 'Red', 1000, 'The Tesla Model S Sedan is a flagship electric vehicle that sets the standard for performance, luxury, and innovation. With its sleek exterior design and minimalist interior, the Model S exudes sophistication and refinement. Its dual-motor all-wheel drive and Ludicrous Mode acceleration deliver exhilarating performance, while its long-range battery ensures you can travel with confidence.', 'Experience the pinnacle of electric luxury with the Tesla Model S Sedan. From its premium materials to its state-of-the-art technology, every aspect of the Model S is designed with the driver in mind. Whether you\'re cruising on the highway or navigating city streets, the Model S offers a comfortable and connected driving experience. With its industry-leading range and advanced autopilot features, the Model S redefines what a sedan can be.', 4, 'https://static-assets.tesla.com/configurator/compositor?context=design_studio_2?&bkba_opt=1&view=STUD_3QTR_V2&size=1400&model=ms&options=$MDLS,$MTS05,$PPMR,$RFFR,$WTD2,$INB3P,$PI01,$APBS,$SC04,$CPF0&crop=1400,850,300,130&', 'new', 90000.00),
# ('5G3S2DKL1MR150912', 'GMC', 'Yukon', 'SUV', 2024, 'Silver', 250, 'The GMC Yukon SUV combines rugged capability with refined luxury to provide a versatile and comfortable driving experience. With its spacious interior, advanced technology features, and powerful engine options, the Yukon is perfect for families and adventurers alike. Whether you\'re tackling rough terrain or cruising on the highway, the Yukon delivers smooth performance and confident handling.', 'Elevate your driving experience with the GMC Yukon SUV. From its bold exterior design to its premium interior amenities, every detail of the Yukon is crafted with quality and craftsmanship in mind. With seating for up to eight passengers and ample cargo space, the Yukon offers flexibility for all your adventures. Whether you\'re embarking on a road trip or running errands around town, the Yukon provides the comfort, convenience, and capability you need to make every journey unforgettable.', 4, 'https://media.chromedata.com/MediaGallery/media/MjkzOTU4Xk1lZGlhIEdhbGxlcnk/o-J6O-H2pz9uZsMjbnG_uBcOpCSlPjyNdSvOV_QCfYOZpn0YX9iFufUMI0EIqU9yfDcIbe2XAvaeP-ymfaLvUhnwt4BkltShcEq-eCxHRmZlmShhs5b5yGGzKzwT2QEhpignwf0fHyZwowD98oacLSDKeyducG-otG7Iti7Xf4MV6GB_IDkOrg/cc_2024GMS290021_01_640_GAZ.png', 'new', 69000.00),
# ('JN1CV6FE1FM347717', 'Honda', 'Civic', 'Sedan', 2024, 'Black', 1000, 'The Honda Civic is a popular compact sedan known for its reliability, fuel efficiency, and sporty design, offering practicality and fun in equal measure.', 'The Honda Civic combines practicality with performance, featuring a stylish exterior, comfortable interior, and responsive handling, all powered by a fuel-efficient engine that\'s perfect for city commuting or long highway drives, making it a versatile choice for drivers of all ages and lifestyles.',  20, 'https://www.freepnglogos.com/uploads/honda-logo-png/honda-logo-emblem-symbol-png-transparent-11.png', 'new', 25000.00),
# ('3FA6P0LU7ER984703', 'Honda', 'Accord', 'Sedan', 2024, 'Gray', 800, 'The Honda Accord is a refined midsize sedan known for its spacious interior, smooth ride, and strong reputation for reliability, making it a top choice for families and commuters alike.', 'The Honda Accord strikes a perfect balance between comfort and performance, featuring a sleek exterior, upscale interior, and efficient engine options, all packaged in a practical sedan body style that\'s perfect for daily commuting, road trips, or running errands around town, making it a versatile and dependable choice for drivers of all ages.',  22, 'https://www.freepnglogos.com/uploads/honda-logo-png/honda-logo-emblem-symbol-png-transparent-11.png', 'new', 29000.00),
# ('WD3PE8CB6D5769421', 'Mercedes-Benz', 'Sprinter', 'Van', 2024, 'White', 100, 'The Mercedes-Benz Sprinter van is designed for versatility and practicality, offering ample cargo space and customizable configurations to suit various business needs. With its robust build quality and advanced safety features, the Sprinter ensures reliability and peace of mind on the road. Whether used for commercial purposes or as a recreational vehicle, the Sprinter delivers exceptional performance and comfort.', 'Experience unparalleled flexibility and functionality with the Mercedes-Benz Sprinter van. From its spacious interior to its innovative technology, the Sprinter is engineered to meet the demands of modern businesses and adventurers alike. With its sleek design and efficient engine options, the Sprinter combines style with substance, making it the perfect companion for any journey.', 4, 'https://vehicle-images.dealerinspire.com/stock-images/chrome/e4c8ec738e559d0d14c5bc97f91be3fb.png', 'new', 65000.00),
# ('1GYS4DKL7MR225532', 'Cadillac', 'Escalade', 'SUV', 2024, 'Gray', 100, 'The Cadillac Escalade SUV boasts a powerful V8 engine paired with advanced suspension technology for a smooth and refined ride. Its spacious cabin accommodates up to seven passengers in utmost comfort, with premium leather upholstery and high-end amenities throughout. Cutting-edge safety features such as adaptive cruise control and automatic emergency braking enhance driver confidence and peace of mind.', 'The 2024 Cadillac Escalade SUV sets the standard for luxury and refinement in the full-size SUV segment. Its bold exterior design is matched by a spacious and opulent interior, featuring premium materials and state-of-the-art technology. With its powerful engine and smooth ride, the Escalade effortlessly glides over any terrain. From its commanding presence on the road to its unmatched comfort and convenience features, the Cadillac Escalade redefines what it means to travel in style.', 4, 'https://images.dealer.com/ddc/vehicles/2024/CADILLAC/Escalade/SUV/perspective/front-left/2024_24.png','new', 86000.00),
# ('WAUUFAFH4AN515152', 'Mazda', 'MX-5 Miata', 'Convertible', 2024, 'Red',12423, 'The Mazda MX-5 Miata Convertible is powered by a responsive and fuel-efficient engine, delivering an exhilarating driving experience. Its lightweight construction and finely tuned chassis make for exceptional handling and agility on twisty roads. The convertible top operates effortlessly, allowing you to enjoy the open-air freedom at the touch of a button. Inside, the MX-5 Miata features a driver-centric cockpit with intuitive controls and premium materials.', 'The 2024 Mazda MX-5 Miata Convertible is the epitome of driving pleasure. With its iconic design and spirited performance, it captures the essence of the classic roadster experience. Whether cruising along coastal highways or navigating winding mountain roads, the MX-5 Miata delivers unmatched agility and responsiveness. Its retractable roof allows you to soak in the sun and feel the wind in your hair, creating unforgettable moments with every drive. Discover the joy of open-air motoring with the Mazda MX-5 Miata Convertible.', 5, 'https://pngimg.com/uploads/mazda/mazda_PNG28.png', 'new', 28985.00),
-- sold cars
('5N1AA0ND2EN467326', 'GMC', 'Yukon', 'SUV', 2024, 'White', 100, 'The GMC Yukon SUV combines rugged capability with refined luxury to provide a versatile and comfortable driving experience. With its spacious interior, advanced technology features, and powerful engine options, the Yukon is perfect for families and adventurers alike. Whether you\'re tackling rough terrain or cruising on the highway, the Yukon delivers smooth performance and confident handling.', 'Elevate your driving experience with the GMC Yukon SUV. From its bold exterior design to its premium interior amenities, every detail of the Yukon is crafted with quality and craftsmanship in mind. With seating for up to eight passengers and ample cargo space, the Yukon offers flexibility for all your adventures. Whether you\'re embarking on a road trip or running errands around town, the Yukon provides the comfort, convenience, and capability you need to make every journey unforgettable.', 4, 'https://images.carprices.com/pricebooks_data/usa/colorized/2024/GMC/View2/Yukon/Denali_Ultimate/TK10706_G1W.png', 'sold', 68000.00),
('3GTU2NEC7JG152638', 'GMC', 'Sierra 1500', 'SUV', 2024, 'White', 100, 'The GMC Sierra 1500 Pickup Truck offers impressive capability, advanced technology, and a comfortable interior. With its powerful engine options and robust towing capacity, the Sierra 1500 is ready to tackle tough jobs with ease. Whether you\'re hauling equipment to the job site or towing your camper for a weekend getaway, the Sierra 1500 delivers reliable performance and confidence on the road.', 'Experience the power and versatility of the GMC Sierra 1500 Pickup Truck. With its rugged exterior design and refined interior features, the Sierra 1500 offers the perfect blend of strength and sophistication. From its innovative trailering technologies to its spacious cabin with advanced connectivity options, every aspect of the Sierra 1500 is designed to enhance your driving experience. Whether you\'re working hard or playing hard, the Sierra 1500 is built to handle whatever you throw its way.', 4, 'https://alcf.s3.us-west-1.amazonaws.com/_custom/2024/gmc/sierra-1500/2024-gmc-sierra-1500%20%281%29.png', 'sold', 55000.00),
('JTDJTUD38ED022075', 'Toyota', 'Corolla', 'Sedan', 2014, 'Silver', 60000, 'Automatic transmission, 4 cylinders', 'Reliable and fuel-efficient sedan suitable for daily commute.', 0, '-', 'sold', 12000.00),
('1G6DE5EG4A0418636', 'Cadillac', 'CTS', 'Sedan', 2010, 'Black', 80000, 'Automatic transmission, V6 engine', 'Luxurious sedan with comfortable interior and powerful performance.', 0, '-', 'sold', 18000.00),
('5YJYGDEF7DF485512', 'Ford', 'F-150', 'Pickup Truck', 2010, 'White', 90000, 'Automatic transmission, V8 engine', 'Spacious and rugged Pickup Truck suitable for work and leisure activities.', 0, '-', 'sold', 22000.00),
('7YJSKDVF8MF475533', 'BMW', '3 Series', 'Sedan', 2004, 'Blue', 120000, 'Manual transmission, 6 cylinders', 'Sporty sedan with precise handling and dynamic performance.', 0, '-', 'sold', 10000.00),
('5YJYCDED8MF475533', 'Audi', 'A4', 'Sedan', 2009, 'Gray', 100000, 'Automatic transmission, 4 cylinders', 'Elegant sedan with refined interior and advanced technology features.', 0, '-', 'sold', 14000.00),
('4YJSA1DG9MF395318', 'BMW', 'X3', 'SUV', 2004, 'Black', 110000, 'Automatic transmission, 6 cylinders', 'Versatile SUV with ample cargo space and all-weather capability.', 0, '-', 'sold', 12000.00),
('5G3S2DKL1MR150912', 'Fiat', '500', 'Hatchback', 2014, 'Red', 50000, 'Automatic transmission, 4 cylinders', 'Compact and stylish hatchback ideal for city driving.', 0, '-', 'sold', 9000.00),
('1LNHL9DR1CG561984', 'Audi', 'A6', 'Sedan', 2007, 'Silver', 95000, 'Automatic transmission, V6 engine', 'Executive sedan with spacious interior and advanced safety features.', 0, '-', 'sold', 15000.00),
('WAUUFAFH4AN515152', 'Audi', 'Q5', 'SUV', 2014, 'White', 70000, 'Automatic transmission, 4 cylinders', 'Luxurious SUV with upscale cabin and strong performance.', 0, '-', 'sold', 25000.00),
('JN1CV6FE1FM347717', 'Dodge', 'Challenger', 'Coupe', 2010, 'Blue', 80000, 'Automatic transmission, V8 engine', 'Muscle car with powerful performance and iconic design.', 0, '-', 'sold', 20000.00),
('3FA6P0LU7ER984703', 'Cadillac', 'Escalade', 'SUV', 2015, 'Black', 60000, 'Automatic transmission, V8 engine', 'Luxurious SUV with spacious cabin and advanced entertainment features.', 0, '-', 'sold', 35000.00),
('WUATNAFG2EN786809', 'Dodge', 'Ram 1500', 'Pickup Truck', 2011, 'Red', 85000, 'Automatic transmission, V8 engine', 'Powerful Pickup Truck with impressive towing capacity and comfortable ride.', 0, '-', 'sold', 18000.00),
('1B3CC5FBXAN551956', 'Lexus', 'ES', 'Sedan', 2012, 'Silver', 70000, 'Automatic transmission, V6 engine', 'Luxurious sedan with plush interior and smooth ride.', 0, '-', 'sold', 22000.00),
('1G6DV1EP4F0840180', 'Audi', 'A8', 'Sedan', 2003, 'Black', 130000, 'Automatic transmission, V8 engine', 'Flagship sedan with opulent features and refined performance.', 0, '-', 'sold', 13000.00),
('1D7RW3BK8BS446576', 'Aston Martin', 'V8 Vantage', 'Coupe', 2014, 'Silver', 40000, 'Automatic transmission, V8 engine', 'Exotic sports car with breathtaking performance and stunning design.', 0, '-', 'sold', 60000.00),
('ZFBCFADH1EZ980832', 'Lincoln', 'MKZ', 'Sedan', 2012, 'White', 75000, 'Automatic transmission, V6 engine', 'Comfortable and luxurious sedan with smooth ride and upscale amenities.', 0, '-', 'sold', 18000.00),
('WAUNF98P37A160773', 'Audi', 'A4', 'Sedan', 2010, 'Black', 80000, 'Automatic transmission, 4 cylinders', 'Elegant sedan with refined interior and advanced technology features.', 0, '-', 'sold', 15000.00),
('1FTMF1E85AK857700', 'Ford', 'F-150', 'Pickup Truck', 2010, 'Blue', 90000, 'Automatic transmission, V8 engine', 'Powerful and reliable Pickup Truck designed for work and leisure.', 0, '-', 'sold', 22000.00),
('1FTEW1E8XAK386177', 'Ford', 'F-150', 'Pickup Truck', 2010, 'White', 90000, 'Automatic transmission, V8 engine', 'Spacious and rugged Pickup Truck suitable for work and leisure activities.', 0, '-', 'sold', 22000.00),
('WBAAX134X4P941020', 'BMW', '3 Series', 'Sedan', 2004, 'Blue', 120000, 'Manual transmission, 6 cylinders', 'Sporty sedan with precise handling and dynamic performance.', 0, '-', 'sold', 10000.00),
('WD3PE8CB6D5769421', 'Mercedes-Benz', 'Sprinter', 'Van', 2013, 'White', 60000, 'Automatic transmission, 4 cylinders', 'Versatile and spacious cargo van ideal for commercial use.', 0, '-', 'sold', 25000.00),
('1GYS4DKL7MR225532', 'Cadillac', 'Escalade', 'SUV', 2021, 'Black', 10000, 'Automatic transmission, V8 engine', 'Luxurious and powerful SUV with cutting-edge technology and upscale amenities.', 0, '-', 'sold', 60000.00),
('WAUKH98E87A124721', 'Mercedes-Benz', 'Metris', 'Van', 2024, 'Black', 180, 'The 2024 Mercedes-Benz Metris Van offers versatility and functionality, ideal for various commercial and personal transport needs.', 'Sleek and stylish, the Mercedes-Benz Metris Van combines performance with practicality. Its spacious interior and customizable features make it ideal for a variety of uses, from commercial delivery to family outings. With advanced safety technologies and a refined design, the Metris Van delivers a driving experience that\'s both secure and enjoyable.', 4, 'https://inv.assets.ansira.net/ChromeColorMatch/us/TRANSPARENT_cc_2023MBV060014_01_1280_040.png', 'sold', 55000.00),
('19UUA66298A039588', 'Mercedes-Benz', 'A-Class', 'Hatchback', 2024, 'Gray', 400, 'The 2024 Mercedes-Benz A-Class Hatchback embodies elegance and performance, delivering a luxurious driving experience in a sleek and compact design.', 'Experience luxury and agility with the Mercedes-Benz A-Class Hatchback. Designed for urban driving, this compact yet stylish vehicle offers impressive performance and cutting-edge technology. From its sleek exterior to its meticulously crafted interior, every detail reflects the brand\'s commitment to excellence. Whether you\'re navigating city streets or cruising on the highway, the A-Class Hatchback delivers an unparalleled driving experience.', 4, 'https://images.drive.com.au/driveau/image/upload/c_fill,f_auto,g_auto,h_360,q_auto:best,w_640/v1/cms/uploads/e5xis8nk8pelx0jjydg1', 'sold', 47000.00),
('WBADN53481G171888', 'Hyundai', 'Accent', 'Hatchback', 2024, 'Blue', 250, 'The 2024 Hyundai Accent Hatchback combines efficiency with modern style, offering a spacious and comfortable ride perfect for urban adventures and daily commuting.', 'The Hyundai Accent Hatchback combines efficiency and affordability without compromising on style. Its compact design makes it perfect for navigating crowded streets, while its spacious interior ensures comfort for all passengers. With advanced technology features and a smooth driving experience, the Accent Hatchback is the perfect choice for those seeking practicality and value in a modern vehicle.', 4, 'https://www.hyundai.com/content/dam/hyundai/wallan/en/data/vehicle-thumbnail/product/accent-2024/small/new-ACCENT-pc1.png', 'sold', 27000.00),
('SAJWA1EK7EM977306', 'Hyundai', 'Elantra', 'Hatchback', 2024, 'Red', 300, 'This Hyundai Elantra Hatchback comes equipped with a fuel-efficient yet powerful engine, perfect for city driving or long highway cruises. It boasts a spacious interior with ample legroom and cargo space, making it ideal for both daily errands and weekend getaways. Safety features such as lane departure warning and automatic emergency braking provide peace of mind on every journey. Additionally, the infotainment system includes smartphone integration for seamless connectivity on the go.', 'The 2024 Hyundai Elantra Hatchback is a stylish and practical choice for those seeking a versatile compact car. With its eye-catching red exterior, sleek design, and spacious interior, this Elantra offers both style and functionality. Packed with modern features and advanced technology, it provides a comfortable and enjoyable driving experience for both daily commutes and weekend adventures.', 4, 'https://inv.assets.ansira.net/ChromeColorMatch/us/TRANSPARENT_cc_2024HYC020015_01_1280_M6T.png', 'sold', 30000.00),
('WBAVA37567N303400', 'Audi', 'A5', 'Coupe', 2024, 'white', 120, 'This Audi A5 Coupe is a true driver\'s car, featuring a potent engine and dynamic handling characteristics. Its sleek coupe design turns heads wherever you go, while the luxurious interior provides comfort and sophistication. Advanced features like Audi virtual cockpit and heads-up display keep you informed and entertained on the road. With its sporty yet refined demeanor, the A5 Coupe offers an unforgettable driving experience tailored to those who demand performance and style.', 'The 2024 Audi A5 Coupe embodies sophistication and performance in every detail. With its timeless white exterior and sleek coupe silhouette, this A5 exudes luxury and style. Featuring a powerful engine and responsive handling, it offers exhilarating performance on the open road. The A5\'s meticulously crafted interior provides a comfortable and refined driving environment, while its advanced technology keeps you connected and entertained throughout your journey. Experience the thrill of driving with the Audi A5 Coupe.', 4,'https://images.carprices.com/pricebooks_data/usa/colorized/2024/Audi/View2/A5_Coupe/2.0_TFSI/F5PCAY_Z9.png', 'sold', 58000.00),
('WAUJEGF4E87465621', 'Audi', 'A3', 'Hatchback', 2024, 'White', 350, 'The Audi A3 Hatchback offers a perfect blend of performance and luxury. Its turbocharged engine delivers exhilarating acceleration while maintaining impressive fuel efficiency. Inside, you\'ll find premium materials and craftsmanship, along with advanced driver assistance features like adaptive cruise control and parking assist. The infotainment system features a responsive touchscreen display with navigation, Bluetooth connectivity, and a premium sound system for an immersive driving experience.', 'The 2024 Audi A3 Hatchback combines luxury and performance in a compact package. With its elegant white exterior and refined interior, this A3 offers a premium driving experience. Equipped with advanced safety features and cutting-edge technology, it delivers both comfort and confidence on the road. Whether navigating city streets or embarking on long journeys, the Audi A3 is sure to impress with its dynamic performance and sophisticated design.', 4, 'https://images.carprices.com/pricebooks_data/usa/colorized/2024/Audi/View2/A3/2.0_TFSI/8YSBUY_A2.png', 'sold', 45000.00),
('1C3BC4FBXBN521723', 'Audi', 'A5', 'Coupe', 2024, 'Red', 240, 'This Audi A5 Coupe is a true driver\'s car, featuring a potent engine and dynamic handling characteristics. Its sleek coupe design turns heads wherever you go, while the luxurious interior provides comfort and sophistication.Advanced features like Audi virtual cockpit and heads - up display keep you informed and entertained on the road.With its sporty yet refined demeanor, the A5 Coupe offers an unforgettable driving experience tailored to those who demand performance and style.', 'The 2024 Audi A5 Coupe in striking red is a fusion of elegance and performance. With its sleek lines and aggressive stance, it commands attention on the road. The turbocharged engine delivers thrilling acceleration, while the finely tuned suspension ensures precise handling through every curve. Inside, the A5 boasts luxurious amenities and advanced technology, including a virtual cockpit and premium sound system. Experience driving exhilaration like never before with the Audi A5 Coupe.', 4, 'https://images.carprices.com/pricebooks_data/usa/colorized/2024/Audi/View2/A5_Coupe/2.0_TFSI/F5PCAY_B1.png','sold', 60000.00),
('1G4HP54K74U724821', 'Nissan', 'Leaf', 'Hatchback', 2024, 'Blue', 2000, 'The Nissan Leaf is a revolutionary electric hatchback known for its zero-emission driving, practical design, and advanced technology, offering eco-conscious drivers a greener way to commute.', 'The Nissan Leaf leads the charge in the electric vehicle revolution with its efficient electric powertrain, long-range capability, and user-friendly features, all packaged in a versatile hatchback body style that\'s perfect for city driving and daily errands, making it a smart choice for those looking to reduce their carbon footprint without sacrificing style or performance.',  15, 'https://www.freepnglogos.com/uploads/nissan-logo-png/nissan-logo-emblem-symbol-png-transparent-13.png', 'sold', 28000.00),
# ('WUATNAFG2EN786809', 'Toyota', 'Corolla', '-', 2023, 'White', 15000, '-', '-', 0, '-', 'new', 20000.00),
# ('1G6DV1EP4F0840180', 'Cadillac', 'CT5', '-', 2022, 'Blue', 12000, '-', '-', 0, '-', 'new', 45000.00),
# ('1D7RW3BK8BS446576', 'Dodge', 'Ram 1500', '-', 2023, 'Red', 5000, '-', '-', 0, '-', 'new', 35000.00),
# ('ZFBCFADH1EZ980832', 'Fiat', '500', '-', 2023, 'Yellow', 8000, '-', '-', 0, '-', 'new', 18000.00),
# ('WAUNF98P37A160773', 'Audi', 'A4', '-', 2023, 'Silver', 10000, '-', '-', 0, '-', 'new', 38000.00),
('WA1YD64B23N299063', 'BMW', '3 Series', '-', 2023, 'Black', 9000, '-', '-', 0, '-', 'new', 45000.00),
# ('WD3PE8CB6D5769421', 'Mercedes-Benz', 'Sprinter', '-', 2023, 'White', 2000, '-', '-', 0, '-', 'new', 55000.00),
('JTHKD5BH1C2538310', 'Toyota', 'Camry', 'Sedan', 2023, 'Silver', 8000, '-', '-', 0, '-', 'sold', 28000.00),
('WAULT58E03A107692', 'Mercedes-Benz', 'E-Class', 'Sedan', 2022, 'Black', 12000, '-', '-', 0, '-', 'sold', 50000.00),
('NM0LS7E23J1365787', 'Audi', 'A4', 'Sedan', 2024, 'White', 6000, '-', '-', 0, '-', 'sold', 35000.00),
# ('WBAVA37567N303400', 'Tesla', 'Model 3', 'Sedan', 2023, 'Blue', 5000, '-', '-', 0, '-', 'new', 45000.00),
('SCFEBBAK9EG600978', 'Porsche', '911', 'Coupe', 2023, 'Yellow', 3000, '-', '-', 0, '-', 'sold', 150000.00),
('JH4DC54895S001234', 'Honda', 'Accord', 'Sedan', 2017, 'Blue', 50000, '-', '-', 7, '-', 'sold', 0),
('WAUHF78P19A929792', 'Audi', 'A4', 'Sedan', 2019, 'Black', 40000, '-', '-', 6, '-', 'sold', 0),
('WBXPA93444W811966', 'BMW', 'X5', 'SUV', 2015, 'White', 60000, '-', '-', 7, '-', 'sold', 0),
('WBA4J3C56KB000100', 'BMW', '4 Series', 'Coupe', 2024, 'Orange', 200, 'The BMW 4 Series combines sporty performance with luxurious comfort in a sleek and stylish package. With its retractable hardtop roof and powerful engine options, the 4 Series offers an exhilarating driving experience. Whether you\'re cruising along the coast or exploring winding mountain roads, this delivers thrills at every turn.', 'Experience the thrill of open-air driving with the BMW 4 Series. Its dynamic design and sophisticated features make it the perfect choice for drivers who demand both style and performance. With its luxurious interior and advanced technology, the 4 Series offers a driving experience unlike any other. Whether you\'re enjoying a weekend getaway or commuting to work, the BMW 4 Series is sure to make every journey memorable.', 4, 'https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-7331cqgv2Z7d%25i02uCaY3MuO2kOHUtWPfbYf6JWl10tLhu1XzWVo7puMLWFmdkAj5DOPitpKZ8XgY1nTNIowJ4HO3zkyXq%25sGM8snpq6v6ODubLz2aKqfkoOjmB2fJj5DOP5Eagd%25kcWExHWpbl8FO2k3Hy2oIjEdwdGbBDS6jQ%25QD22Ydw6ZuL3iptQ%25wc3yHmifZu%25KXC17HSc3uBrU26JdKX324bpzTQBrXpFhgplZ24riI1gYscpF4HvVJL0KiIFJGzTOABHvIT9avrO2JGvloRGEgpT9GsLxnQUilo90yW5BbHsLoACe0shJ0yLOEjxGqTACygN6WYmlOECUkyEH7sgNEbnC5V10UkNh5EWDVAbnkq8NeuzOh5nmPkj%25agq857MnskRUmP81D50Oxb7MPVY8AaWh1DMzt%2595eqVYDafusUjmztYRS3ol67aftxdXrWw1RSfWQr4m%25VxdSeZ4FCuzWQdjcFsk3aeZQ6KIO0XRjcZwBvL5rxlc9Nv2Z7d5yKlHS9fxQun%25P6Ub1Z', 'sold', 59000.00),
('4T1BK1EB3EU579953', 'BMW', '3 Series', 'Hatchback', 2024, 'White', 150, 'The BMW 3 Series Hatchback offers a perfect blend of performance, comfort, and style. With its sleek design and powerful engine options, the 3 Series Hatchback delivers an exhilarating driving experience. Its spacious interior and advanced technology features ensure that every journey is both enjoyable and convenient.', 'Elevate your driving experience with the BMW 3 Series Hatchback. Whether you\'re navigating city streets or cruising on the highway, this hatchback delivers exceptional performance and handling. Its stylish exterior design is complemented by a luxurious interior that\'s packed with advanced features. From its responsive handling to its comfortable ride, the BMW 3 Series Hatchback is designed to impress.', 4, 'https://65e81151f52e248c552b-fe74cd567ea2f1228f846834bd67571e.ssl.cf1.rackcdn.com/ldm-images/2021-BMW-3-Series-hero.png', 'sold', 48000.00),
('3D73Y4EL4BG548166', 'Ram', '1500', 'Pickup Truck', 2024, 'Black', 300, 'The Ram 1500 Pickup Truck is built to handle tough jobs with ease. With its powerful engine options and rugged construction, the 1500 is capable of towing heavy loads and navigating rough terrain. Its spacious cabin offers comfort and convenience for both driver and passengers, making it the perfect choice for work or play.', 'Dominate the road with the Ram 1500 Pickup Truck. Whether you\'re hauling equipment to the job site or towing a trailer for a weekend adventure, the 1500 delivers the performance and capability you need. Its advanced technology features keep you connected and in control, while its comfortable interior ensures a smooth ride every time. From its powerful engine options to its impressive towing capacity, the Ram 1500 is ready for whatever challenges come its way.', 4, 'https://di-uploads-pod20.dealerinspire.com/saltlakevalleycdjr/uploads/2021/10/mlp-img-top-2022-1500-temp.png', 'sold', 53000.00),
('WAUDF48H57A145781', 'Ram', '2500', 'Pickup Truck', 2024, 'Red', 250, 'The Ram 2500 Pickup Truck is a heavy-duty workhorse designed to tackle the toughest jobs. With its robust construction and powerful engine options, the 2500 is capable of handling heavy loads and towing large trailers with ease. Its spacious interior offers comfort and convenience for both driver and passengers, making it the perfect choice for demanding work environments.', 'Conquer any challenge with the Ram 2500 Pickup Truck. Whether you\'re hauling equipment on the job site or towing a camper for a weekend getaway, the 2500 delivers the performance and capability you need. Its rugged exterior design exudes strength and confidence, while its refined interior provides comfort and convenience. From its advanced towing features to its innovative technology, the Ram 2500 is built to exceed expectations.', 4, 'https://media.chromedata.com/MediaGallery/media/MjkzOTU4Xk1lZGlhIEdhbGxlcnk/OKVq9ic1oczJd-gxrbSkQgTMWspC1FbwUB9itAnVej4Gv7vOHByhXH5UByIi9g4MnilYhzCCc-ABz2rFO6_tLX-gQtdydtRVaTiSgkenbujTAAT0LweGuvoO3p8Py-og5cHk7h4Zh6S48Oz82_WqTqnkxtp1ZV7Zbk_75bjYQJBoBIZsb5GZVg/cc_2024RMT120030_01_640_PW7.png', 'sold', 52000.00),
('1B3CB3HA6AD530751', 'Ram', 'ProMaster', 'Van', 2024, 'Black', 120, 'The Ram ProMaster Van is a versatile and capable commercial vehicle designed to meet the demands of modern businesses. With its spacious cargo area and configurable interior, the ProMaster offers ample room for transporting goods and equipment. Its efficient engine options and advanced technology features make it the ideal choice for delivery services, contractors, and other professionals.', 'Streamline your business operations with the Ram ProMaster Van. Its flexible interior design allows you to customize the cargo space to suit your specific needs, while its efficient engine options ensure reliable performance on the road. With its advanced safety features and connectivity options, the ProMaster keeps you and your cargo secure and connected at all times. Whether you\'re making deliveries or running a mobile workshop, the Ram ProMaster is ready to help you get the job done efficiently and effectively.', 4, 'https://images.carprices.com/pricebooks_data/usa/colorized/2024/Ram/View2/Promaster_Cargo_Van/1500/VF1L13_PX8.png', 'sold', 60000.00),

-- outside dealership car inserts
('5FRYD3H48FB697538', 'Toyota', 'Corolla', 'Sedan', 2018, 'Blue', 50000, '-', '-', 0, '-', 'Outside Dealership', 0),
('WA1CMAFE1CD332305', 'Audi', 'Q5', 'SUV', 2012, 'Black', 70000, '-', '-', 0, '-', 'Outside Dealership', 0),
('WA1MYAFE8AD005776', 'Audi', 'A4', 'Sedan', 2010, 'White', 80000, '-', '-', 0, '-', 'Outside Dealership', 0),
('1FTNF2A59AE274535', 'Ford', 'F-250', 'Truck', 2010, 'Red', 90000, '-', '-', 0, '-', 'Outside Dealership', 0),
('4USBU33577L779003', 'BMW', 'X5', 'SUV', 2007, 'Silver', 100000, '-', '-', 0, '-', 'Outside Dealership', 0),
('1YVHZ8AHXA5361715', 'Mazda', 'Mazda6', 'Sedan', 2010, 'Black', 80000, '-', '-', 0, '-', 'Outside Dealership', 0),
('JN8AZ2KRXET870589', 'Nissan', 'Murano', 'SUV', 2014, 'Gray', 60000, '-', '-', 0, '-', 'Outside Dealership', 0),
('WAUAF78E35A401889', 'Audi', 'A6', 'Sedan', 2005, 'Blue', 120000, '-', '-', 0, '-', 'Outside Dealership', 0),
('1G6DA8E5XC0766424', 'Cadillac', 'CTS', 'Sedan', 2012, 'Black', 90000, '-', '-', 0, '-', 'Outside Dealership', 0),
('5UXWX9C54D0838067', 'BMW', 'X3', 'SUV', 2013, 'White', 70000, '-', '-', 0, '-', 'Outside Dealership', 0),
('WVWED7AJ6DW427020', 'Volkswagen', 'Jetta', 'Sedan', 2013, 'Gray', 60000, '-', '-', 0, '-', 'Outside Dealership', 0),
('WBAAX13423P051870', 'BMW', '330i', 'Sedan', 2003, 'Black', 150000, '-', '-', 0, '-', 'Outside Dealership', 0),
('1FTSW2B58AE824132', 'Ford', 'F-150', 'Truck', 2010, 'Red', 100000, '-', '-', 0, '-', 'Outside Dealership', 0),
('WUARL48H58K525655', 'Audi', 'A4', 'Sedan', 2008, 'Silver', 110000, '-', '-', 0, '-', 'Outside Dealership', 0),
('WVWAA7AH3AV482448', 'Volkswagen', 'Passat', 'Sedan', 2010, 'Blue', 90000, '-', '-', 0, '-', 'Outside Dealership', 0),
('WBAVM5C59EV711847', 'BMW', 'X5', 'SUV', 2014, 'Black', 60000, '-', '-', 0, '-', 'Outside Dealership', 0),
('SCBLC37F43C179911', 'Bentley', 'Continental GT', 'Coupe', 2003, 'Silver', 80000, '-', '-', 0, '-', 'Outside Dealership', 0);

-- add more data for cars regarding body types [convertible, coupe, hatchback, pickup_truck, sedan, suv, and van] -> (DONE)



INSERT INTO Employee (first_name, last_name, email, phone, address, city, state, zipcode, employeeType) VALUES
('Tabby', 'Steger', 'tsteger0@de.vu', '6354591816', '2 Thierer Junction', 'Newark', 'NJ', '07101', 'superAdmin'),
('Aleta', 'Clavering', 'aclavering1@desdev.cn', '2208706316', '62405 Merry Plaza', 'Jersey City', 'NJ', '07302', 'technician'),
('Patsy', 'Orchart', 'porchart2@ibm.com', '4734835137', '693 Nova Road', 'Paterson', 'NJ', '07501', 'technician'),
('Blanche', 'Prophet', 'bprophet3@economist.com', '7763821407', '5173 North Terrace', 'Elizabeth', 'NJ', '07201', 'manager'),
('Theda', 'Draper', 'tdraper4@devhub.com', '7041746513', '66 Superior Alley', 'Edison', 'NJ', '08817', 'manager'),
('Rafferty', 'Frostdicke', 'rfrostdicke5@ucoz.com', '9805076681', '8 Delladonna Parkway', 'Toms River', 'NJ', '08753', 'technician'),
('Roi', 'Lamzed', 'rlamzed6@vimeo.com', '8846875214', '5 Sunbrook Plaza', 'Trenton', 'NJ', '08608', 'manager'),
('Avigdor', 'Mizzi', 'amizzi7@mtv.com', '6554398772', '41326 Hanover Point', 'Camden', 'NJ', '08102', 'manager'),
('Glori', 'Cox', 'gcox8@timesonline.co.uk', '9495623767', '6 Dexter Crossing', 'Clifton', 'NJ', '07011', 'technician'),
('Florenza', 'Schoffel', 'fschoffel9@hud.gov', '2779866316', '84196 Village Green Place', 'East Orange', 'NJ', '07017', 'technician'),
('Rodie', 'Woollends', 'rwoollendsa@woothemes.com', '9713949393', '44653 Maywood Hill', 'Union', 'NJ', '07083', 'manager'),
('Nikki', 'Craise', 'ncraiseb@smh.com.au', '7595756390', '58946 Drewry Place', 'Bayonne', 'NJ', '07002', 'manager'),
('Delinda', 'Dey', 'ddeyc@ca.gov', '8581258708', '4862 Brickson Park Park', 'Vineland', 'NJ', '08360', 'technician'),
('Earvin', 'Tregiddo', 'etregiddod@wisc.edu', '2206199554', '03675 Schiller Crossing', 'New Brunswick', 'NJ', '08901', 'manager'),
('Licha', 'Abelovitz', 'labelovitze@telegraph.co.uk', '6237294660', '2594 Johnson Plaza', 'Passaic', 'NJ', '07055', 'manager'),
('Rhett', 'Pawson', 'rpawsonf@t.co', '2434620716', '24632 Elka Parkway', 'Hoboken', 'NJ', '07030', 'technician'),
('Edythe', 'Clementet', 'eclementetg@japanpost.jp', '8435574441', '33222 Crownhardt Terrace', 'Perth Amboy', 'NJ', '08861', 'technician'),
('Nickie', 'Cuchey', 'ncucheyh@histats.com', '4895517826', '7 Elmside Center', 'Plainfield', 'NJ', '07060', 'manager'),
('Maryanne', 'Wressell', 'mwresselli@shareasale.com', '3963082365', '0 Lotheville Alley', 'Atlantic City', 'NJ', '08401', 'manager'),
('Torrence', 'Kibblewhite', 'tkibblewhitej@msn.com', '8928541469', '94556 Hudson Pass', 'Long Branch', 'NJ', '07740', 'technician');
-- add employee address info -> (DONE)


INSERT INTO EmployeeSensitiveInfo (employeeID, password, SSN, driverID, lastModified) VALUES
(1, '$2y$10$CNalhwglaOJLYaAql91pg.tpT.zdbG5DF87XB3p.XTCbKkJ1xOjM.', '$2y$10$7wpXAVROM06swzKglf.Z5eT.yOlCZ12MZz5hvwXmZtQxyNeo0Ggpq', 'I96670745983742', '2023-08-06 14:41:01'),
(2, '$2y$10$j7HGFRktPr7F6TJvLunRmux28fl358rQ0rIr7LkzMUTHIJ90A0MIq', '$2y$10$HO.yRS2ehZfbqLvaLzotVe7.6NSkH1kD1g6B3XbhwnbZ63y3K3TIG', 'G23005417297863', '2023-04-08 01:25:21'),
(3, '$2y$10$knhjRBqoQfqYP9ZMw/DioeVMuF66HAxDusiT1vBEqxQLdc6Xe98fm', '$2y$10$Sh/41i/ZNfXSkO3.uB3P0u3.l/xZ9ZQstHpSl649kronV3FWWhBeu', 'F25356251439825', '2023-10-15 13:50:22'),
(4, '$2y$10$hu4ZUkAD7ejXycAwjsSiGOIb1huKzXblLQ2Ubii.foZeYDDKBUX9a', '$2y$10$PF70G.KGVUJkhcFCNiGiX.L01dKhHdKcVQtMDCJffnEbjXYW/7xUC', 'U25064328606142', '2023-10-06 20:13:10'),
(5, '$2y$10$BEpzGxvUQ/UWHkNOe1jM/OSBh7aaqXy1E.c4Lceh8pom8C0XqteDq', '$2y$10$pP5/fB8k9PtcEfzmlOgiaOeQKR0Vy86Agp.5QY8DqCiF6QcLuHGzq', 'C75881620476833', '2024-03-02 02:57:59'),
(6, '$2y$10$RI/WnbY5GWue/PrqUiomTedFC..PtJYp09zDkeQ32ZEaD5vE3T3SG', '$2y$10$2PpzhwY12MCltkzbf0oRH.N7SDrnGPM2jx1N3UhnDy9Ngx3Dxh9hS', 'L45026077556480', '2023-11-16 07:04:38'),
(7, '$2y$10$EfXYt1t7pqSqdEwmAb3N2O9Roe5p5vkx1m5be3/8Kj3HazUKNF3Ui', '$2y$10$hFhDCITP1u764Rs2ya35dOoPunhWYiUXteyIfXoBdALjID4YrWKYK', 'V19237356992642', '2023-10-23 07:45:01'),
(8, '$2y$10$Bosx6pABi6MPhcievW8vcOQTP9CTE3nmndZ/DetuadQh9Qea.0oXy', '$2y$10$yCDjpm0Seat/6UvXS1gbWOEusTdxFCy3c.vufY8l4K3Td6cbsnwQ6', 'P87226193493909', '2023-06-12 13:41:35'),
(9, '$2y$10$vvdEpHLJyVyeogJdNOGhz.sjeexwSJMcE5QF/6NNVaFtCHz9pgYhG', '$2y$10$KjhfjVjfmVy6fa4rhYwVZeh7iLXK.YMvdWDB.TODRisksn2tIQW4a', 'N56834854481057', '2023-12-19 03:41:34'),
(10, '$2y$10$xzRWd12h3JPJwBGaT/vctezI55ZYDmX2dMJktQK7mUwRKe6xp4Xxu', '$2y$10$bk7eSsRWgIN6MFmnkl0P4uielZ7qHCP1nNiXmrqhWTWnqOWJKhjdm', 'J87895470258351', '2023-02-03 19:55:06'),
(11, '$2y$10$DKENM1hHWS09alVKX7RwLOVACQ5KApX1nj1dQNQRyiLT8waFROt6a', '$2y$10$6LiqJTfPoOnDRwZk8Flym.g75enbBgrgcLHwa3QJpv1gjrGknGoHq', 'M90526830311912', '2023-11-04 07:54:15'),
(12, '$2y$10$Nmccwo7Nu/tlEPS7Yxuo0emXiSk8XqLxDJZ.DCKp2Llc1UJRiZ3iy', '$2y$10$rb94zd2OWZQkXyhrWcp5AOoReO5JrTTTxi3aj3Er0BdS9yhARRuwO', 'N60004229422223', '2023-09-24 18:12:18'),
(13, '$2y$10$DX4wV/5sqxsyBRo8.BIdHe4PK2hGzJ47Ke1HS2bgVhT4ObVH8TukS', '$2y$10$We5TmA36oTvOaoLZu1XwdOk49XSlZvVG1qGuuHpf46bbBnDR19cLq', 'E73725928843550', '2024-02-15 15:37:33'),
(14, '$2y$10$xguhBwkGCs70Ih.VNwfVyu8bmHzFWGlfkPA5WG6vJ6P04nhpOjvgm', '$2y$10$3cGcdyZPU6VlHtSwBQ2h3uY.AzloiZo7Q8Fw9gpo.EjxbkFIw/EiS', 'U82548510742695', '2023-12-06 04:22:33'),
(15, '$2y$10$2/rlxqy83qwvWXX5UvlWKuxja0Iv8m8qmHXgwKTEJSVuCzU1MxW4q', '$2y$10$wZd8UyOPPsojIB04aCHmK.wL6byFt81rPuFDcU5Jf.qpKFqv4aSCe', 'W55496494796644', '2023-02-10 12:50:11'),
(16, '$2y$10$9rfEvdlC/E747xpyAiCAxuROZBb3Qh2LIShTkBeYGo/ZjKDvbEnSC', '$2y$10$TmDUl7KsM7z4.NRP3B9eXulhgz/4sQf9tG07jVOCLtzvYiiPyIbHK', 'Z11226785662506', '2023-08-20 15:37:39'),
(17, '$2y$10$xzvd/GjRhO4mU5caH7D2NO2EsrhcNsWsHoGCEdubupi2a7eH0qnxG', '$2y$10$NeHJfE.zFJuX5Ru8icEBGuMX4xkTMTCAItTLF8RRi.HFQy.a2fUbG', 'N87778191930551', '2023-04-07 22:12:22'),
(18, '$2y$10$SifLgCXEqvGE9NoJKvBvXedj9EYXW/.HOU5k1o8L./dOSQ8g8QNyK', '$2y$10$XlKu411HJrxOh6fJ3il.F.YHyRcNNNk/1KyVA1IJROPE5zWGBqzN.', 'R36578819583636', '2023-11-14 13:31:26'),
(19, '$2y$10$69tvOz5InYvGX5cQnpDPvuWj9Dye2fdqQnSecABIfEjyDSM0OLvDq', '$2y$10$8VsDitEPdsFXjTqb8yv5NuyaUNZTQ2O77hC3k4vS8P34azvsGLkoC', 'A17046949140707', '2023-04-08 23:03:48'),
(20, '$2y$10$cwI5VFcke5AyJ8BtKLchv.McDSC4hadEC2KXLPxxQciKx33IdPFeW', '$2y$10$W9D8z4vk5OjXN9yV3SUu2uxZa64MAjYOR9hIVyDNIwdeNHLTON6h.', 'P84486181854073', '2023-06-06 12:56:11');
-- hash the ssn -> (DONE)





INSERT INTO MemberSensitiveInfo (memberID, SSN, username, password, driverID, lastModified) VALUES
(1,'$2y$10$jRfzLq/t3QwdQWUZDGOiqO44hShWf0ESe0YO4s2sEZ3YgqdVSjBgW', 'kscinelli0','$2y$10$gXyTeH9.nls1yJoAkinBaulYhCZtsp9Kph38eZ2nWZOcNO.7kaWtS','R22313811699913', '2023-01-11 07:54:39'),
(2,'$2y$10$J.yfmmYGk8h5SnottUcIjeuy/DelRCmChN/OTrMjPzSnp4wIetADa','jtheyer1','$2y$10$OQirnS4a.NwwpW7qwK04peq6.SsbNvmNATl5j6.29LXUtQqGGTsN.','X95512680606098', '2023-03-14 19:10:16'),
(3,'$2y$10$NogcTeAjdEaNr6giwR3wxO18aEmGHI0wWuuZgvzyKjgpJqA/Pr6V6','rtrahair2','$2y$10$v8bPfhTYRIcRBEbXTR/4N.f5qp899vSN9edb8xnryoHNB0E/LnqM2','D08707674135194', '2023-08-31 15:46:47'),
(4,'$2y$10$rNhnBv.COk3h9HkmNxzBTu/iUMqQSjTalpoRLmQhtbW6PGKXXWPnq','ggoold3','$2y$10$RDtA1ZrMOwL7b4nkwao4iOlM4.JzJOKqT4ea0GNE.BxpUEYswnFj6','C16041684227955', '2024-02-29 22:48:44'),
(5,'$2y$10$sToJLcF3dKYaN1rALW2fR.dxwwVgjNVkSzVUPRrDyw9bt/SwFK2YC','hkordas4','$2y$10$cYGDGekYoPDLABkAbNixmeKWQhH4WQhJDTYm23T5WtXzOqvBcvwRm','K40404256713626','2023-06-08 21:02:47'),
(6,'$2y$10$p3uXXsD.7L2L07L3Ft.SPutcXCIw7VGpkUg0JyV/FaQir/SXsrBem','jcressingham5','$2y$10$YcocQ.An2zEJ.RJEubVIKe2/NeDhJbZ6SwFRLV1nx4LlGzmdwL0U6','R95125829361332', '2023-01-27 01:55:00'),
(7,'$2y$10$OjjkjRNLhJ64d6qJFojaiONvUvadgW1QWBa7Cbum0ejhKI5JqZL56','gmcguffog6','$2y$10$HDd7kLjmHnzT015L.z2bZOKO.EprGz42DRWlUrQIu4WItHB28uNN6','C99938545187865', '2023-06-26 10:14:37'),
(8,'$2y$10$.gbymqx4n5iWq725u5UGje6g0VC76T//75C45EFgzTWHzmtd/GzZS','mcurthoys7','$2y$10$bFT0qBBMWc7xHP0c3oMx9.v8p/1UrLsjUZrpH.TM9iIiZuNOI.Hb.','T53807275459626', '2023-01-07 13:34:23'),
(9,'$2y$10$SaatnfYlCpwkGg3LZEZTIOsnFcG2PzI6B7xn2W7WQKDU9XJd3Bp7S','lroff8','$2y$10$kMxQwDJ2zM8S4qIS/9bLbu9kYjw2FGky0NVTi1OW3CHebe8GzFrVy','P93000133288498', '2023-11-28 03:16:19'),
(10,'$2y$10$R8vUqMn/v8hji4JOjK1.ueXAlSzwiLyBUiPP53neb84.8O8ZDuGT2','dbaszniak9','$2y$10$cJw47q/HUfsPImSv2M3DJul8sdtQSb5Da6Zvc3wfZqh0dhYhTOWL.','F98941422570001', '2023-01-03 12:55:47');
-- hash the ssn -> (DONE)


INSERT INTO Financing (memberID, income, credit_score, loan_total, down_payment, percentage, monthly_payment_sum, remaining_months) VALUES
(1, 100000, 750, 15000.00, 5000, 10, 205.00, 48),
(2, 200000, 750, 18000.00, 6000, 10, 250.00, 60),
(3, 80000, 700, 12000.00, 4000, 8, 180.00, 72),
(4, 120000, 720, 16000.00, 5500, 9, 220.00, 48),
(5, 150000, 730, 20000.00, 7000, 10, 300.00, 60),
(6, 90000, 700, 17000.00, 5500, 10, 280.00, 48),
(7, 110000, 720, 19000.00, 6000, 8, 250.00, 60),
(8, 130000, 730, 22000.00, 7500, 9, 320.00, 72),
(9, 85000, 710, 15000.00, 5000, 10, 200.00, 48),
(10, 95000, 720, 16000.00, 5500, 8, 230.00, 60),
(11, 75000, 690, 14000.00, 4500, 9, 190.00, 72);


INSERT INTO Payments (paymentStatus, valuePaid, valueToPay, initialPurchase, lastPayment, routingNumber, bankAcctNumber, memberID, financingID)
VALUES
('Completed', 205.00, 15000.00, '2024-04-17 11:00:00', '2024-05-17 11:00:00', '$2y$10$jX5c0xseZ25wyuOeWyHrGOqkaeCH8QBDy0agXmc534QIaWNik0fzu', '$2y$10$zKxDeJ096bDJCJaFhq4on.adwXT1p304tWSK69nlS20fgNd1prLkK', 1, 1),
('Completed', 250.00, 18000.00, '2024-04-17 11:15:00', '2024-05-17 11:15:00', '$2y$10$6KC8Ge5X4jRljFabsTOuyOqXP2Yb3S2dArqyioqn9xS1cflLGncb6', '$2y$10$kO3gK5lHCo1h9FTJ9mF4aeytUfgA0IuZ8HRwvHEtYpMNnyU7tY1fq', 2, 2),
('Completed', 180.00, 12000.00, '2024-04-17 12:00:00', '2024-05-17 12:00:00', '$2y$10$olCcDP6BPyKKeOzfqeWCm.qNzOuNYxWLWVgNHr02LD3t6hD2VUhgW', '$2y$10$OVH5aoc8pLsxyI/QFfHhiutAhfnEe/9hAa1cEw0COPV2kXYJ4/X32', 3, 3),
('Completed', 220.00, 16000.00, '2024-04-17 12:15:00', '2024-05-17 12:15:00',  '$2y$10$vlE3xevuewMy6COhyjGJOOjA5RYKS31DDWWsA9XDDEh3tGugRHB3W', '$2y$10$j5j3vYk6QvZBFJf5eEtnye94xt5ciTaxqfP77Kn7ySRI0M9GHH.5.', 4, 4),
('Completed', 300.00, 20000.00, '2024-04-17 12:30:00', '2024-05-17 12:30:00',  '$2y$10$HogjrCIFztClDH5yQUTcueaur/JNgiJrY4y6iZFZvHr1cVlonYctW', '$2y$10$ICmx5aNRsJw6XlXOM.LW1.jIUykQQCx7j4l4fggNkeBwW75UkMpma', 5, 5),
('Completed', 280.00, 17000.00, '2024-04-17 11:00:00', '2024-05-17 11:00:00',  '$2y$10$JAT/BLscO/WUnvq0nReTcebSuXrsom1dBLTRC0SGVOWIQd7eUqScO', '$2y$10$cSb7Smfi/HzUId7a8PnAk.amB73bjco3INPKVHS7xOJXGi68kaV1S', 6, 6),
('Completed', 250.00, 19000.00, '2024-04-17 11:15:00', '2024-05-17 11:15:00',  '$2y$10$X7FEcf8l9DdDBFbIS5ammOVROljTxnfUimluTZjgtUyl9jLZ/nAEu', '$2y$10$o1Dt7u3s5giq52x1kP6z6ugX7xZ2ZyXxdWJCWPsyV2dADb94MPqUm', 7, 7),
('Completed', 320.00, 22000.00, '2024-04-17 12:00:00', '2024-05-17 12:00:00',  '$2y$10$q1kk0YOdAh7r3qBNLzNt2enp0e9mjap3K5RFgO4hLKggKopDNOzA2', '$2y$10$54FWzEOpNe/Y7Oa.Xhbsk.SeHsuCeexjos8HLMA3uW3rgerMK9MZ2', 8, 8),
('Completed', 200.00, 15000.00, '2024-04-17 12:15:00', '2024-05-17 12:15:00',  '$2y$10$YpPelZrAq6rMJF5xZXVwLuYEgHf7.Yy.WCrbJemORw31N4izakNtq', '$2y$10$DdOfNS7VewdPQmeWP46Q3OBWDfgQ4Y7e8p/0dsyRfakqxH5S.cEAy', 9, 9),
('Completed', 230.00, 16000.00, '2024-04-17 12:30:00', '2024-05-17 12:30:00', '$2y$10$QasfJ34YEmIJoF3qry2fNu5wMNW68eYB7Bqf8Q7uWQJ7nKAzFHjGO', '$2y$10$RNFrzmJYBlp1BrmlJYcjd.aSehp1lFvKRO9JOt4PPld8/FGSrkRaq', 10, 10);
# ('Completed', 190.00, 14000.00, '2024-04-17 11:00:00', '2024-05-17 11:00:00',  '$2y$10$ALse.pCRqjBr23B4ofGS1OV.GLtEI53RXurokAuoXKgE2zHvtGO9.', '$2y$10$xNbe9JrNu20VG1euRoSTI.6IGzX0u4cFq/TEIoYl1DLVGX29ZT5I6', 11, 11);
-- make more payment data


INSERT INTO Bids (memberID, bidValue, bidStatus, bidTimestamp) VALUES
(2, 15000.00, 'Confirmed', '2024-04-17 10:30:00'),
(3, 18000.00, 'Confirmed', '2024-04-17 10:45:00'),
(1, 20000.00, 'Confirmed', '2024-04-17 11:00:00'),
(2, 22000.00, 'Confirmed', '2024-04-17 11:15:00'),
(2, 18000.00, 'Confirmed', '2024-04-17 11:30:00'),
(3, 18000.00, 'Confirmed', '2024-04-17 11:30:00'),
(4, 18000.00, 'Confirmed', '2024-04-17 11:30:00'),
(7, 18000.00, 'Confirmed', '2024-04-17 11:30:00'),
(1, 18000.00, 'Confirmed', '2024-04-17 11:30:00'),
(5, 18000.00, 'Confirmed', '2024-04-17 11:30:00'),
(6, 18000.00, 'Confirmed', '2024-04-17 11:30:00'),
(9, 18000.00, 'Processing', '2024-04-17 11:30:00'),
(3, 18000.00, 'Processing', '2024-04-17 11:30:00'),
(9, 18000.00, 'Processing', '2024-04-17 11:30:00'),
(8, 18000.00, 'Processing', '2024-04-17 11:30:00'),
(8, 18000.00, 'Processing', '2024-04-17 11:30:00'),
(7, 18000.00, 'Processing', '2024-04-17 11:30:00'),
(6, 18000.00, 'Processing', '2024-04-17 11:30:00'),
(1, 18000.00, 'Denied', '2024-04-17 11:30:00'), -- denied Bids we should have is so that when any bidStatus is changed to denied in the backend, it removes that corresponding information (bidID, memberID) from the purchases page
(2, 18000.00, 'Denied', '2024-04-17 11:30:00'),
(9, 18000.00, 'Denied', '2024-04-17 11:30:00'),
(8, 18000.00, 'Denied', '2024-04-17 11:30:00'),
(8, 18000.00, 'Denied', '2024-04-17 11:30:00'),
(7, 18000.00, 'Denied', '2024-04-17 11:30:00'),
(7, 18000.00, 'Denied', '2024-04-17 11:30:00'),
(6, 15000.00, 'Confirmed', '2024-04-16 09:00:00'),
(7, 18000.00, 'Confirmed', '2024-04-16 09:30:00'),
(7, 20000.00, 'Confirmed', '2024-04-16 10:00:00'),
(1, 17000.00, 'Confirmed', '2024-04-16 10:30:00'),
(2, 16000.00, 'Confirmed', '2024-04-16 11:00:00'),
(3, 19000.00, 'Confirmed', '2024-04-16 11:30:00'),
(4, 17500.00, 'Confirmed', '2024-04-16 12:00:00'),
(7, 18500.00, 'Confirmed', '2024-04-16 12:30:00'),
(5, 19500.00, 'Confirmed', '2024-04-16 13:00:00'),
(5, 15500.00, 'Confirmed', '2024-04-16 13:30:00'),
(11, 0.00, 'None', NOW()); -- Placeholder bid table for vehicles bought at MSRP or finance without bidding.


INSERT INTO Purchases (bidID, VIN_carID, memberID, confirmationNumber, purchaseType, purchaseDate, signature) VALUES
(1, 'JTDJTUD38ED022075', 2, 'IKFDU3JBOVQU3', 'Vehicle/Add-on Purchase', '2024-04-17 11:00:00', 'Yes'), -- Accepted bids
(2, '1G6DE5EG4A0418636', 3, 'LF4OABA9A9XDL', 'Vehicle/Add-on Purchase', '2024-04-17 11:15:00', 'Yes'),
(3, '5YJYGDEF7DF485512', 1, 'IIKV2SED455I9', 'Vehicle/Add-on Purchase', '2024-04-17 12:00:00', 'Yes'),
(4, '7YJSKDVF8MF475533', 2, 'VVBPFP61ES8GT', 'Vehicle/Add-on Purchase', '2024-04-17 12:15:00', 'Yes'),
(5, '5YJYCDED8MF475533', 2, '6CQJZB73INO53', 'Vehicle/Add-on Purchase', '2024-04-17 12:30:00', 'Yes'),
(6, '4YJSA1DG9MF395318', 3, 'JZ70EVAEJBHJA', 'Vehicle/Add-on Purchase', '2024-04-17 11:00:00', 'Yes'),
(7, '5G3S2DKL1MR150912', 4, '4O0PRAWYGZDKT', 'Vehicle/Add-on Purchase', '2024-04-17 11:15:00', 'Yes'),
(8, '1LNHL9DR1CG561984', 7, 'F66YESEQKVSVA', 'Vehicle/Add-on Purchase', '2024-04-17 12:00:00', 'Yes'),
(9, 'WAUUFAFH4AN515152', 1, 'IK4V9RDNNYNXG', 'Vehicle/Add-on Purchase', '2024-04-17 12:15:00', 'Yes'),
(10, 'JN1CV6FE1FM347717', 5, 'PGV30DWNP2I7N', 'Vehicle/Add-on Purchase', '2024-04-17 12:30:00', 'Yes'),
(11, '3FA6P0LU7ER984703', 6, 'ZPS6G9PUDIFWJ', 'Vehicle/Add-on Purchase', '2024-04-17 12:30:00', 'Yes'),
(12, 'NM0LS7E23J1365787', 9, 'QXI0PHXKDP61T', 'Vehicle/Add-on Purchase', '2024-04-17 12:30:00', 'No'), -- Current bids
(13, 'WA1YD64B23N299063', 3, 'I8042YYXEK5IG', 'Vehicle/Add-on Purchase', '2024-04-17 12:30:00', 'No'),
(14, 'WBA4J3C56KB000100', 9, '9MUKWTP162HSX', 'Vehicle/Add-on Purchase', '2024-04-17 12:30:00', 'No'),
(15, '4T1BK1EB3EU579953', 8, '1K08AFEZUALTD', 'Vehicle/Add-on Purchase', '2024-04-17 12:30:00', 'No'),
(16, '3D73Y4EL4BG548166', 8, 'BOCWKJ339M5CA', 'Vehicle/Add-on Purchase', '2024-04-17 12:30:00', 'No'),
(17, 'WAUDF48H57A145781', 7, '8FG75BXIPM6SD', 'Vehicle/Add-on Purchase', '2024-04-17 12:30:00', 'No'),
(18, '1B3CB3HA6AD530751', 6, 'IYY4NNKDD1L9R', 'Vehicle/Add-on Purchase', '2024-04-17 12:30:00', 'No'),
(26, 'WAUHF78P19A929792', 6, 'SYWQ2O0AFKRRF', 'Vehicle/Add-on Purchase', '2024-04-17 12:30:00', 'Yes'), -- Financing with accepted bids | skip in bidID because of Denied bids, they don't get added into the Purchases Table
(27, 'WBXPA93444W811966', 7, 'JP52OS28GCFIQ', 'Vehicle/Add-on Purchase', '2024-04-17 12:30:00', 'Yes'),
(28, 'WAUKH98E87A124721', 7, 'O8BEN6VT13M0O', 'Vehicle/Add-on Purchase', '2024-04-17 12:30:00', 'Yes'),
(29, '19UUA66298A039588', 1, 'BK3E1B359HBMM', 'Vehicle/Add-on Purchase', '2024-04-17 12:30:00', 'Yes'),
(30, 'WBADN53481G171888', 2, 'G2KJK2G1IXRUX', 'Vehicle/Add-on Purchase', '2024-04-17 12:30:00', 'Yes'),
(31, 'SAJWA1EK7EM977306', 3, '4GEVUUOB6UDIH', 'Vehicle/Add-on Purchase', '2024-04-17 12:30:00', 'Yes'),
(32, 'WAUJEGF4E87465621', 4, 'G6AQDOLAL8X3B', 'Vehicle/Add-on Purchase', '2024-04-17 12:30:00', 'Yes'),
(33, 'JH4DC54895S001234', 7, 'ZX8BZE7ATRXEK', 'Vehicle/Add-on Purchase', '2024-04-17 12:30:00', 'Yes'),
(34, '3GTU2NEC7JG152638', 5, 'M0EXGD4APARTO', 'Vehicle/Add-on Purchase', '2024-04-17 12:30:00', 'Yes'),
(35, '5N1AA0ND2EN467326', 5, 'X9TK4KEEE217Q', 'Vehicle/Add-on Purchase', '2024-04-17 12:30:00', 'Yes'),
(11, 'WUATNAFG2EN786809', 10, 'B0NWTEUVG508W', 'Vehicle/Add-on Purchase', '2024-02-12 11:34:00', 'Yes'), -- MSRP Purchases
(11, '1B3CC5FBXAN551956', 1, '282AZ5YHJN1JE', 'Vehicle/Add-on Purchase', '2024-02-12 11:34:00', 'Yes'),
(11, '1G6DV1EP4F0840180', 2, 'BV2DMCY8OHBR5', 'Vehicle/Add-on Purchase', '2024-02-12 11:34:00', 'Yes'),
(11, '1D7RW3BK8BS446576', 3, 'BPMTAEYZU93BP', 'Vehicle/Add-on Purchase', '2024-02-12 11:34:00', 'Yes'),
(11, 'ZFBCFADH1EZ980832', 8, 'YISSKH1RI1J48', 'Vehicle/Add-on Purchase', '2024-02-12 11:34:00', 'Yes'),
(11, 'WAUNF98P37A160773', 9, 'OSPQVYE1U2E1R', 'Vehicle/Add-on Purchase', '2024-02-12 11:34:00', 'Yes'),
(11, '1FTMF1E85AK857700', 8, 'C9O5AROFHUPRF', 'Vehicle/Add-on Purchase', '2024-02-12 11:34:00', 'Yes'),
(11, '1FTEW1E8XAK386177', 4, 'AK6WBPYI7SZF9', 'Vehicle/Add-on Purchase', '2024-02-12 11:34:00', 'Yes'),
(11, 'WBAAX134X4P941020', 5, 'XE4G72OCA967D', 'Vehicle/Add-on Purchase', '2024-02-12 11:34:00', 'Yes'),
(11, 'WD3PE8CB6D5769421', 7, '1FHYDU3ZN9NI8', 'Vehicle/Add-on Purchase', '2024-02-12 11:34:00', 'Yes'),
(11, '1GYS4DKL7MR225532', 9, 'ATGVKC3Q9YH60', 'Vehicle/Add-on Purchase', '2024-02-12 11:34:00', 'Yes'),
(11, 'JTHKD5BH1C2538310', 4, 'QVL8UTJ0UH1NR', 'Vehicle/Add-on Purchase', '2024-02-12 11:34:00', 'Yes'), -- financing at MSRP
(11, 'WAULT58E03A107692', 5, 'T2R7NEXD6QZR6', 'Vehicle/Add-on Purchase', '2024-02-12 11:34:00', 'Yes'),
(11, '1G4HP54K74U724821', 10, 'AGPMB1MF7L44M', 'Vehicle/Add-on Purchase', '2024-02-12 11:34:00', 'Yes'),
(11, 'WBAVA37567N303400', 5, 'WBIP3NIR92YGI', 'Vehicle/Add-on Purchase', '2024-02-12 11:34:00', 'Yes'),
(11, '1C3BC4FBXBN521723', 6, '9MA2G0S65I7W0', 'Vehicle/Add-on Purchase', '2024-02-12 11:34:00', 'Yes'),
(11, 'SCFEBBAK9EG600978', 6, 'TBCWPEZCN9Y6Z', 'Vehicle/Add-on Purchase', '2024-02-12 11:34:00', 'Yes');


-- add more for other purchase types


INSERT INTO TestDrive (memberID, VIN_carID, appointment_date, confirmation) VALUES
(2, 'SALSF2D47CA305941', '2024-04-03 10:00:00', 'Confirmed'),
(5, '2G4GU5GV1D9224709', '2024-04-04 11:00:00', 'Awaiting Confirmation'),
(3, 'WAUEG94F16N011182', '2024-04-05 12:00:00', 'Denied'),
(4, '1G4HP57M79U336833', '2024-04-06 13:00:00', 'Cancelled'),
(9, '2T1KE4EEXDC541493', '2024-04-07 14:00:00', 'Confirmed'),
(6, 'WDDHF2EBXBA659567', '2024-04-08 10:00:00', 'Confirmed'),
(7, 'WVWED7AJ7CW030690', '2024-04-09 11:00:00', 'Awaiting Confirmation'),
(8, 'WBSBR93441E328102', '2024-04-10 12:00:00', 'Denied'),
(9, '3VW517AT2FM570847', '2024-04-11 13:00:00', 'Cancelled'),
(10, '1G6DJ5ED0B0941154', '2024-04-12 14:00:00', 'Confirmed'),
(1, '1G4HP52KX44657084', '2024-04-13 15:00:00', 'Awaiting Confirmation'),
(2, 'JN8AZ2KRXAT240808', '2024-04-14 16:00:00', 'Confirmed'),
(3, '3C4PDCABXCT526082', '2024-04-15 17:00:00', 'Awaiting Confirmation'),
(4, 'WA1DKBFP7BA136094', '2024-04-16 18:00:00', 'Confirmed'),
(5, '2T1KE4EE8BC840347', '2024-04-17 09:00:00', 'Awaiting Confirmation'),
(6, 'WAUJT54B03N038966', '2024-04-18 10:00:00', 'Confirmed'),
(7, 'WAUBFBFL5AN763430', '2024-04-19 11:00:00', 'Awaiting Confirmation'),
(8, 'SCFBF04B27G426214', '2024-04-20 12:00:00', 'Denied'),
(9, '5N1AA0NE2FN817354', '2024-04-21 13:00:00', 'Cancelled'),
(10, 'KNALN4D74F5929503', '2024-04-22 14:00:00', 'Confirmed'),
(1, 'JTDZN3EU7FJ029990', '2024-04-23 15:00:00', 'Awaiting Confirmation'),
(9, 'KM8JT3AB0BU232473', '2024-04-24 16:00:00', 'Confirmed'),
(3, 'ZHWGU5AU9CL270811', '2024-04-25 17:00:00', 'Awaiting Confirmation'),
(9, 'KMHHT6KD5DU114602', '2024-04-26 18:00:00', 'Confirmed'),
(5, 'ZHWGU5BZ8CL986853', '2024-04-27 09:00:00', 'Awaiting Confirmation');


INSERT INTO Services(service_name, price) VALUES
('Oil Change',39.99),
('Brake Inspection',79.99),
('Tire Rotation',30.00),
('Battery Replacement',149.99),
('Wheel Alignment',80.00),
('Diagnostic Services',50.00),
('Spark Plug Replacement',99.99),
('Air Conditioner Recharge', 89.99),
('Cabin Air Filter Replacement:', 115.99);


INSERT INTO ServiceAppointment (memberID, serviceID,  VIN_carID, appointment_date, status, last_modified) VALUES
(1, 1, 'WAUUFAFH4AN515152', '2024-04-01 09:00:00', 'Done', '2024-04-01 08:30:00'),
(2, 2, 'JTDJTUD38ED022075', '2024-04-02 10:00:00', 'Done', '2024-04-02 09:30:00'),
(3, 3, '1G6DE5EG4A0418636', '2024-04-03 11:00:00', 'Done', '2024-04-03 10:30:00'),
(4, 4, '1FTEW1E8XAK386177', '2024-04-04 12:00:00', 'Cancelled', '2024-04-04 11:30:00'),
(5, 5, 'WBAAX134X4P941020', '2024-04-05 13:00:00', 'Done', '2024-04-05 12:30:00'),
(7, 7, 'WBXPA93444W811966', '2024-04-07 15:00:00', 'Done', '2024-04-07 14:30:00'),
(8, 8, 'ZFBCFADH1EZ980832', '2024-04-08 16:00:00', 'Done', '2024-04-08 15:30:00'),
(9, 9, 'WAUNF98P37A160773', '2024-04-09 17:00:00', 'Done', '2024-04-09 16:30:00'),
(10, 1, 'WUATNAFG2EN786809', '2024-04-19 18:00:00', 'Scheduled', '2024-05-19 17:30:00'),
(1, 2, '5FRYD3H48FB697538', '2024-04-20 09:00:00', 'Scheduled', '2024-05-20 08:30:00'),
(2, 3, 'WA1CMAFE1CD332305', '2024-04-21 10:00:00', 'Scheduled', '2024-05-21 09:30:00'),
(3, 4, 'WA1MYAFE8AD005776', '2024-04-22 11:00:00', 'Cancelled', '2024-05-22 10:30:00'),
(4, 5, '1FTNF2A59AE274535', '2024-04-23 12:00:00', 'Cancelled', '2024-05-23 11:30:00'),
(5, 6, '4USBU33577L779003', '2024-04-24 13:00:00', 'Scheduled', '2024-05-24 12:30:00'),
(6, 7, '1YVHZ8AHXA5361715', '2024-04-25 14:00:00', 'Scheduled', '2024-05-25 13:30:00'),
(7, 8, 'JN8AZ2KRXET870589', '2024-04-26 15:00:00', 'Scheduled', '2024-05-26 14:30:00'),
(8, 9, 'WAUAF78E35A401889', '2024-04-27 16:00:00', 'Scheduled', '2024-05-27 15:30:00'),
(9, 1, '1G6DA8E5XC0766424', '2024-04-28 17:00:00', 'Cancelled', '2024-05-28 16:30:00'),
(10, 2, '5UXWX9C54D0838067', '2024-04-29 18:00:00', 'Scheduled', '2024-05-29 17:30:00');


INSERT INTO ServiceAppointmentEmployeeAssignments (appointment_id, employeeID) VALUES
(1,2),
(2,3),
(3,6),
(4,9),
(5,2),
(6,3),
(7,4),
(8,9),
(9,2),
(10,3),
(11,6),
(12,2),
(13,3),
(14,6),
(15,9),
(16,2),
(17,3),
(18,6),
(19,9);


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

INSERT INTO WarrantyService (addon_ID, serviceID) VALUES
(2,1),
(5,5);

INSERT INTO OrderHistory ( memberID, item_name, item_price, financed_amount, confirmationNumber, purchaseDate)
VALUES
( 2, '2024 Ford Mustang', 55000, 0, 'ZLOXCTK9P8J8I', '2024-04-30 00:48'),
( 2, 'Extended Warranty', 1500, 0, 'ZLOXCTK9P8J8I', '2024-04-30 00:48'),
( 2, 'Maintenance Plans', 800, 0, 'ZLOXCTK9P8J8I', '2024-04-30 00:48'),
( 2, 'Interior Protection Packages', 500, 0, 'ZLOXCTK9P8J8I', '2024-04-30 00:48'),
( 2, 'Paint Protection Film/Ceramic Coating', 1200, 0, 'ZLOXCTK9P8J8I', '2024-04-30 00:48'),
( 2, 'Towing Packages', 1000, 0, 'ZLOXCTK9P8J8I', '2024-04-30 00:48'),
( 2, '2024 Ford Mustang', 55000, 0, 'B1R3VA8OPI45L', '2024-04-30 00:51'),
( 2, 'Extended Warranty', 1500, 0, 'B1R3VA8OPI45L', '2024-04-30 00:51'),
( 2, 'Maintenance Plans', 800, 0, 'B1R3VA8OPI45L', '2024-04-30 00:51'),
( 2, 'Interior Protection Packages', 500, 0, 'B1R3VA8OPI45L', '2024-04-30 00:51'),
( 2, 'Paint Protection Film/Ceramic Coating', 1200, 0, 'B1R3VA8OPI45L', '2024-04-30 00:51'),
( 2, 'Towing Packages', 1000, 0, 'B1R3VA8OPI45L', '2024-04-30 00:51');

INSERT INTO Purchases (bidID, VIN_carID, memberID, confirmationNumber, purchaseType, purchaseDate, signature) VALUES
-- January 2023
(1, NULL, 3, 'ABCD123456', 'Vehicle/Add-on Purchase', '2023-01-01 09:00:00', 'Yes'),
(2, NULL, 4, 'EFGH789012', 'Vehicle/Add-on Purchase', '2023-01-15 10:30:00', 'Yes'),
(3, NULL, 5, 'IJKL345678', 'Vehicle/Add-on Purchase', '2023-01-20 14:45:00', 'Yes'),

-- February 2023
(4, NULL, 6, 'MNOP901234', 'Vehicle/Add-on Purchase', '2023-02-03 11:15:00', 'Yes'),
(5, NULL, 7, 'QRST567890', 'Vehicle/Add-on Purchase', '2023-02-10 13:00:00', 'Yes'),
(6, NULL, 8, 'UVWX123456', 'Vehicle/Add-on Purchase', '2023-02-18 15:30:00', 'Yes'),

-- March 2023
(7, NULL, 9, 'YZAB789012', 'Vehicle/Add-on Purchase', '2023-03-05 09:45:00', 'Yes'),
(8, NULL, 10, 'CDEF345678', 'Vehicle/Add-on Purchase', '2023-03-14 12:00:00', 'Yes'),
(9, NULL, 3, 'GHIJ901234', 'Vehicle/Add-on Purchase', '2023-03-22 14:15:00', 'Yes'),

-- April 2023
(10, NULL, 4, 'KLMN567890', 'Vehicle/Add-on Purchase', '2023-04-08 10:30:00', 'Yes'),
(11, NULL, 5, 'OPQR123456', 'Vehicle/Add-on Purchase', '2023-04-17 11:45:00', 'Yes'),
(12, NULL, 6, 'STUV789012', 'Vehicle/Add-on Purchase', '2023-04-25 13:00:00', 'Yes'),

-- May 2023
(13, NULL, 7, 'WXYZ345678', 'Vehicle/Add-on Purchase', '2023-05-03 14:15:00', 'Yes'),
(14, NULL, 8, '1234 567890', 'Vehicle/Add-on Purchase', '2023-05-12 16:30:00', 'Yes'),
(15, NULL, 9, '5678 901234', 'Vehicle/Add-on Purchase', '2023-05-21 09:45:00', 'Yes'),

-- June 2023
(16, NULL, 10, '9012 345678', 'Vehicle/Add-on Purchase', '2023-06-02 12:00:00', 'Yes'),
(17, NULL, 3, 'ABCD 567890', 'Vehicle/Add-on Purchase', '2023-06-11 14:15:00', 'Yes'),
(18, NULL, 4, 'EFGH 901234', 'Vehicle/Add-on Purchase', '2023-06-20 16:30:00', 'Yes'),

-- July 2023
(19, NULL, 5, 'IJKL 345678', 'Vehicle/Add-on Purchase', '2023-07-07 09:45:00', 'Yes'),
(20, NULL, 6, 'MNOP 567890', 'Vehicle/Add-on Purchase', '2023-07-15 12:00:00', 'Yes'),
(21, NULL, 7, 'QRST 901234', 'Vehicle/Add-on Purchase', '2023-07-24 14:15:00', 'Yes'),

-- August 2023
(22, NULL, 8, 'UVWX 345678', 'Vehicle/Add-on Purchase', '2023-08-04 16:30:00', 'Yes'),
(23, NULL, 9, 'YZAB 567890', 'Vehicle/Add-on Purchase', '2023-08-13 09:45:00', 'Yes'),
(24, NULL, 10, 'CDEF 901234', 'Vehicle/Add-on Purchase', '2023-08-22 12:00:00', 'Yes'),

-- September 2023
(25, NULL, 3, 'GHIJ 345678', 'Vehicle/Add-on Purchase', '2023-09-05 14:15:00', 'Yes'),
(26, NULL, 4, 'KLMN 567890', 'Vehicle/Add-on Purchase', '2023-09-14 16:30:00', 'Yes'),
(27, NULL, 5, 'OPQR 901234', 'Vehicle/Add-on Purchase', '2023-09-23 09:45:00', 'Yes'),

-- October 2023
(28, NULL, 6, 'STUV 345678', 'Vehicle/Add-on Purchase', '2023-10-01 12:00:00', 'Yes'),
(29, NULL, 7, 'WXYZ 567890', 'Vehicle/Add-on Purchase', '2023-10-10 14:15:00', 'Yes'),
(30, NULL, 8, '1234 901234', 'Vehicle/Add-on Purchase', '2023-10-19 16:30:00', 'Yes'),

-- November 2023
(31, NULL, 9, '5678 345678', 'Vehicle/Add-on Purchase', '2023-11-06 09:45:00', 'Yes'),
(32, NULL, 10, '9012 567890', 'Vehicle/Add-on Purchase', '2023-11-15 12:00:00', 'Yes'),
(33, NULL, 3, 'ABCD 901234', 'Vehicle/Add-on Purchase', '2023-11-24 14:15:00', 'Yes'),

-- December 2023
(34, NULL, 4, 'EFGH 345678', 'Vehicle/Add-on Purchase', '2023-12-03 16:30:00', 'Yes'),
(35, NULL, 5, 'IJKL 567890', 'Vehicle/Add-on Purchase', '2023-12-12 09:45:00', 'Yes'),
(36, NULL, 6, 'MNOP 901234', 'Vehicle/Add-on Purchase', '2023-12-21 12:00:00', 'Yes');
