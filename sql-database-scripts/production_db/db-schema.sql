-- Drop the database if it exists
DROP DATABASE IF EXISTS dealership_backend;

CREATE DATABASE IF NOT EXISTS dealership_backend;
USE dealership_backend;

-- Drop existing tables if they exist
DROP TABLE IF EXISTS Addons;
DROP TABLE IF EXISTS Purchases;
DROP TABLE IF EXISTS Bids;
DROP TABLE IF EXISTS Payments;
DROP TABLE IF EXISTS MemberSensitiveInfo;
DROP TABLE IF EXISTS EmployeeSensitiveInfo;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS ServiceAppointment;
DROP TABLE IF EXISTS Financing;
DROP TABLE IF EXISTS TestDrive;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS CarVINs;
DROP TABLE IF EXISTS CarInfo;
DROP TABLE IF EXISTS Services;
DROP TABLE IF EXISTS MemberAuditLog;
DROP TABLE IF EXISTS EmployeeAuditLog;
DROP TABLE IF EXISTS ServiceAppointmentEmployeeAssignments;
DROP TABLE IF EXISTS checkoutcart;


CREATE TABLE IF NOT EXISTS Member (
    -- this table is meant to serve the purpose of containing basic information of the dealership memebrs
    memberID INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(255),
    city VARCHAR(20),
    state VARCHAR(2),
    zipcode VARCHAR(5),
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS CarVINs (
    # needed to differentiate between the car brought into the service center being bought from outside ot inside the dealership
    itemID INT AUTO_INCREMENT PRIMARY KEY,
    VIN_carID VARCHAR(17) UNIQUE,
    purchase_status ENUM ('Dealership - Not Purchased', 'Dealership - Purchased', 'Outside Dealership'),
    memberID INT,
    FOREIGN KEY (memberID) REFERENCES Member(memberID)
);
-- will have to change endpoints to ensure that carVins are valid in purchases and such with key relationships if their
-- purchase status is 'Dealership - Purchased'
-- also endpoint that changes the status here in the db of the car purchase status as well

CREATE TABLE IF NOT EXISTS CarInfo (  # prev. known as  Cars
    # this table is meant to serve the purpose of containing information on the cars stored in the dealership for sale
    itemID INT AUTO_INCREMENT PRIMARY KEY,
    VIN_carID VARCHAR(17),
    make VARCHAR(50),
    model VARCHAR(50),
    body VARCHAR(50),
    year INT,
    color VARCHAR(50),
    mileage INT,
    details TEXT,
    description TEXT,
    viewsOnPage INT,
    pictureLibraryLink TEXT,
    status ENUM('new', 'sold', 'low-mileage', 'being-watched', 'Outside Dealership'),
    price DECIMAL(10, 2),
    FOREIGN KEY (VIN_carID) REFERENCES CarVINs(VIN_carID)
);

CREATE TABLE IF NOT EXISTS TestDrive (
    -- this table is meant to store information on the test drive appointments made
    testdrive_id INT AUTO_INCREMENT PRIMARY KEY,
    memberID INT,
    VIN_carID VARCHAR(17),
    appointment_date TIMESTAMP,
    confirmation ENUM ('Confirmed', 'Denied', 'Cancelled', 'Awaiting Confirmation') default NULL,
    FOREIGN KEY (memberID) REFERENCES Member(memberID),
    FOREIGN KEY (VIN_carID) REFERENCES CarInfo(VIN_carID)
);

CREATE TABLE IF NOT EXISTS Employee (
    -- this table is meant to serve the purpose of containing basic information of the dealership employees
    employeeID INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(255),
    city VARCHAR(20),
    state VARCHAR(2),
    zipcode VARCHAR(5),
    employeeType ENUM('superAdmin', 'Manager', 'Technician')
);

CREATE TABLE IF NOT EXISTS EmployeeSensitiveInfo (
    -- this table contains sensitive information relating to the Employees
    sensitiveID INT AUTO_INCREMENT PRIMARY KEY,
    employeeID INT,
    password VARCHAR(255),
    SSN VARCHAR(255) UNIQUE,
    driverID VARCHAR(255) UNIQUE,
    lastModified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (employeeID) REFERENCES Employee(employeeID)
);

CREATE TABLE IF NOT EXISTS MemberSensitiveInfo (
    -- this table contains sensitive information relating to the members
    sensitiveID INT AUTO_INCREMENT PRIMARY KEY,
    memberID INT,
    SSN VARCHAR(255) UNIQUE,
    username VARCHAR(50) UNIQUE,
    password TEXT,
    driverID VARCHAR(15) UNIQUE,
    lastModified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (memberID) REFERENCES Member(memberID)
);

CREATE TABLE IF NOT EXISTS Services (
    serviceID INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(255),
    price DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS ServiceAppointment (
    -- this table is meant to store information on the service appointments made
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    memberID INT,
    VIN_carID VARCHAR(17),
    serviceID INT,
    appointment_date TIMESTAMP,
    comments TEXT,
    status ENUM ('Scheduled', 'Done', 'Cancelled'),
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (memberID) REFERENCES Member(memberID),
    FOREIGN KEY (VIN_carID) REFERENCES CarVINs(VIN_carID),
    FOREIGN KEY (serviceID) REFERENCES Services(serviceID)
);

CREATE TABLE IF NOT EXISTS ServiceAppointmentEmployeeAssignments (
    assignmentID INT AUTO_INCREMENT PRIMARY KEY,
    appointment_id INT,
    employeeID INT,
    FOREIGN KEY (appointment_id) REFERENCES ServiceAppointment(appointment_id),
    FOREIGN KEY (employeeID) REFERENCES Employee(employeeID)
);

CREATE TABLE IF NOT EXISTS Financing (
    -- this table is meant to keep information on financing if the customer buys and finances
    financingID INT AUTO_INCREMENT PRIMARY KEY,
    memberID INT,
    income INT,
    credit_score INT,
    loan_total INT,
    down_payment INT,
    percentage INT,
    monthly_payment_sum INT, # how much they have to pay for per month
    remaining_months INT,
    FOREIGN KEY (memberID) REFERENCES Member(memberID)
);

CREATE TABLE IF NOT EXISTS Payments (
    paymentID INT AUTO_INCREMENT PRIMARY KEY,
    paymentStatus ENUM('Completed', 'Pending', 'Failed', 'None'),
    valuePaid VARCHAR(20), # what you just paid
    valueToPay VARCHAR(20), # the rest of what you still have to pay
    initialPurchase TIMESTAMP NULL DEFAULT NULL,
    lastPayment TIMESTAMP NULL DEFAULT NULL,
--  paymentType ENUM('Check/Bank Account', 'Card', 'None'),
--     cardNumber TEXT, -- Assuming card numbers are stored as strings
--    expirationDate TEXT, -- Storing as MM/YY format
--    CVV TEXT, -- Assuming CVV is a string with a fixed length
    routingNumber TEXT, -- Assuming routing number is stored as string
    bankAcctNumber TEXT, -- Assuming bank account number is stored as string
    memberID INT,
    financingID INT,
    FOREIGN KEY (memberID) REFERENCES Member(memberID),
    FOREIGN KEY (financingID) REFERENCES Financing(financingID)
);

CREATE TABLE IF NOT EXISTS Bids (
    -- this table is meant to store all bids and their information
    bidID INT AUTO_INCREMENT PRIMARY KEY,
    memberID INT,
    bidValue DECIMAL(10,2),
    bidStatus ENUM ('Confirmed', 'Denied', 'Processing', 'None'),
    bidTimestamp TIMESTAMP,
    FOREIGN KEY (memberID) REFERENCES Member(memberID)
);

CREATE TABLE IF NOT EXISTS Purchases (
    -- this table is meant to serve more as a crossroads to connect the bids, payments and financing table
    purchaseID INT AUTO_INCREMENT PRIMARY KEY,
    bidID INT,
    VIN_carID VARCHAR(17),
    memberID INT,
    confirmationNumber VARCHAR(13) UNIQUE,
    purchaseType ENUM ('Vehicle/Add-on Purchase', 'Vehicle/Add-on Continuing Payment', 'Service Payment'),
    purchaseDate TIMESTAMP,
    signature ENUM ('Yes', 'No'),
    FOREIGN KEY (bidID) REFERENCES Bids(bidID),
    FOREIGN KEY (VIN_carID) REFERENCES CarVINs(VIN_carID),
    FOREIGN KEY (memberID) REFERENCES Member(memberID)
);

CREATE TABLE IF NOT EXISTS Addons (
    -- contains the addons and their cost
    itemID INT AUTO_INCREMENT PRIMARY KEY,
    itemName VARCHAR(100),
    totalCost DECIMAL(10, 2)
);


CREATE TABLE IF NOT EXISTS checkoutcart (
  `cart_item_id` int NOT NULL AUTO_INCREMENT,
  `memberID` int NOT NULL,
  `VIN_carID` varchar(45) DEFAULT NULL,
  `addon_ID` int DEFAULT NULL,
  `item_name` varchar(120) NOT NULL,
  `item_price` decimal(10,2) NOT NULL,
  `last_updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`cart_item_id`),
  KEY `userID_FK_idx` (`memberID`),
  KEY `VIN_carID_FK_idx` (`VIN_carID`),
  KEY `addonID_FK_idx` (`addon_ID`),
  CONSTRAINT `addonID_FK` FOREIGN KEY (`addon_ID`) REFERENCES `addons` (`itemID`),
  CONSTRAINT `memberID_FK` FOREIGN KEY (`memberID`) REFERENCES `member` (`memberID`),
  CONSTRAINT `VIN_carID_FK` FOREIGN KEY (`VIN_carID`) REFERENCES `carinfo` (`VIN_carID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci