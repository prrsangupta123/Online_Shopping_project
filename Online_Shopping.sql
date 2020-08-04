
-- MySQL dump 10.13  Distrib 5.7.23, for Linux (x86_64)
--
-- Host: localhost    Database: Company

DROP DATABASE IF EXISTS `Online_Shopping`;
CREATE SCHEMA `Online_Shopping`;
USE `Online_Shopping`;

DROP TABLE IF EXISTS `Seller`;

CREATE TABLE `Seller` (
  `Seller_id` int(11) NOT NULL,
  `First_name` varchar(30) NOT NULL,
  `Middle_name` varchar(30) ,
  `Last_name` varchar(30) NOT NULL,
  `Seller_address` varchar(64) NOT NULL,
  PRIMARY KEY (`Seller_id`)
 
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


LOCK TABLES `Seller` WRITE;
INSERT INTO `Seller` VALUES (1,'Nikunj','nik','nawal','32/91 mahu indore'),(2,'satyam','viksit','pansari','patel nagar bihar'),(3,'manas','manoj','kabre','B-302 aishwarya serenty bangalore'),(4,'anubhav','rajesh','sharma','ridge road near iit bombay'),(5,'subodh','sunil','sondkar','catalyser vadodara');
UNLOCK TABLES;

DROP TABLE IF EXISTS `SellerContact`;
CREATE TABLE `SellerContact` (
  `Seller_id` int(9) NOT NULL,
  `Seller_contact` varchar(20) NOT NULL,
  PRIMARY KEY (`Seller_id`)
 
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
LOCK TABLES `SellerContact` WRITE;
INSERT INTO `SellerContact` VALUES (1,'1234567891'),(2,'2124567890'),(3,'8274629871'),(4,'4536567869'),(5,'1232345657');
UNLOCK TABLES;


DROP TABLE IF EXISTS `Driver`;
CREATE TABLE `Driver` (
  `Driver_id` int(11) NOT NULL,
  `First_name` varchar(30) NOT NULL,
  `Middle_name` varchar(30) ,
  `Last_name` varchar(30) NOT NULL,
  `Vehicle_id` varchar(64) NOT NULL,
  PRIMARY KEY (`Driver_id`)
 
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
LOCK TABLES `Driver` WRITE;
INSERT INTO `Driver` VALUES (1,'Alice','malice','salice','0000'),(2,'Elizabeth','eli','seli','1010'),(3,'Michael','Mik','johny','2111'),(4,'john','jack','jam','2345'),(5,'Joy','joel','joe','5432'),(6,'maddy','abc','dce','0987');
UNLOCK TABLES;


DROP TABLE IF EXISTS `DriverContact`;
CREATE TABLE `DriverContact` (
  `Driver_id` int(9) NOT NULL,
  `Driver_contact` varchar(11) NOT NULL,
  PRIMARY KEY (`Driver_id`)
  
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
LOCK TABLES `DriverContact` WRITE;
INSERT INTO `DriverContact` VALUES (1,'2313456745'),(2,'6565454345'),(3,'9878765676'),(4,'9870989876'),(5,'8767890987'),(6,'7654345678');
UNLOCK TABLES;
DROP TABLE IF EXISTS `Buyer`;
CREATE TABLE `Buyer` (
  `Buyer_id` int(11) NOT NULL,
  `First_name` varchar(30) NOT NULL,
  `Middle_name` varchar(30) ,
  `Last_name` varchar(30) NOT NULL,
  `Buyer_address` varchar(64) NOT NULL,
  PRIMARY KEY (`Buyer_id`)
  
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
LOCK TABLES `Buyer` WRITE;
INSERT INTO `Buyer` VALUES (1,'anishka','chikka','sachdeva','B-10 lahore'),(2,'radhika','radhi','rao','90-street north bombay'),(3,'prerna','shanjeet','gupta','gandhi nagar shahjahapur'),(4,'harshita','chutki','upadhyay','kamlakar nagar agra'),(5,'utkarsh','ut','mishra','phoda nagar jabalpur');
UNLOCK TABLES;

DROP TABLE IF EXISTS `BuyerContact`;
CREATE TABLE `BuyerContact` (
  `Buyer_id` int(9) NOT NULL,
  `Buyer_contact` varchar(11) NOT NULL,
  PRIMARY KEY (`Buyer_id`)
  
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `BuyerContact` WRITE;
INSERT INTO `BuyerContact` VALUES (1,'7364546373'),(2,'9878934567'),(3,'6789876543'),(4,'1234567123'),(5,'4535434565');
UNLOCK TABLES;

DROP TABLE IF EXISTS `Item`;
CREATE TABLE `Item` (
  `Item_id` int(11) NOT NULL,
  `Item_name` varchar(30) NOT NULL,
  `Cat_id` int(11) NOT NULL,
  PRIMARY KEY (`Item_id`),
  UNIQUE KEY `Item_name` (`Item_name`)
  
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
LOCK TABLES `Item` WRITE;
INSERT INTO `Item` VALUES (1,'jeans',1),(2,'shirt',1),(3,'dress',1),(4,'suit',1),(5,'iphone 11 pro',2),(6,'onplus7pro',2),(7,'baby bath and skin care',3),(8,'household cleaning',3);
UNLOCK TABLES;
DROP TABLE IF EXISTS `ItemCost`;
CREATE TABLE `ItemCost` (
  `Item_id` int(11) NOT NULL,
  `Seller_id` int(15) NOT NULL,
  `Item_cost` int(11) NOT NULL,
  PRIMARY KEY (`Item_id`)
 
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `ItemCost` WRITE;
INSERT INTO `ItemCost` VALUES (1,2,1000),(2,4,510),(3,1,850),(4,4,900),(5,3,50000),(6,3,39000),(7,5,300),(8,5,500);
UNLOCK TABLES;


DROP TABLE IF EXISTS `ItemSellPrice`;
CREATE TABLE `ItemSellPrice` (
  `Item_id` int(11) NOT NULL,
  `Item_sale_price` int(15) NOT NULL,
  PRIMARY KEY (`Item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `ItemSellPrice` WRITE;
INSERT INTO `ItemSellPrice` VALUES (1,1100),(2,561),(3,935),(4,990),(5,50500),(6,39390),(7,330),(8,550);
UNLOCK TABLES;

DROP TABLE IF EXISTS `Category`;
CREATE TABLE `Category` (
  `Cat_name` varchar(15) NOT NULL,
  `Cat_id` int(11) NOT NULL,
  PRIMARY KEY (`Cat_id`),
  UNIQUE KEY `Cat_name` (`Cat_name`)
 
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `Category` WRITE;
INSERT INTO `Category` VALUES ('clothing',1),('mobile',2),('grocery',3);
UNLOCK TABLES;

DROP TABLE IF EXISTS `Payment`;
CREATE TABLE `Payment` (
  `Purchase_id` int(9) NOT NULL,
  `Item_id` int(11) NOT NULL,
  `Profit` int(11) DEFAULT NULL,
  PRIMARY KEY (`Purchase_id`)
 
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `Purchase`;
CREATE TABLE `Purchase` (
  `Purchase_id` int(9) NOT NULL,
  `Driver_id` int(11) NOT NULL,
  `Buyer_id` int(11) NOT NULL,
  `Time_of_delivery` date DEFAULT NULL,
  `Time_of_purchase` date NOT NULL,
  PRIMARY KEY(`Purchase_id`)
  
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `Delivery`;
CREATE TABLE `Delivery` (
  `Purchase_id` int(11) NOT NULL,
  `Driver_id` int(11) NOT NULL,
  `Delivery_time` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`Driver_id`, `Purchase_id`)
  
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
