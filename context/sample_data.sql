-- Sample Data for Hotel Room Booking
-- Minimal dataset to test queries

USE Hotel_Room_Booking;

-- ----------------------------
-- Table: Pincode
-- ----------------------------
INSERT INTO Pincode VALUES (515001, 'Anantapur', 'Andhra Pradesh');
INSERT INTO Pincode VALUES (560002, 'Bangalore', 'Karnataka');
INSERT INTO Pincode VALUES (500003, 'Hyderabad', 'Telangana');

-- ----------------------------
-- Table: Hotel
-- ----------------------------
INSERT INTO Hotel VALUES (101, 'Masineni Grand', 'Budget Hotel', 32, 'Bhagya Nagar', 515001);
INSERT INTO Hotel VALUES (149, 'Swagath Royal', 'Extended Stay', 67, 'Madhapur', 500003);
INSERT INTO Hotel VALUES (234, 'Clarks Inn', 'Airport Hotel', 165, 'Bettahalsur Cross', 560002);

-- ----------------------------
-- Table: Service
-- ----------------------------
INSERT INTO Service VALUES ('S101', 'Laundry', 'General Services');
INSERT INTO Service VALUES ('S102', 'Room Service', 'General Services');
INSERT INTO Service VALUES ('S104', 'Spa Treatments', 'Wellness Services');

-- ----------------------------
-- Table: Offers
-- ----------------------------
INSERT INTO Offers VALUES ('S101', 101, 250);
INSERT INTO Offers VALUES ('S102', 149, 200);
INSERT INTO Offers VALUES ('S104', 234, 500);

-- ----------------------------
-- Table: Room
-- ----------------------------
INSERT INTO Room VALUES ('A101', 101, 'Double Room', 'Yes', 'Ideal for two guests. Contains TV, safe.', 101);
INSERT INTO Room VALUES ('B101', 101, 'Single Room', 'No', 'Single guest room, no balcony.', 149);
INSERT INTO Room VALUES ('C101', 101, 'Family Room', 'Yes', 'Large room with balcony view.', 234);

-- ----------------------------
-- Table: Customer
-- ----------------------------
INSERT INTO Customer VALUES (1, 'Yashwanth', 4, 'Vidya Nagar', 'yash123@gmail.com', FALSE, 500003);
INSERT INTO Customer VALUES (2, 'Karthik', 17, 'Ram Nagar', 'karthik@gmail.com', TRUE, 515001);

-- ----------------------------
-- Table: CustomerContact
-- ----------------------------
INSERT INTO CustomerContact VALUES (1, '9876543210');
INSERT INTO CustomerContact VALUES (2, '9123456780');

-- ----------------------------
-- Table: Guest
-- ----------------------------
INSERT INTO Guest VALUES (2, 'VIP', 'Family Room');

-- ----------------------------
-- Table: Booking
-- ----------------------------
INSERT INTO Booking VALUES (120, 'Stay in Hyd', '2024-03-07', '2024-03-11', '2024-03-14', 'A101', 1);
INSERT INTO Booking VALUES (121, 'Business Trip', '2024-03-10', '2024-03-15', '2024-03-17', 'C101', 2);

-- ----------------------------
-- Table: Payment
-- ----------------------------
INSERT INTO Payment VALUES ('P1001', 120, '2024-03-07', 3500);
INSERT INTO Payment VALUES ('P1002', 121, '2024-03-10', 5000);
