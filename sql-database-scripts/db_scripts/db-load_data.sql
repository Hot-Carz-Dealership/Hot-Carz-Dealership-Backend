USE dealership_backend;

LOAD DATA INFILE '/localdir/employee.csv' --
INTO TABLE Employee
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';

LOAD DATA INFILE '/localdir/cars.csv' --
INTO TABLE Cars
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';

LOAD DATA INFILE '/localdir/payment.csv' -- 
INTO TABLE Payments
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';

LOAD DATA INFILE '/localdir/purchases.csv' -- 
INTO TABLE Purchases
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';

LOAD DATA INFILE '/localdir/sensitiveInfoEmployee.csv' --
INTO TABLE EmployeeSensitiveInfo
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';

LOAD DATA INFILE '/localdir/senstitiveInfoMember.csv' --
INTO TABLE MemberSensitiveInfo
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';

LOAD DATA INFILE '/localdir/financing.csv'
INTO TABLE Financing
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';

LOAD DATA INFILE '/localdir/serviceappointment.csv'
INTO TABLE ServiceAppointment
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';

LOAD DATA INFILE '/localdir/testDrive.csv'
INTO TABLE TestDrive
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';

INSERT INTO Addons (itemName, totalCost) VALUES -- 
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