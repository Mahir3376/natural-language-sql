-- Hotel Room Booking Schema
-- Defines the core entities, relationships, and constraints

CREATE DATABASE IF NOT EXISTS Hotel_Room_Booking;
USE Hotel_Room_Booking;

-- ----------------------------
-- Table: Pincode
-- ----------------------------
CREATE TABLE Pincode (
    Pincode INT PRIMARY KEY,
    City VARCHAR(20),
    State VARCHAR(20)
);

-- ----------------------------
-- Table: Hotel
-- ----------------------------
CREATE TABLE Hotel (
    Hotel_id INT PRIMARY KEY,
    Hotel_Name VARCHAR(20),
    Hotel_type VARCHAR(20),
    Road_no INT,
    Street VARCHAR(20),
    Pincode INT,
    FOREIGN KEY (Pincode) REFERENCES Pincode(Pincode)
);

-- ----------------------------
-- Table: Service
-- ----------------------------
CREATE TABLE Service (
    Service_id VARCHAR(10) PRIMARY KEY,
    Service_name VARCHAR(20),
    Service_type VARCHAR(32)
);

-- ----------------------------
-- Table: Offers (many-to-many between Hotel and Service)
-- ----------------------------
CREATE TABLE Offers (
    Service_id VARCHAR(10),
    Hotel_id INT,
    Price INT,
    PRIMARY KEY (Service_id, Hotel_id),
    FOREIGN KEY (Service_id) REFERENCES Service(Service_id),
    FOREIGN KEY (Hotel_id) REFERENCES Hotel(Hotel_id)
);

-- ----------------------------
-- Table: Room
-- ----------------------------
CREATE TABLE Room (
    Room_id VARCHAR(10) PRIMARY KEY,
    Room_no INT,
    Room_type VARCHAR(32),
    Availability VARCHAR(10),
    Description VARCHAR(128),
    Hotel_id INT,
    FOREIGN KEY (Hotel_id) REFERENCES Hotel(Hotel_id)
);

-- ----------------------------
-- Table: Customer
-- ----------------------------
CREATE TABLE Customer (
    Customer_id INT PRIMARY KEY,
    Customer_name VARCHAR(20),
    H_no INT,
    Street VARCHAR(20),
    Email VARCHAR(50),
    IsGuest BOOLEAN,
    Pincode INT,
    FOREIGN KEY (Pincode) REFERENCES Pincode(Pincode)
);

-- ----------------------------
-- Table: CustomerContact
-- ----------------------------
CREATE TABLE CustomerContact (
    Customer_id INT,
    Contact_num VARCHAR(15),
    PRIMARY KEY (Customer_id, Contact_num),
    FOREIGN KEY (Customer_id) REFERENCES Customer(Customer_id)
);

-- ----------------------------
-- Table: Guest (1-to-1 with Customer)
-- ----------------------------
CREATE TABLE Guest (
    Customer_id INT PRIMARY KEY,
    Guest_type VARCHAR(10),
    Preferred_roomtype VARCHAR(20),
    FOREIGN KEY (Customer_id) REFERENCES Customer(Customer_id)
);

-- ----------------------------
-- Table: Booking
-- ----------------------------
CREATE TABLE Booking (
    Booking_id INT PRIMARY KEY,
    Booking_title VARCHAR(50),
    Booking_date DATE,
    Check_in_date DATE,
    Check_out_date DATE,
    Room_id VARCHAR(10),
    Customer_id INT,
    FOREIGN KEY (Room_id) REFERENCES Room(Room_id),
    FOREIGN KEY (Customer_id) REFERENCES Customer(Customer_id)
);

-- ----------------------------
-- Table: Payment
-- ----------------------------
CREATE TABLE Payment (
    Payment_id VARCHAR(10) PRIMARY KEY,
    Booking_id INT,
    Date DATE,
    Amount INT,
    FOREIGN KEY (Booking_id) REFERENCES Booking(Booking_id)
);
