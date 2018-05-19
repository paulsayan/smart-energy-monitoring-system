-- MySQL dump 10.13  Distrib 5.7.22, for Linux (x86_64)
--
-- Host: localhost    Database: tmp
-- ------------------------------------------------------
-- Server version	5.7.22-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `devices`
--

DROP TABLE IF EXISTS `devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `devices` (
  `id` varchar(30) NOT NULL,
  `name` varchar(30) NOT NULL,
  `state` tinyint(1) NOT NULL,
  `owner` int(11) NOT NULL,
  `authtoken` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `owner` (`owner`),
  CONSTRAINT `devices_ibfk_1` FOREIGN KEY (`owner`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devices`
--

LOCK TABLES `devices` WRITE;
/*!40000 ALTER TABLE `devices` DISABLE KEYS */;
INSERT INTO `devices` VALUES ('1002_1GPz4AP8','TableFan 1',0,1002,'fb9b1af6-12ae-470a-a661-8f0f71b1dd57'),('1002_GrZtwF6o','TableFan 1',0,1002,'6e192e2b-23ba-420b-9bcf-6004d0935d66'),('1003_h5AAUxnU','TableFan 1',0,1003,'c6166404-ee60-44d4-8b3b-fe557d9c4ba9'),('1007_pCEyiF2K','TubeLight X',0,1007,'26ce90e3-2e6c-4184-b5f2-6618c1ecb3dd'),('1009_2zOzhy7z','Fan 1',0,1009,'695ea717-6ccb-4ff8-a5d3-d51a63280a9a'),('1009_div738Ol','Tubelight 1',0,1009,'aa8587ce-3a62-4349-abee-3e0cb5825f61'),('1009_FgQd0ar2','Fan X',0,1009,'e58d9156-5cb0-463f-955e-f7fa8fb90de6'),('1009_tuI7fp0k','Bulb X',0,1009,'0fdb5750-e140-4556-a97d-fd585b64f21b');
/*!40000 ALTER TABLE `devices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notifications` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `time` datetime NOT NULL,
  `type` varchar(30) NOT NULL,
  `msg` varchar(500) DEFAULT NULL,
  `readn` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
INSERT INTO `notifications` VALUES (1,1009,'2018-05-13 22:48:09','ENERGYC_QUOTA_EXCEEDED','Your devices have exceeded the energy consumption quota for the billing period                 2018-05-04 to 2018-06-02.',0);
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sessions`
--

DROP TABLE IF EXISTS `sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sessions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` varchar(30) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime DEFAULT NULL,
  `energy_consumed` double(20,8) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`),
  CONSTRAINT `sessions_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1058 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessions`
--

LOCK TABLES `sessions` WRITE;
/*!40000 ALTER TABLE `sessions` DISABLE KEYS */;
INSERT INTO `sessions` VALUES (1003,'1009_tuI7fp0k','2018-05-04 23:37:15','2018-05-05 00:46:16',24.35640000),(1008,'1009_tuI7fp0k','2018-05-05 04:15:20','2018-05-06 04:10:03',24.35640000),(1017,'1009_tuI7fp0k','2018-05-06 17:49:08','2018-05-06 17:50:18',2.51000000),(1022,'1009_tuI7fp0k','2018-05-06 18:26:37',NULL,NULL),(1023,'1009_tuI7fp0k','2018-05-06 18:36:54',NULL,NULL),(1025,'1009_tuI7fp0k','2018-05-06 18:59:30',NULL,NULL),(1033,'1009_div738Ol','2018-05-07 23:47:49','2018-05-07 23:47:52',28.35640000),(1035,'1009_div738Ol','2018-05-08 03:51:09',NULL,NULL),(1036,'1009_2zOzhy7z','2018-05-08 04:00:03',NULL,NULL),(1037,'1009_tuI7fp0k','2018-05-09 20:01:46','2018-05-09 20:04:27',3.04130000),(1044,'1009_tuI7fp0k','2018-05-11 03:04:46','2018-05-11 03:05:49',1.17400000),(1045,'1009_tuI7fp0k','2018-05-13 21:53:46','2018-05-13 21:55:11',2.71800000),(1047,'1009_tuI7fp0k','2018-05-13 21:57:22','2018-05-13 21:58:25',2.38730000),(1048,'1009_tuI7fp0k','2018-05-13 22:08:17','2018-05-13 22:08:46',420.05000000),(1049,'1009_tuI7fp0k','2018-05-13 22:09:30','2018-05-13 22:10:32',420.05000000),(1050,'1009_tuI7fp0k','2018-05-13 22:49:22','2018-05-13 22:51:22',4.30990000),(1051,'1009_tuI7fp0k','2018-05-13 23:41:04','2018-05-13 23:41:10',0.14250000),(1052,'1009_tuI7fp0k','2018-05-14 03:48:02','2018-05-14 03:48:56',1.92030000),(1053,'1009_tuI7fp0k','2018-05-14 03:51:30','2018-05-14 03:53:30',4.42570000),(1054,'1009_tuI7fp0k','2018-05-14 03:59:18','2018-05-14 04:02:04',5.23760000),(1055,'1009_tuI7fp0k','2018-05-14 04:03:17','2018-05-14 04:03:29',0.21320000),(1056,'1009_tuI7fp0k','2018-05-14 04:04:00','2018-05-14 04:05:29',2.28980000),(1057,'1009_tuI7fp0k','2018-05-16 20:07:01','2018-05-16 20:09:22',5.58260000);
/*!40000 ALTER TABLE `sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student` (
  `name` varchar(30) DEFAULT NULL,
  `marks` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES ('XYZ',92.5),('PQR',85.6);
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tmp1`
--

DROP TABLE IF EXISTS `tmp1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tmp1` (
  `id` char(10) NOT NULL,
  `name` char(30) DEFAULT NULL,
  `marks` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tmp1`
--

LOCK TABLES `tmp1` WRITE;
/*!40000 ALTER TABLE `tmp1` DISABLE KEYS */;
INSERT INTO `tmp1` VALUES ('145opt','rtqs',57.234),('456abc','helloworld',45.6317),('456abd','hello',545.6317),('46587','mark',84.5),('46589','mark',84.5),('5689','john',45.63),('78587','ivy',76.52);
/*!40000 ALTER TABLE `tmp1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `pwd` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=1010 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1000,'s1','s1@xyz.com','pbkdf2:sha256:50000$YdCcJSYD$4e3400f284dd77c1282491620ac7e6c49c87aa8b09c6fd6b2d19b8f6a0d0aefc'),(1002,'s2','s2@xyz.com','pbkdf2:sha256:50000$YdCcJSYD$4e3400f284dd77c1282491620ac7e6c49c87aa8b09c6fd6b2d19b8f6a0d0aefc'),(1003,'s3','s3@xyz.com','pbkdf2:sha256:50000$YdCcJSYD$4e3400f284dd77c1282491620ac7e6c49c87aa8b09c6fd6b2d19b8f6a0d0aefc'),(1004,'Mohan','mohan1@gmail.com','pbkdf2:sha256:50000$YdCcJSYD$4e3400f284dd77c1282491620ac7e6c49c87aa8b09c6fd6b2d19b8f6a0d0aefc'),(1005,'Mohan 2','mohan2@gmail.com','pbkdf2:sha256:50000$YdCcJSYD$4e3400f284dd77c1282491620ac7e6c49c87aa8b09c6fd6b2d19b8f6a0d0aefc'),(1006,'TesterX','test@test.com','pbkdf2:sha256:50000$YdCcJSYD$4e3400f284dd77c1282491620ac7e6c49c87aa8b09c6fd6b2d19b8f6a0d0aefc'),(1007,'Nasirul','nasirul@test.com','pbkdf2:sha256:50000$YdCcJSYD$4e3400f284dd77c1282491620ac7e6c49c87aa8b09c6fd6b2d19b8f6a0d0aefc'),(1009,'Arjun','arjun@test.com','pbkdf2:sha256:50000$3uauJs44$7f8f8970f3918dfe1175a2bd7b4e88938d722d8913f9e9030c15198ffafbae30');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usersettings`
--

DROP TABLE IF EXISTS `usersettings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usersettings` (
  `user_id` int(11) NOT NULL,
  `setting` varchar(30) NOT NULL,
  `svalue` varchar(100) NOT NULL,
  PRIMARY KEY (`user_id`,`setting`),
  CONSTRAINT `usersettings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usersettings`
--

LOCK TABLES `usersettings` WRITE;
/*!40000 ALTER TABLE `usersettings` DISABLE KEYS */;
INSERT INTO `usersettings` VALUES (1007,'billingcycle','30'),(1007,'energyc_quota','50'),(1007,'lastbilldate','2018-05-05'),(1009,'billingcycle','30'),(1009,'energyc_quota','800'),(1009,'lastbilldate','2018-05-03');
/*!40000 ALTER TABLE `usersettings` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-05-17  3:59:45
