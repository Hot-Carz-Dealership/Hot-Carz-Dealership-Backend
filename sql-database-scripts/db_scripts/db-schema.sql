-- Drop the database if it exists
DROP DATABASE IF EXISTS dealership_backend;

CREATE DATABASE IF NOT EXISTS dealership_backend;
USE dealership_backend;

-- Drop existing tables if they exist
DROP TABLE IF EXISTS Addons;
DROP TABLE IF EXISTS Purchases;
DROP TABLE IF EXISTS Payments;
DROP TABLE IF EXISTS MemberSensitiveInfo;
DROP TABLE IF EXISTS EmployeeSensitiveInfo;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS ServiceAppointment;
DROP TABLE IF EXISTS Technician;
DROP TABLE IF EXISTS Financing;
DROP TABLE IF EXISTS TestDrive;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Cars;
DROP TABLE IF EXISTS MemberAuditLog;
DROP TABLE IF EXISTS EmployeeAuditLog;

CREATE TABLE IF NOT EXISTS Cars (
    VIN_carID VARCHAR(17) PRIMARY KEY,
    make VARCHAR(50),
    model VARCHAR(50),
    body VARCHAR(50),
    year INT,
    color VARCHAR(50),
    mileage INT,
    details VARCHAR(255),
    description TEXT,
    inStock ENUM('yes', 'no'),
    stockAmount INT,
    viewsOnPage INT,
    pictureLibraryLink TEXT,
    status ENUM('new', 'sold', 'low-mileage', 'being-watched'),
    price DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS Member (
    memberID INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    status ENUM('Confirmed', 'Denied', 'Cancelled') default NULL,
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS TestDrive (
    testdrive_id INT AUTO_INCREMENT PRIMARY KEY,
    memberID INT,
    car_id VARCHAR(17),
    appointment_date TIMESTAMP,
    confirmation ENUM ('confirm', 'deny', 'Awaiting Confirmation') default NULL
#     FOREIGN KEY (memberID) REFERENCES Member(memberID),
#     FOREIGN KEY (car_id) REFERENCES Cars(VIN_carID)
);

CREATE TABLE IF NOT EXISTS Financing (
    financing_id INT AUTO_INCREMENT PRIMARY KEY,
    memberID INT,
    credit_score INT,
    loan_total INT,
    down_payment INT,
    percentage INT,
    monthly_sum INT,
    remaining_months INT,
    FOREIGN KEY (memberID) REFERENCES Member(memberID)
);

CREATE TABLE IF NOT EXISTS ServiceAppointment (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    memberID INT,
    technician_id INT,
    appointment_date DATE,
    service_name VARCHAR(100)
#     FOREIGN KEY (memberID) REFERENCES Member(memberID)
);

CREATE TABLE IF NOT EXISTS Employee (
    employeeID INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(50),
    lastname VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(255),
    employeeType ENUM('superAdmin', 'manager', 'technician')
);

CREATE TABLE IF NOT EXISTS EmployeeSensitiveInfo (
    sensitiveID INT AUTO_INCREMENT PRIMARY KEY,
    employeeID INT,
    password VARCHAR(255),
    SSN VARCHAR(255) UNIQUE,
    driverID VARCHAR(255),
    lastModified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (employeeID) REFERENCES Employee(employeeID)
);

CREATE TABLE IF NOT EXISTS MemberSensitiveInfo (
    sensitiveID INT AUTO_INCREMENT PRIMARY KEY,
    memberID INT,
    SSN VARCHAR(255) UNIQUE,
    username VARCHAR(50) UNIQUE,
    password TEXT,
    driverID VARCHAR(15) UNIQUE,
    cardInfo TEXT,
    lastModified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#     FOREIGN KEY (memberID) REFERENCES Member(memberID) -- uncomment and test when member input it done and tested
);

CREATE TABLE IF NOT EXISTS Payments (
    paymentID INT AUTO_INCREMENT PRIMARY KEY,
    paymentStatus ENUM('completed', 'pending', 'failed', 'none'),
    paymentPerMonth VARCHAR(20),
    financeLoanAmount VARCHAR(20),
    loanRatePercentage VARCHAR(20),
    valuePaid VARCHAR(20),
    valueToPay VARCHAR(20),
    initialPurchase TIMESTAMP NULL DEFAULT NULL,
    lastPayment TIMESTAMP NULL DEFAULT NULL,
    creditScore VARCHAR(3),
    income VARCHAR(20),
    paymentType ENUM('check', 'card', 'none'),
    servicePurchased ENUM ('Vehicle Purchase/Payment', 'Vehicle Service'),
    cardNumber TEXT, -- Assuming card numbers are stored as strings
    expirationDate TEXT, -- Storing as MM/YY format
    CVV TEXT, -- Assuming CVV is a string with a fixed length
    routingNumber TEXT, -- Assuming routing number is stored as string
    bankAcctNumber TEXT, -- Assuming bank account number is stored as string
    memberID INT
#     FOREIGN KEY (memberID) REFERENCES Member(memberID) -- uncomment and test when member input it done and tested
);


CREATE TABLE IF NOT EXISTS Purchases (
    purchaseID INT AUTO_INCREMENT PRIMARY KEY,
    paymentID INT,
    VIN_carID VARCHAR(17),
    memberID INT,
    paymentType ENUM ('MSRP', 'BID'),
    bidValue VARCHAR(20),
    bidStatus ENUM ('Confirmed', 'Denied', 'Processing'),
    confirmationNumber VARCHAR (13) UNIQUE
#     FOREIGN KEY (paymentID) REFERENCES Payments(paymentID),
#     FOREIGN KEY (VIN_carID) REFERENCES Cars(VIN_carID)
#     FOREIGN KEY (memberID) REFERENCES Member(memberID) -- uncomment and test when member input it done and tested
);



CREATE TABLE IF NOT EXISTS Addons (
    itemID INT AUTO_INCREMENT PRIMARY KEY,
    itemName VARCHAR(100),
    totalCost DECIMAL(10, 2)
);

-- Audit tables for tracking events

CREATE TABLE IF NOT EXISTS MemberAuditLog (
    logID INT AUTO_INCREMENT PRIMARY KEY,
    memberID INT,
    event_description TEXT,
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (memberID) REFERENCES Member(memberID)
);

CREATE TABLE IF NOT EXISTS EmployeeAuditLog (
    logID INT AUTO_INCREMENT PRIMARY KEY,
    employeeID INT,
    event_description TEXT,
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employeeID) REFERENCES Employee(employeeID)
);


-- Trigger to log member updates
DELIMITER //

CREATE TRIGGER member_update_trigger
AFTER UPDATE ON Member
FOR EACH ROW
BEGIN
    DECLARE log_description VARCHAR(255);

    -- Initialize the log description
    SET log_description = '';

    -- Check if first name was updated
    IF OLD.first_name != NEW.first_name THEN
        SET log_description = CONCAT(log_description, 'First name updated ' , OLD.first_name, ' to ', NEW.first_name);
    END IF;

    -- Check if last name was updated
    IF OLD.last_name != NEW.last_name THEN
        SET log_description = CONCAT(log_description, 'Last name updated ' , OLD.last_name, ' to ', NEW.last_name);
    END IF;

    -- Check if email was updated
    IF OLD.email != NEW.email THEN
        SET log_description = CONCAT(log_description, 'Email updated ' , OLD.email, ' to ', NEW.email);
    END IF;

    -- Check if phone number was updated
    IF OLD.phone != NEW.phone THEN
        SET log_description = CONCAT(log_description, 'Phone number updated' , OLD.phone, ' to ', NEW.phone);
    END IF;

    -- Check if join date was updated
    IF OLD.join_date != NEW.join_date THEN
        SET log_description = CONCAT(log_description, 'Join date updated from ', OLD.join_date, ' to ', NEW.join_date, '; ');
    END IF;

    -- Insert log entry if any fields were updated
    IF log_description != '' THEN
        INSERT INTO MemberAuditLog (memberID, event_description)
        VALUES (NEW.memberID, log_description);
    END IF;
END//

DELIMITER ;


-- Trigger to log changes in MemberSensitiveInfo table
DELIMITER //

CREATE TRIGGER member_sensitive_info_trigger
AFTER UPDATE ON MemberSensitiveInfo
FOR EACH ROW
BEGIN
    DECLARE log_description VARCHAR(255);
    DECLARE lastModified TIMESTAMP;
    SET lastModified = CURRENT_TIMESTAMP;

    -- Initialize the log description
    SET log_description = '';

    -- Check if SSN was updated
    IF OLD.SSN != NEW.SSN THEN
        SET log_description = CONCAT(log_description, 'SSN updated ', OLD.SSN, ' to ', NEW.SSN);
    END IF;

    -- Check if username was updated
    IF OLD.username != NEW.username THEN
        SET log_description = CONCAT(log_description, 'Username updated ', OLD.username, ' to ', NEW.username);
    END IF;

    -- Check if password was updated
    IF OLD.password != NEW.password THEN
        SET log_description = CONCAT(log_description, 'Password updated from ', OLD.password, ' to ', NEW.password);
    END IF;

    -- Check if driverID was updated
    IF OLD.driverID != NEW.driverID THEN
        SET log_description = CONCAT(log_description, 'Driver ID updated ', OLD.driverID, ' to ', NEW.driverID);
    END IF;

    -- Check if cardInfo was updated
    IF OLD.cardInfo != NEW.cardInfo THEN
        SET log_description = CONCAT(log_description, 'Card info updated ', OLD.cardInfo, ' to ', NEW.cardInfo);
    END IF;

    -- Insert log entry if any fields were updated
    IF log_description != '' THEN
        INSERT INTO MemberAuditLog (memberID, event_description)
        VALUES (NEW.memberID, log_description);
    END IF;
END//

DELIMITER ;


-- Trigger to log employee updates
DELIMITER //

CREATE TRIGGER employee_update_trigger
AFTER UPDATE ON Employee
FOR EACH ROW
BEGIN
    DECLARE log_description VARCHAR(255);

    -- Initialize the log description
    SET log_description = '';

    -- Check if firstname was updated
    IF OLD.firstname != NEW.firstname THEN
        SET log_description = CONCAT(log_description, 'First name updated ' , OLD.firstname, ' to ', NEW.firstname);
    END IF;

    -- Check if lastname was updated
    IF OLD.lastname != NEW.lastname THEN
        SET log_description = CONCAT(log_description, 'Last name updated ' , OLD.lastname, ' to ', NEW.lastname);
    END IF;

    -- Check if email was updated
    IF OLD.email != NEW.email THEN
        SET log_description = CONCAT(log_description, 'Email updated ' , OLD.email, ' to ', NEW.email);
    END IF;

    -- Check if phone number was updated
    IF OLD.phone != NEW.phone THEN
        SET log_description = CONCAT(log_description, 'Phone number updated' , OLD.phone, ' to ', NEW.phone);
    END IF;

    -- Check if address was updated
    IF OLD.address != NEW.address THEN
        SET log_description = CONCAT(log_description, 'Address updated ', OLD.address, ' to ', NEW.address);
    END IF;

    -- Check if employeeType was updated
    IF OLD.employeeType != NEW.employeeType THEN
        SET log_description = CONCAT(log_description, 'Employee type updated from ', OLD.employeeType, ' to ', NEW.employeeType);
    END IF;

    -- Insert log entry if any fields were updated
    IF log_description != '' THEN
        INSERT INTO EmployeeAuditLog (employeeID, event_description)
        VALUES (NEW.employeeID, log_description);
    END IF;
END//

DELIMITER ;


-- Trigger to log changes in EmployeeSensitiveInfo table
DELIMITER //

CREATE TRIGGER employee_sensitive_info_trigger
AFTER UPDATE ON EmployeeSensitiveInfo
FOR EACH ROW
BEGIN
    DECLARE log_description VARCHAR(255);
    DECLARE lastModified TIMESTAMP;
    SET lastModified = CURRENT_TIMESTAMP;

    -- Initialize the log description
    SET log_description = '';

    -- Check if password was updated
    IF OLD.password != NEW.password THEN
        SET log_description = CONCAT(log_description, 'Password updated ');
    END IF;

    -- Check if SSN was updated
    IF OLD.SSN != NEW.SSN THEN
        SET log_description = CONCAT(log_description, 'SSN updated ');
    END IF;

    -- Check if driverID was updated
    IF OLD.driverID != NEW.driverID THEN
        SET log_description = CONCAT(log_description, 'Driver ID updated ');
    END IF;

    -- Insert log entry if any sensitive fields were updated
    IF log_description != '' THEN
        INSERT INTO EmployeeAuditLog (employeeID, event_description)
        VALUES (NEW.employeeID, CONCAT('Employee sensitive info updated: ', log_description));
    END IF;
END//
DELIMITER ;
