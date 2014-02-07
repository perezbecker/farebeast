-- Create farebeast database containing user, flight, fares, flight groups, and group fare data. 
-- To start SQL, run on terminal:
-- mysql -uroot
-- Inside mysql run:
-- \. create_database.sql 



CREATE DATABASE farebeast;
USE farebeast;

CREATE TABLE `users` (
    `uid` int NOT NULL AUTO_INCREMENT,
    `user` varchar(100) NOT NULL,
    `password` varchar(100) NOT NULL,
    `email` varchar(100) NOT NULL,
    `mobile` char(10) NOT NULL, 
    `carrier` varchar(100) NOT NULL,
    `datejoined` date NOT NULL,
PRIMARY KEY (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `flights` (
    `fid` int NOT NULL AUTO_INCREMENT, 
    `portA` char(3) NOT NULL,
    `portB` char(3) NOT NULL,
    `dateA` date NOT NULL,
    `dateB` date NOT NULL,
PRIMARY KEY (`fid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `fares` (
    `fareid` int NOT NULL AUTO_INCREMENT,
    `searchtime` datetime NOT NULL,
    `fid` int NOT NULL,
    `expediafare` int NOT NULL,
    `kayakfare`int NOT NULL,
PRIMARY KEY (`fareid`),
KEY `index_flights_fid` (`fid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `flightgroups` (
    `fgid` int NOT NULL AUTO_INCREMENT,
    `fgname` varchar(100), 
    `uid` int NOT NULL,
    `pref` int,
    `alarm` int, 
    `fid01` int,
    `fid02` int,
    `fid03` int,
    `fid04` int,
    `fid05` int,
    `fid06` int,
    `fid07` int,
    `fid08` int,
    `fid09` int,
    `fid10` int,
    `fid11` int,
    `fid12` int,
    `fid13` int,
    `fid14` int,
    `fid15` int,
    `fid16` int,
    `fid17` int,
    `fid18` int,
    `fid19` int,
    `fid20` int,
PRIMARY KEY (`fgid`),
KEY `index_users_uid` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `groupfares` (
    `groupfareid` int NOT NULL AUTO_INCREMENT, 
    `grouptime` datetime NOT NULL, 
    `fgid` int NOT NULL, 
    `fid` int NOT NULL, 
    `fare` int NOT NULL, 
    `website` varchar(100) NOT NULL, 
    `searchtime` datetime NOT NULL, 
    `alert` int NOT NULL, 
PRIMARY KEY (`groupfareid`),
KEY `index_flights_fid` (`fid`),
KEY `index_flightgroups_fgid` (`fgid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
