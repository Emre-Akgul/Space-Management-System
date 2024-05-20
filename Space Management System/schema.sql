CREATE DATABASE IF NOT EXISTS spaceapp;


USE spaceapp;

CREATE TABLE User (
	user_id INT AUTO_INCREMENT PRIMARY KEY,
	username VARCHAR(256) NOT NULL,
	name VARCHAR(256) NOT NULL,
	password VARCHAR(256) NOT NULL,
	email VARCHAR(256) NOT NULL
);

ALTER TABLE User
ADD UNIQUE (username),
ADD UNIQUE (email);

CREATE TABLE launch_vehicle (
	launch_vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
	launch_vehicle_name VARCHAR(255),
	model VARCHAR(100),
	status VARCHAR(50),
	launch_site VARCHAR(100)
);

CREATE TABLE Spaceship (
	spaceship_id INT AUTO_INCREMENT PRIMARY KEY,
	spaceship_name VARCHAR(256) NOT NULL,
	type VARCHAR(50) NOT NULL,
	status VARCHAR(50) NOT NULL,
	capacity INT NOT NULL,
	owner_comp_id INT NOT NULL,
	launch_vehicle_id INT,
	FOREIGN KEY (owner_comp_id) REFERENCES User(user_id),
	FOREIGN KEY (launch_vehicle_id) REFERENCES launch_vehicle(launch_vehicle_id)
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
	bid_deadline DATE,
	creator_comp_id INT,
	manager_comp_id INT,
	spaceship_id INT,
	FOREIGN KEY (creator_comp_id) REFERENCES User(user_id),
	FOREIGN KEY (manager_comp_id) REFERENCES User(user_id),
	FOREIGN KEY (spaceship_id) REFERENCES Spaceship(spaceship_id)
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

CREATE TABLE Admin (
	user_id INT PRIMARY KEY,
	permission_level VARCHAR(256) NOT NULL,
	FOREIGN KEY (user_id) REFERENCES User(user_id)
);



CREATE TABLE Company (
	user_id INT PRIMARY KEY,
	address VARCHAR(256) NOT NULL,
	industry_sector VARCHAR(50) NOT NULL,
	website VARCHAR(256),
	FOREIGN KEY (user_id) REFERENCES User(user_id)
);

CREATE TABLE Role (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL
);

CREATE TABLE Astronaut (
    user_id INT PRIMARY KEY,
    company_id INT,
    date_of_birth DATE,
    nationality VARCHAR(40) NOT NULL,
    experience_level VARCHAR(40),
    role_id INT,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (company_id) REFERENCES Company(user_id),
    FOREIGN KEY (role_id) REFERENCES Role(role_id)
);

ALTER TABLE Astronaut
ADD CONSTRAINT chk_astronaut_min_age
CHECK (TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) >= 18);

INSERT INTO Role (role_name) VALUES
('Not Assigned'),
('Commander'),
('Pilot'),
('Mission Specialist'),
('Flight Engineer'),
('Medical Doctor');

CREATE TABLE participates (
	astronaut_id INT,
	mission_id INT,
	FOREIGN KEY (astronaut_id) REFERENCES User(user_id),
	FOREIGN KEY (mission_id) REFERENCES space_mission(mission_id) ,
	PRIMARY KEY (astronaut_id, mission_id)
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
    required_for INT,
    difficulty ENUM('Essential', 'Intermediate', 'Advanced'),
    FOREIGN KEY (required_for) REFERENCES Role(role_id)
);

CREATE VIEW MissionSummary AS
SELECT 
    mission_id,
    mission_name, 
    status, 
    launch_date, 
    cost
FROM 
    space_mission;


CREATE VIEW BidSummary AS
SELECT 
    b.bid_id,
    b.bid_amount, 
    u.name AS bidder_name,
    m.mission_name
FROM 
    bid b
JOIN 
    User u ON b.company_id = u.user_id
JOIN 
    space_mission m ON b.mission_id = m.mission_id;


INSERT INTO Training_program (name, description, required_for, difficulty) VALUES 
('Commander Essential Training', 'This is the essential training program for the commander role.', (SELECT role_id FROM Role WHERE role_name = 'Commander'), 'Essential'),
('Commander Intermediate Training', 'This is the intermediate training program for the commander role.', (SELECT role_id FROM Role WHERE role_name = 'Commander'), 'Intermediate'),
('Commander Advanced Training', 'This is the advanced training program for the commander role.', (SELECT role_id FROM Role WHERE role_name = 'Commander'), 'Advanced'),
('Pilot Essential Training', 'This is the essential training program for the pilot role.', (SELECT role_id FROM Role WHERE role_name = 'Pilot'), 'Essential'),
('Pilot Intermediate Training', 'This is the intermediate training program for the pilot role.', (SELECT role_id FROM Role WHERE role_name = 'Pilot'), 'Intermediate'),
('Pilot Advanced Training', 'This is the advanced training program for the pilot role.', (SELECT role_id FROM Role WHERE role_name = 'Pilot'), 'Advanced'),
('Mission Specialist Essential Training', 'This is the essential training program for the mission specialist role.', (SELECT role_id FROM Role WHERE role_name = 'Mission Specialist'), 'Essential'),
('Mission Specialist Intermediate Training', 'This is the intermediate training program for the mission specialist role.', (SELECT role_id FROM Role WHERE role_name = 'Mission Specialist'), 'Intermediate'),
('Mission Specialist Advanced Training', 'This is the advanced training program for the mission specialist role.', (SELECT role_id FROM Role WHERE role_name = 'Mission Specialist'), 'Advanced'),
('Flight Engineer Essential Training', 'This is the essential training program for the flight engineer role.', (SELECT role_id FROM Role WHERE role_name = 'Flight Engineer'), 'Essential'),
('Flight Engineer Intermediate Training', 'This is the intermediate training program for the flight engineer role.', (SELECT role_id FROM Role WHERE role_name = 'Flight Engineer'), 'Intermediate'),
('Flight Engineer Advanced Training', 'This is the advanced training program for the flight engineer role.', (SELECT role_id FROM Role WHERE role_name = 'Flight Engineer'), 'Advanced'),
('Medical Doctor Essential Training', 'This is the essential training program for the medical doctor role.', (SELECT role_id FROM Role WHERE role_name = 'Medical Doctor'), 'Essential'),
('Medical Doctor Intermediate Training', 'This is the intermediate training program for the medical doctor role.', (SELECT role_id FROM Role WHERE role_name = 'Medical Doctor'), 'Intermediate'),
('Medical Doctor Advanced Training', 'This is the advanced training program for the medical doctor role.', (SELECT role_id FROM Role WHERE role_name = 'Medical Doctor'), 'Advanced'),
('Space Agriculture Training', 'This advanced training program covers the techniques for growing food in space environments.', (SELECT role_id FROM Role WHERE role_name = 'Not assigned'), 'Advanced'),
('Spacecraft Maintenance Training', 'This advanced training program covers the maintenance procedures and troubleshooting of spacecraft systems.', (SELECT role_id FROM Role WHERE role_name = 'Not assigned'), 'Advanced'),
('Robotics Training', 'This advanced training program focuses on the operation and maintenance of robotic systems used in space missions.', (SELECT role_id FROM Role WHERE role_name = 'Not assigned'), 'Advanced'),
('Space Research Training', 'This advanced training program covers the methodologies and practices for conducting research in space.', (SELECT role_id FROM Role WHERE role_name = 'Not assigned'), 'Advanced'),
('Space Engineering Training', 'This advanced training program covers the engineering principles and technologies used in space missions.', (SELECT role_id FROM Role WHERE role_name = 'Not assigned'), 'Advanced');

CREATE TABLE astronaut_training (
    astronaut_id INT,
    program_id INT,
    completion_date DATE,
    FOREIGN KEY (astronaut_id) REFERENCES User(user_id),
    FOREIGN KEY (program_id) REFERENCES Training_program(program_id),
    PRIMARY KEY (astronaut_id, program_id)
);

CREATE TABLE Health_record (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    checkup_date DATE NOT NULL,
    health_status VARCHAR(256),
    fitness_level ENUM('Optimal', 'Above Average', 'Average', 'Below Average', 'Injured') NOT NULL,
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
ALTER TABLE Spaceship CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE owns (
    company_id INT,
    spaceship_id INT,
    PRIMARY KEY (company_id, spaceship_id),
    FOREIGN KEY (company_id) REFERENCES Company(user_id),
    FOREIGN KEY (spaceship_id) REFERENCES Spaceship(spaceship_id)
);

CREATE TABLE uses (
    spaceship_id INT,
    space_mission_id INT,
    PRIMARY KEY (spaceship_id, space_mission_id),
    FOREIGN KEY (spaceship_id) REFERENCES Spaceship(spaceship_id),
    FOREIGN KEY (space_mission_id) REFERENCES space_mission(mission_id)
);

INSERT INTO User (user_id, username, name, password, email) VALUES 
(1, 'companyA', 'Company A', 'pass1', 'companya@example.com'), 
(2, 'companyB', 'Company B', 'pass2', 'companyb@example.com'), 
(3, 'companyC', 'Company C', 'pass3', 'companyc@example.com');

-- Insert corresponding entries into the Company table
INSERT INTO Company (user_id, address, industry_sector, website) VALUES 
(1, '123 Space Way', 'Aerospace', 'https://companyA.com'), 
(2, '456 Galaxy Road', 'Aerospace', 'https://companyB.com'), 
(3, '789 Star Blvd', 'Aerospace', 'https://companyC.com');

-- Inserting sample data into launch_vehicle table 
INSERT INTO launch_vehicle (launch_vehicle_name, model, status, launch_site) 
VALUES 
('Falcon 9', 'Block 5', 'Operational', 'Cape Canaveral'), 
('Delta IV Heavy', 'Heavy', 'Operational', 'Vandenberg'), 
('Atlas V', '401', 'Operational', 'Cape Canaveral'), 
('Starship', 'Mk1', 'Testing', 'Boca Chica'), 
('New Glenn', 'Rocket', 'In Development', 'Cape Canaveral'); 
 
-- Inserting sample data into Spaceship table 
INSERT INTO Spaceship (spaceship_name, type, status, capacity, owner_comp_id, launch_vehicle_id) 
VALUES 
('Spaceship Alpha', 'Exploration', 'Active', 10, 1, 1), 
('Spaceship Beta', 'Mining', 'Active', 15, 2, 2), 
('Spaceship Gamma', 'Research', 'Active', 20, 3, 3), 
('Spaceship Delta', 'Mapping', 'Active', 8, 1, 4), 
('Spaceship Epsilon', 'Tourism', 'Active', 5, 2, 5); 

INSERT INTO owns (company_id, spaceship_id) VALUES 
(1, 1),  -- Company A owns Spaceship Alpha
(2, 2),  -- Company B owns Spaceship Beta
(3, 3),  -- Company C owns Spaceship Gamma
(1, 4),  -- Company A owns Spaceship Delta
(2, 5);  -- Company B owns Spaceship Epsilon

-- Insert users for astronauts
INSERT INTO User (user_id, username, name, password, email) VALUES (4, 'astronaut1', 'Astronaut One', 'pass1', 'astronaut1@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (5, 'astronaut2', 'Astronaut Two', 'pass2', 'astronaut2@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (6, 'astronaut3', 'Astronaut Three', 'pass3', 'astronaut3@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (7, 'astronaut4', 'Astronaut Four', 'pass4', 'astronaut4@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (8, 'astronaut5', 'Astronaut Five', 'pass5', 'astronaut5@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (9, 'astronaut6', 'Astronaut Six', 'pass6', 'astronaut6@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (10, 'astronaut7', 'Astronaut Seven', 'pass7', 'astronaut7@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (11, 'astronaut8', 'Astronaut Eight', 'pass8', 'astronaut8@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (12, 'astronaut9', 'Astronaut Nine', 'pass9', 'astronaut9@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (13, 'astronaut10', 'Astronaut Ten', 'pass10', 'astronaut10@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (14, 'astronaut11', 'Astronaut Eleven', 'pass11', 'astronaut11@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (15, 'astronaut12', 'Astronaut Twelve', 'pass12', 'astronaut12@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (16, 'astronaut13', 'Astronaut Thirteen', 'pass13', 'astronaut13@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (17, 'astronaut14', 'Astronaut Fourteen', 'pass14', 'astronaut14@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (18, 'astronaut15', 'Astronaut Fifteen', 'pass15', 'astronaut15@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (19, 'astronaut16', 'Astronaut Sixteen', 'pass16', 'astronaut16@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (20, 'astronaut17', 'Astronaut Seventeen', 'pass17', 'astronaut17@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (21, 'astronaut18', 'Astronaut Eighteen', 'pass18', 'astronaut18@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (22, 'astronaut19', 'Astronaut Nineteen', 'pass19', 'astronaut19@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (23, 'astronaut20', 'Astronaut Twenty', 'pass20', 'astronaut20@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (24, 'astronaut21', 'Astronaut Twenty-One', 'pass21', 'astronaut21@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (25, 'astronaut22', 'Astronaut Twenty-Two', 'pass22', 'astronaut22@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (26, 'astronaut23', 'Astronaut Twenty-Three', 'pass23', 'astronaut23@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (27, 'astronaut24', 'Astronaut Twenty-Four', 'pass24', 'astronaut24@example.com');
INSERT INTO User (user_id, username, name, password, email) VALUES (28, 'astronaut25', 'Astronaut Twenty-Five', 'pass25', 'astronaut25@example.com');

-- Insert astronauts infos
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (4, 1, '2000-01-01', 'TUR', 'Beginner', 1);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (5, 2, '1985-05-20', 'TUR', 'Intermediate', 2);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (6, 3, '1990-07-15', 'CAN', 'Expert', 3);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (7, 1, '1978-11-11', 'IND', 'Advanced', 4);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (8, 2, '1988-02-28', 'TUR', 'Intermediate', 5);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (9, 1, '1977-03-14', 'USA', 'Beginner', 1);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (10, 2, '1992-06-21', 'TUR', 'Expert', 2);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (11, 3, '1980-08-19', 'TUR', 'Advanced', 3);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (12, 1, '1985-12-11', 'IND', 'Intermediate', 4);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (13, 2, '1993-05-15', 'TUR', 'Beginner', 5);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (14, 1, '1982-07-22', 'USA', 'Expert', 1);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (15, 2, '1990-01-01', 'TUR', 'Advanced', 2);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (16, 3, '1989-09-09', 'CAN', 'Intermediate', 3);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (17, 1, '1981-10-23', 'IND', 'Beginner', 4);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (18, 2, '1995-04-18', 'TUR', 'Expert', 5);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (19, 1, '1979-11-29', 'USA', 'Advanced', 1);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (20, 2, '1994-02-14', 'TUR', 'Intermediate', 2);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (21, 3, '1983-03-17', 'CAN', 'Beginner', 3);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (22, 1, '1987-06-11', 'IND', 'Expert', 4);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (23, 2, '1991-08-19', 'CHN', 'Advanced', 5);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (24, 1, '1984-10-30', 'USA', 'Intermediate', 1);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (25, 2, '1990-12-12', 'TUR', 'Beginner', 2);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (26, 3, '1986-11-21', 'CAN', 'Expert', 3);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (27, 1, '1993-09-09', 'IND', 'Advanced', 4);
INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, experience_level, role_id) VALUES (28, 2, '1988-03-15', 'TUR', 'Intermediate', 5);

Insert into User (username, name, password, email) values ('admin', 'Admin', 'admin', 'admin@admin.com');
Insert into Admin (user_id, permission_level) values (29, 'SuperAdmin');

-- Insert a past mission
INSERT INTO space_mission (mission_name, description, status, launch_date, destination, cost, duration, crew_size, required_roles, bid_deadline, creator_comp_id, manager_comp_id, spaceship_id)
VALUES 
('Mission Past Alpha', 'Exploration mission to Mars.', 'Completed', '2022-07-20', 'Mars', 50000000, 180, 10, 'Commander, Pilot, Mission Specialist, Flight Engineer, Medical Doctor', '2021-06-20', 1, 2, 1),
('Mission Past Beta', 'Mining mission on the Moon.', 'Completed', '2021-05-10', 'Moon', 30000000, 90, 8, 'Commander, Pilot, Mission Specialist, Flight Engineer', '2020-11-30', 2, 3, 2);

-- upcoming missions
INSERT INTO space_mission (mission_name, description, status, launch_date, destination, cost, duration, crew_size, required_roles, bid_deadline, creator_comp_id, manager_comp_id, spaceship_id)
VALUES 
('Mission Future Gamma', 'Research mission to study asteroids.', 'Planned', '2025-01-05', 'Asteroid Belt', 70000000, 270, 12, 'Commander, Pilot, Mission Specialist, Flight Engineer, Medical Doctor', '2024-06-30', 3, 1, 3),
('Mission Future Delta', 'Mapping mission to Venus.', 'Planned', '2025-04-10', 'Venus', 60000000, 150, 8, 'Commander, Pilot, Mission Specialist, Flight Engineer', '2024-09-30', 1, 3, 4),
('Mission Future Epsilon', 'Tourism mission to the International Space Station.', 'Bidding', '2025-07-25', 'ISS', 40000000, 60, 6, 'Commander, Pilot, Mission Specialist, Medical Doctor', '2025-01-31', 2, 1, 5);

-- astronauts to past missions
INSERT INTO participates (astronaut_id, mission_id) VALUES 
(4, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Past Alpha')),
(5, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Past Alpha')),
(6, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Past Alpha')),
(7, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Past Alpha')),
(8, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Past Alpha')),
(9, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Past Alpha')),
(10, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Past Alpha')),
(11, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Past Alpha')),
(12, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Past Alpha')),
(13, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Past Alpha')),
(14, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Past Beta')),
(15, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Past Beta')),
(16, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Past Beta')),
(17, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Past Beta')),
(18, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Past Beta')),
(19, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Past Beta')),
(20, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Past Beta')),
(21, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Past Beta'));

-- astronauts to upcoming missions
INSERT INTO participates (astronaut_id, mission_id) VALUES 
(4, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Gamma')),
(5, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Gamma')),
(6, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Gamma')),
(7, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Gamma')),
(8, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Gamma')),
(9, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Gamma')),
(10, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Gamma')),
(11, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Gamma')),
(12, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Gamma')),
(13, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Gamma')),
(14, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Delta')),
(15, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Delta')),
(16, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Delta')),
(17, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Delta')),
(18, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Delta')),
(19, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Delta')),
(20, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Delta')),
(21, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Delta')),
(22, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Epsilon')),
(23, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Epsilon')),
(24, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Epsilon')),
(25, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Epsilon')),
(26, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Epsilon')),
(27, (SELECT mission_id FROM space_mission WHERE mission_name = 'Mission Future Epsilon'));


DELIMITER $$

CREATE TRIGGER update_mission_status
BEFORE UPDATE ON space_mission
FOR EACH ROW
BEGIN
    IF NEW.launch_date <= CURDATE() AND (NEW.status = 'Planned' OR NEW.status = 'Bidding') THEN
        SET NEW.status = 'In Progress';
    END IF;
END$$

DELIMITER ;
