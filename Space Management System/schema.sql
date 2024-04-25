CREATE TABLE User (
	user_id INT AUTO_INCREMENT PRIMARY KEY,
	username VARCHAR(256) NOT NULL,
	name VARCHAR(256) NOT NULL,
	password VARCHAR(256) NOT NULL,
	email VARCHAR(256) NOT NULL
);

CREATE TABLE Astronaut (
	user_id INT PRIMARY KEY,
	company_id INT,
	date_of_birth DATE,
	nationality VARCHAR(40) NOT NULL,
	experience_level VARCHAR(40),
	preferred_role VARCHAR(40),
	FOREIGN KEY (user_id) REFERENCES User(user_id),
	FOREIGN KEY (company_id) REFERENCES User(user_id)
);

CREATE TABLE Company (
	user_id INT PRIMARY KEY,
	address VARCHAR(256) NOT NULL,
	industry_sector VARCHAR(50) NOT NULL,
	website VARCHAR(256),
	FOREIGN KEY (user_id) REFERENCES User(user_id)
);

CREATE TABLE participates (
	astronaut_id INT,
	mission_id INT,
	FOREIGN KEY (astronaut_id) REFERENCES User(user_id),
	FOREIGN KEY (mission_id) REFERENCES space_mission(mission_id) ,
	PRIMARY KEY (astronaut_id, mission_id)
);

CREATE TABLE Admin (
	user_id INT PRIMARY KEY,
	permission_level VARCHAR(256) NOT NULL,
	FOREIGN KEY (user_id) REFERENCES User(user_id)
);

CREATE TABLE space_mission (
	mission_id INT AUTO_INCREMENT PRIMARY KEY,
	mission_name VARCHAR(255),
	description VARCHAR(4096),
	status VARCHAR(50),
	launch_date DATE,
	destination VARCHAR(100),
	cost FLOAT(15, 2),
	duration INT,
	crew_size INT,
	required_roles VARCHAR(255),
	bid_deadline DATE;
	creator_comp_id INT,
	manager_comp_id INT,
	spaceship_id INT,
	FOREIGN KEY (creator_comp_id) REFERENCES User(user_id), -- Assuming User table has a primary key called user_id
	FOREIGN KEY (manager_comp_id) REFERENCES User(user_id), --Assuming User table has a primary key called user_id
	FOREIGN KEY (spaceship_id) REFERENCES spaceship(spaceship_id) -- Assuming spaceship table has a primary key called spaceship_id
);

CREATE TABLE Spaceship (
	spaceship_id INT AUTO_INCREMENT PRIMARY KEY,
	spaceship_name VARCHAR(256) NOT NULL,
	type VARCHAR(50) NOT NULL,
	status VARCHAR(50) NOT NULL,
	capacity INT NOT NULL,
	owner_comp _id INT NOT NULL,
	launch_vehicle_id INT,
	FOREIGN KEY (owner_comp_id) REFERENCES User(user_id),
	FOREIGN KEY (launch_vehicle_id) REFERENCES
	launch_vehicle(launch_vehicle_id)
);

CREATE TABLE launch_vehicle (
	launch_vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
	launch_vehicle_name VARCHAR(255),
	model VARCHAR(100),
	status VARCHAR(50),
	launch_site VARCHAR(100)
);

CREATE TABLE financial_transaction (
	transaction_id INT AUTO_INCREMENT PRIMARY KEY,
	date DATE,
	type VARCHAR(50),
	amount FLOAT(15, 2),
	status VARCHAR(50),
	description VARCHAR(4096),
	payer_comp INT,
	payee_comp INT,
	mission_id INT,
	FOREIGN KEY (payer_comp) REFERENCES User(user_id),
	FOREIGN KEY (payee_comp) REFERENCES User(user_id),
	FOREIGN KEY (mission_id) REFERENCES space_mission(mission_id)
);

CREATE TABLE bid (
	bid_id INT AUTO_INCREMENT PRIMARY KEY,
	bid_amount FLOAT(15, 2),
	bid_date DATE,
	status VARCHAR(50),
	company_id INT,
	mission_id INT,
	FOREIGN KEY (company_id) REFERENCES User(user_id),
	FOREIGN KEY (mission_id) REFERENCES space_mission(mission_id)
);

CREATE TABLE communication_log (
	log_id INT PRIMARY KEY AUTO_INCREMENT,
	date_time DATETIME,
	sender_id INT,
	receiver_id INT,
	message VARCHAR(4096),
	type VARCHAR(50),
	mission_id INT,
	FOREIGN KEY (sender_id) REFERENCES User(user_id),
	FOREIGN KEY (receiver_id) REFERENCES User(user_id),
	FOREIGN KEY (mission_id) REFERENCES space_mission(mission_id)
);


CREATE TABLE mission_resource (
	mission_id INT,
	resource_id INT,
	budget FLOAT(15, 2),
	resource_type VARCHAR(50),
	FOREIGN KEY (mission_id) REFERENCES space_mission(mission_id),
	PRIMARY KEY (mission_id, resource_id)
);


CREATE TABLE Training_program (
	program_id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(256),
	description VARCHAR(4096),
	required_for VARCHAR(100),
	completion_date DATE,
);

CREATE TABLE astronaut_training (
	astronaut_id INT,
	program_id INT,
	FOREIGN KEY (astronaut_id) REFERENCES User(user_id),
	FOREIGN KEY (program_id) REFERENCES training_program(program_id),
	PRIMARY KEY (astronaut_id, program_id)
);

CREATE TABLE Health_record (
	record_id INT AUTO_INCREMENT PRIMARY KEY,
	checkup_date DATE NOT NULL,
	health_status VARCHAR(256),
	fitness_level VARCHAR(50),
	expected_ready_time DATETIME,
	astronaut_id INT,
	FOREIGN KEY (astronaut_id) REFERENCES User(user_id)
);

CREATE TABLE mission_feedback (
	feedback_id INT AUTO_INCREMENT PRIMARY KEY,
	date_submitted DATE NOT NULL,
	content VARCHAR(4096),
	mission_id INT,
	feedback_giver INT,
	FOREIGN KEY (mission_id) REFERENCES space_mission(mission_id),
	FOREIGN KEY (feedback_giver) REFERENCES User(user_id)
);