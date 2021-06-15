-- PRAGMA foreign_keys=ON
-- BEGIN TRANSACTION; 

-- guest table
DROP TABLE IF EXISTS guest; 
CREATE TABLE guest(
    guestID INTEGER primary key AUTOINCREMENT,
    firstName VARCHAR, 
    lastName VARCHAR,
    phone VARCHAR NULL,
    addr VARCHAR NULL,
    email VARCHAR NULL,
    id VARCHAR NULL,
    vehicle VARCHAR NULL,
    totalCharge DOUBLE NULL,
    balance DOUBLE NULL
); 
DROP TABLE IF EXISTS housekeeper;
CREATE TABLE housekeeper(
    employeeID INTEGER PRIMARY KEY AUTOINCREMENT, 
    fName VARCHAR, 
    lName VARCHAR
); 
DROP TABLE IF EXISTS room; 
CREATE TABLE room(
    rmNum INT primary key NOT NULL, 
    type VARCHAR, 
    status VARCHAR,
    houseKeeperID INT NULL,
    bathroom INT NULL,
    towels INT NULL, 
    bedSheets INT NULL, 
    vacum INT NULL, 
    dusting INT NULL, 
    electronics INT NULL,
    rate INT NULL, 
    FOREIGN KEY (houseKeeperID) REFERENCES housekeeper(employeeID) 
); 

-- reservation table
DROP TABLE IF EXISTS reservation; 
CREATE TABLE reservation(
    reservID INTEGER primary key AUTOINCREMENT, 
    guestID INT, 
    dateMade DATE,
    checkIN DATE NULL, 
    checkOut DATE NULL,
    rmNum INT,
    checkedIn VARCHAR,
    FOREIGN KEY (guestID) REFERENCES guest(guestID)
    FOREIGN KEY (rmNum) REFERENCES room(rmNum)
);

INSERT INTO guest(firstName,lastName,phone,addr,email,id,vehicle,totalCharge,balance) 
VALUES('bob','smith',"123-123-1123",'STREET 123', 'bobsmith@gmail.com','123','ABC123', 400.50, 150); 
INSERT INTO guest(firstName,lastName) 
VALUES('william','marcus'); 

INSERT INTO room(rmNum, type, status) VALUES(001, 'K','Available'); 
INSERT INTO room(rmNum, type, status) VALUES(002, 'DQK','Available'); 
INSERT INTO room(rmNum, type, status) VALUES(003, 'DQ','Dirty'); 
INSERT INTO room(rmNum, type, status) VALUES(004, 'S','Maintenance'); 
INSERT INTO room(rmNum, type, status) VALUES(005, 'S','Available'); 
INSERT INTO room(rmNum, type, status) VALUES(006, 'DQ','Dirty'); 
INSERT INTO room(rmNum, type, status) VALUES(007, 'S','Maintenance'); 
INSERT INTO room(rmNum, type, status) VALUES(008, 'K','Available'); 
INSERT INTO room(rmNum, type, status) VALUES(009, 'DQK','Available'); 
INSERT INTO room(rmNum, type, status) VALUES(010, 'S','Available'); 


INSERT INTO reservation(guestID,dateMade,checkIN,checkOut,rmNum)
VALUES(1,CURRENT_DATE,'01-26-2022','02-22-2022',002);
INSERT INTO reservation(guestID,dateMade,checkIN,checkOut,rmNum)
VALUES(2,CURRENT_DATE,'01-26-2022','02-22-2022',010);


INSERT INTO housekeeper( fName, lName) VALUES('rhonda','smith'); 

