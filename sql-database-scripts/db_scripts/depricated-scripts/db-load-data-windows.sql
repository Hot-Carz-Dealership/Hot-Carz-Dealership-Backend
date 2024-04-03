-- WINDOWS SYSTEMS \r\n
-- TEMP CHANGE SO THAT THE FRONT END CAN START TESTING END POINTS. MODFIED MOCK DATA WILL COME LATER

USE dealership_backend;

LOAD DATA INFILE '/localdir/employee.csv' --
INTO TABLE Employee
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n';

LOAD DATA INFILE '/localdir/cars.csv' --
INTO TABLE Cars
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n';

INSERT INTO Member (first_name, last_name, email, phone, status, join_date)
VALUES
('John', 'Doe', 'john.doe@example.com', '1234567890', 'Confirmed', '2024-03-28 10:00:00'),
('Alice', 'Smith', 'alice.smith@example.com', '2345678901', 'Denied', '2024-03-29 11:00:00'),
('Bob', 'Johnson', 'bob.johnson@example.com', '3456789012', 'Cancelled', '2024-03-30 12:00:00'),
('Emma', 'Brown', 'emma.brown@example.com', '4567890123', NULL, '2024-03-31 13:00:00'),
('Michael', 'Davis', 'michael.davis@example.com', '5678901234', 'Confirmed', '2024-04-01 14:00:00');


# LOAD DATA INFILE 'localdir/payment.csv'
# INTO TABLE Payments
# FIELDS TERMINATED BY ','
# LINES TERMINATED BY '\r\n';

INSERT INTO Payments (paymentStatus, paymentPerMonth, financeLoanAmount, loanRatePercentage, valuePaid, valueToPay, initialPurchase, lastPayment, creditScore, income, paymentType, servicePurchased, cardNumber, expirationDate, CVV, routingNumber, bankAcctNumber, memberID)
VALUES
('completed', '500', '10000', '5', '10000', '0', '2023-01-01', '2023-12-31', '750', '50000', 'card', 'Vehicle Purchase/Payment', '1234567890123456', '12/25', '123', '123456789', '987654321', 1),
('failed', '700', '15000', '7', '5000', '10000', '2023-03-01', NULL, '650', '55000', 'none', 'Vehicle Purchase/Payment', NULL, NULL, NULL, '123456789', '987654321', 2);


# LOAD DATA INFILE 'localdir/purchases.csv'
# INTO TABLE Purchases
# FIELDS TERMINATED BY ','
# LINES TERMINATED BY '\r\n';

INSERT INTO Purchases (paymentID, VIN_carID, memberID, paymentType, bidValue, bidStatus, confirmationNumber)
VALUES
    (1, 'SALSF2D47CA305941', 101, 'MSRP', '1000', 'Confirmed', 'CN1234567890'),
    (2, 'SALSF2D47CA305941', 102, 'BID', '1500', 'Processing', 'CN2345678901'),
    (3, 'SALSF2D47CA305941', 103, 'BID', '2000', 'Processing', 'CN3456789012');

LOAD DATA INFILE '/localdir/sensitiveInfoEmployee.csv' --
INTO TABLE EmployeeSensitiveInfo
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n';

LOAD DATA INFILE '/localdir/senstitiveInfoMember.csv' --
INTO TABLE MemberSensitiveInfo
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n';

# LOAD DATA INFILE 'localdir/financing.csv'
# INTO TABLE Financing
# FIELDS TERMINATED BY ','
# LINES TERMINATED BY '\r\n';

# LOAD DATA INFILE 'localdir/serviceappointment.csv'
# INTO TABLE ServiceAppointment
# FIELDS TERMINATED BY ','
# LINES TERMINATED BY '\r\n';

INSERT INTO ServiceAppointment (memberID, technician_id, appointment_date, service_name)
VALUES
(101, 201, '2024-04-01', 'Oil Change'),
(102, 202, '2024-04-02', 'Brake Inspection'),
(103, 203, '2024-04-03', 'Tire Rotation'),
(104, 204, '2024-04-04', 'Engine Tune-up'),
(105, 205, '2024-04-05', 'Transmission Flush');


# LOAD DATA INFILE 'localdir/testDrive.csv'
# INTO TABLE TestDrive
# FIELDS TERMINATED BY ','
# LINES TERMINATED BY '\r\n';

INSERT INTO TestDrive (memberID, car_id, appointment_date, confirmation)
VALUES
(1, 'SALSF2D47CA305941', '2024-04-01 10:00:00', 'confirm'),
(2, 'SALSF2D47CA305941', '2024-04-02 11:00:00', 'deny'),
(3, 'SALSF2D47CA305941', '2024-04-03 12:00:00', 'Awaiting Confirmation'),
(4, 'SALSF2D47CA305941', '2024-04-04 13:00:00', 'confirm'),
(5, 'SALSF2D47CA305941', '2024-04-05 14:00:00', 'Awaiting Confirmation');


INSERT INTO Addons (itemName, totalCost)
VALUES
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
