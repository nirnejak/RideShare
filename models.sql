CREATE TABLE users(
	userId INT(11) AUTO_INCREMENT PRIMARY KEY, 
	fname VARCHAR(100), 
	lname VARCHAR(100), 
	gender VARCHAR(50),
	driving VARCHAR(50) UNIQUE,
	aadhar VARCHAR(50) UNIQUE,
	contactNo VARCHAR(30) UNIQUE, 
	alternateContactNo VARCHAR(30), 
	email VARCHAR(100) UNIQUE, 
	password VARCHAR(100), 
	registerDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	addLine1 VARCHAR(150),
	addLine2 VARCHAR(150),
	colony VARCHAR(100),
	city VARCHAR(100),
	state VARCHAR(100),

	userStatus VARCHAR(50) DEFAULT "LOGGEDIN",
	userType VARCHAR(50) DEFAULT "CUSTOMER"
);

CREATE TABLE Ride(
	RideId INT(11) AUTO_INCREMENT PRIMARY KEY, 
	creatorUserId INT(11), # ID of user who sent the request
	rideDate DATE,
	rideTime TIME,
	rideStatus VARCHAR(50) DEFAULT "PENDING",

	fromLocation VARCHAR(100),
	toLocation VARCHAR(100),
	state VARCHAR(100),
	city VARCHAR(100)
);


CREATE TABLE ShareRequest(
	RequestID INT(11) AUTO_INCREMENT PRIMARY KEY,
	RideID INT(11),
	requestUserId INT(11) # ID of user who sent the request
);
