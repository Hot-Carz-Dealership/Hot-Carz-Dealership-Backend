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
DROP TABLE IF EXISTS Technician;
DROP TABLE IF EXISTS Financing;
DROP TABLE IF EXISTS TestDrive;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Cars;
DROP TABLE IF EXISTS MemberAuditLog;
DROP TABLE IF EXISTS EmployeeAuditLog;

CREATE TABLE IF NOT EXISTS Cars (
    # this table is meant to serve the purpose of containing information on the cars stored in the dealership for sale
    VIN_carID VARCHAR(17) PRIMARY KEY,
    make VARCHAR(50),
    model VARCHAR(50),
    body VARCHAR(50),
    year INT,
    color VARCHAR(50),
    mileage INT,
    details VARCHAR(255),
    description TEXT,
    viewsOnPage INT,
    pictureLibraryLink TEXT,
    status ENUM('new', 'sold', 'low-mileage', 'being-watched'),
    price DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS Member (
    -- this table is meant to serve the purpose of containing basic information of the dealership memebrs
    memberID INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS TestDrive (
    -- this table is meant to store information on the test drive appointments made
    testdrive_id INT AUTO_INCREMENT PRIMARY KEY,
    memberID INT,
    VIN_carID VARCHAR(17),
    appointment_date TIMESTAMP,
    confirmation ENUM ('Confirmed', 'Denied', 'Cancelled', 'Awaiting Confirmation') default NULL,
    FOREIGN KEY (memberID) REFERENCES Member(memberID),
    FOREIGN KEY (VIN_carID) REFERENCES Cars(VIN_carID)
);


CREATE TABLE IF NOT EXISTS ServiceAppointment (
    -- this table is meant to store information on the service appointments made
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    memberID INT,
    appointment_date TIMESTAMP,
    service_name VARCHAR(100),
    FOREIGN KEY (memberID) REFERENCES Member(memberID)
);

CREATE TABLE IF NOT EXISTS Employee (
    -- this table is meant to serve the purpose of containing basic information of the dealership employees
    employeeID INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(50),
    lastname VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(255),
    employeeType ENUM('superAdmin', 'Manager', 'Technician')
);

CREATE TABLE IF NOT EXISTS EmployeeSensitiveInfo (
    -- this table contains sensitive information relating to the Employees
    sensitiveID INT AUTO_INCREMENT PRIMARY KEY,
    employeeID INT,
    password VARCHAR(255),
    SSN VARCHAR(255) UNIQUE,
    driverID VARCHAR(255),
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
    cardInfo TEXT, -- this does literally nothing but im gonna keep it here because it just works and i don't wanna keep breaking stuff rn
    lastModified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (memberID) REFERENCES Member(memberID)
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
    monthly_sum INT, # how much they have to pay for per month
    remaining_months INT,
    FOREIGN KEY (memberID) REFERENCES Member(memberID)
);

CREATE TABLE IF NOT EXISTS Payments (
    paymentID INT AUTO_INCREMENT PRIMARY KEY,
    paymentStatus ENUM('Completed', 'Pending', 'Failed', 'None'),
    valuePaid VARCHAR(20),
    valueToPay VARCHAR(20),
    initialPurchase TIMESTAMP NULL DEFAULT NULL,
    lastPayment TIMESTAMP NULL DEFAULT NULL,
    paymentType ENUM('Check/Bank Account', 'Card', 'None'),
    cardNumber TEXT, -- Assuming card numbers are stored as strings
    expirationDate TEXT, -- Storing as MM/YY format
    CVV TEXT, -- Assuming CVV is a string with a fixed length
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
    FOREIGN KEY (bidID) REFERENCES Bids(bidID),
    FOREIGN KEY (VIN_carID) REFERENCES Cars(VIN_carID),
    FOREIGN KEY (memberID) REFERENCES Member(memberID)
);


CREATE TABLE IF NOT EXISTS Addons (
    -- contains the addons and their cost
    itemID INT AUTO_INCREMENT PRIMARY KEY,
    itemName VARCHAR(100),
    totalCost DECIMAL(10, 2)
);

-- don't worry about these tables yet, later when testing phase comes
-- Audit tables for tracking events

# CREATE TABLE IF NOT EXISTS MemberAuditLog (
#     logID INT AUTO_INCREMENT PRIMARY KEY,
#     memberID INT,
#     event_description TEXT,
#     event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (memberID) REFERENCES Member(memberID)
# );
#
# CREATE TABLE IF NOT EXISTS EmployeeAuditLog (
#     logID INT AUTO_INCREMENT PRIMARY KEY,
#     employeeID INT,
#     event_description TEXT,
#     event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (employeeID) REFERENCES Employee(employeeID)
# );
#
#
# -- Trigger to log member updates
# DELIMITER //
#
# CREATE TRIGGER member_update_trigger
# AFTER UPDATE ON Member
# FOR EACH ROW
# BEGIN
#     DECLARE log_description VARCHAR(255);
#
#     -- Initialize the log description
#     SET log_description = '';
#
#     -- Check if first name was updated
#     IF OLD.first_name != NEW.first_name THEN
#         SET log_description = CONCAT(log_description, 'First name updated ' , OLD.first_name, ' to ', NEW.first_name);
#     END IF;
#
#     -- Check if last name was updated
#     IF OLD.last_name != NEW.last_name THEN
#         SET log_description = CONCAT(log_description, 'Last name updated ' , OLD.last_name, ' to ', NEW.last_name);
#     END IF;
#
#     -- Check if email was updated
#     IF OLD.email != NEW.email THEN
#         SET log_description = CONCAT(log_description, 'Email updated ' , OLD.email, ' to ', NEW.email);
#     END IF;
#
#     -- Check if phone number was updated
#     IF OLD.phone != NEW.phone THEN
#         SET log_description = CONCAT(log_description, 'Phone number updated' , OLD.phone, ' to ', NEW.phone);
#     END IF;
#
#     -- Check if join date was updated
#     IF OLD.join_date != NEW.join_date THEN
#         SET log_description = CONCAT(log_description, 'Join date updated from ', OLD.join_date, ' to ', NEW.join_date, '; ');
#     END IF;
#
#     -- Insert log entry if any fields were updated
#     IF log_description != '' THEN
#         INSERT INTO MemberAuditLog (memberID, event_description)
#         VALUES (NEW.memberID, log_description);
#     END IF;
# END//
#
# DELIMITER ;
#
#
# -- Trigger to log changes in MemberSensitiveInfo table
# DELIMITER //
#
# CREATE TRIGGER member_sensitive_info_trigger
# AFTER UPDATE ON MemberSensitiveInfo
# FOR EACH ROW
# BEGIN
#     DECLARE log_description VARCHAR(255);
#     DECLARE lastModified TIMESTAMP;
#     SET lastModified = CURRENT_TIMESTAMP;
#
#     -- Initialize the log description
#     SET log_description = '';
#
#     -- Check if SSN was updated
#     IF OLD.SSN != NEW.SSN THEN
#         SET log_description = CONCAT(log_description, 'SSN updated ', OLD.SSN, ' to ', NEW.SSN);
#     END IF;
#
#     -- Check if username was updated
#     IF OLD.username != NEW.username THEN
#         SET log_description = CONCAT(log_description, 'Username updated ', OLD.username, ' to ', NEW.username);
#     END IF;
#
#     -- Check if password was updated
#     IF OLD.password != NEW.password THEN
#         SET log_description = CONCAT(log_description, 'Password updated from ', OLD.password, ' to ', NEW.password);
#     END IF;
#
#     -- Check if driverID was updated
#     IF OLD.driverID != NEW.driverID THEN
#         SET log_description = CONCAT(log_description, 'Driver ID updated ', OLD.driverID, ' to ', NEW.driverID);
#     END IF;
#
#     -- Check if cardInfo was updated
#     IF OLD.cardInfo != NEW.cardInfo THEN
#         SET log_description = CONCAT(log_description, 'Card info updated ', OLD.cardInfo, ' to ', NEW.cardInfo);
#     END IF;
#
#     -- Insert log entry if any fields were updated
#     IF log_description != '' THEN
#         INSERT INTO MemberAuditLog (memberID, event_description)
#         VALUES (NEW.memberID, log_description);
#     END IF;
# END//
#
# DELIMITER ;
#
#
# -- Trigger to log employee updates
# DELIMITER //
#
# CREATE TRIGGER employee_update_trigger
# AFTER UPDATE ON Employee
# FOR EACH ROW
# BEGIN
#     DECLARE log_description VARCHAR(255);
#
#     -- Initialize the log description
#     SET log_description = '';
#
#     -- Check if firstname was updated
#     IF OLD.firstname != NEW.firstname THEN
#         SET log_description = CONCAT(log_description, 'First name updated ' , OLD.firstname, ' to ', NEW.firstname);
#     END IF;
#
#     -- Check if lastname was updated
#     IF OLD.lastname != NEW.lastname THEN
#         SET log_description = CONCAT(log_description, 'Last name updated ' , OLD.lastname, ' to ', NEW.lastname);
#     END IF;
#
#     -- Check if email was updated
#     IF OLD.email != NEW.email THEN
#         SET log_description = CONCAT(log_description, 'Email updated ' , OLD.email, ' to ', NEW.email);
#     END IF;
#
#     -- Check if phone number was updated
#     IF OLD.phone != NEW.phone THEN
#         SET log_description = CONCAT(log_description, 'Phone number updated' , OLD.phone, ' to ', NEW.phone);
#     END IF;
#
#     -- Check if address was updated
#     IF OLD.address != NEW.address THEN
#         SET log_description = CONCAT(log_description, 'Address updated ', OLD.address, ' to ', NEW.address);
#     END IF;
#
#     -- Check if employeeType was updated
#     IF OLD.employeeType != NEW.employeeType THEN
#         SET log_description = CONCAT(log_description, 'Employee type updated from ', OLD.employeeType, ' to ', NEW.employeeType);
#     END IF;
#
#     -- Insert log entry if any fields were updated
#     IF log_description != '' THEN
#         INSERT INTO EmployeeAuditLog (employeeID, event_description)
#         VALUES (NEW.employeeID, log_description);
#     END IF;
# END//
#
# DELIMITER ;
#
#
# -- Trigger to log changes in EmployeeSensitiveInfo table
# DELIMITER //
#
# CREATE TRIGGER employee_sensitive_info_trigger
# AFTER UPDATE ON EmployeeSensitiveInfo
# FOR EACH ROW
# BEGIN
#     DECLARE log_description VARCHAR(255);
#     DECLARE lastModified TIMESTAMP;
#     SET lastModified = CURRENT_TIMESTAMP;
#
#     -- Initialize the log description
#     SET log_description = '';
#
#     -- Check if password was updated
#     IF OLD.password != NEW.password THEN
#         SET log_description = CONCAT(log_description, 'Password updated ');
#     END IF;
#
#     -- Check if SSN was updated
#     IF OLD.SSN != NEW.SSN THEN
#         SET log_description = CONCAT(log_description, 'SSN updated ');
#     END IF;
#
#     -- Check if driverID was updated
#     IF OLD.driverID != NEW.driverID THEN
#         SET log_description = CONCAT(log_description, 'Driver ID updated ');
#     END IF;
#
#     -- Insert log entry if any sensitive fields were updated
#     IF log_description != '' THEN
#         INSERT INTO EmployeeAuditLog (employeeID, event_description)
#         VALUES (NEW.employeeID, CONCAT('Employee sensitive info updated: ', log_description));
#     END IF;
# END//
# DELIMITER ;
