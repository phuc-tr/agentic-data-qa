-- MySQL dump 10.13  Distrib 8.0.44, for Linux (x86_64)
--
-- Host: localhost    Database: billing
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `billing_history`
--

DROP TABLE IF EXISTS `billing_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing_history` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `phone` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `planId` int DEFAULT NULL,
  `billAmount` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `billAction` varchar(128) NOT NULL DEFAULT 'Unavailable',
  `billPerformer` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `billReason` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `paymentmethod` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `bounce` int DEFAULT NULL,
  `notes` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `creationdate` datetime DEFAULT '0000-00-00 00:00:00',
  `creationby` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `updatedate` datetime DEFAULT '0000-00-00 00:00:00',
  `updateby` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `username` (`phone`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=21186 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing_history`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `billing_history` WRITE;
/*!40000 ALTER TABLE `billing_history` DISABLE KEYS */;
INSERT INTO `billing_history` VALUES (11089,'92675167',31,'166','239','MersalService','New Charge','PrePaid',73,NULL,'2014-04-29 00:00:00','MersalService',NULL,NULL),(12400,'22865561',32,'300','540','MersalService','New Charge','PrePaid',240,NULL,'2014-06-01 00:00:00','MersalService',NULL,NULL),(14578,'22773796',32,'90','180','MersalService','New Charge','PrePaid',90,NULL,'2014-07-08 00:00:00','MersalService',NULL,NULL),(2078,'22956657',14,'240','360','MersalService','New Charge','PrePaid',120,NULL,'2013-04-21 00:00:00','MersalService',NULL,NULL),(3981,'22768942',27,'90','130','MersalService','New Charge','PrePaid',40,NULL,'2013-09-16 00:00:00','MersalService',NULL,NULL),(9211,'42442051',37,'30','37','MersalService','New Charge','PrePaid',7,NULL,'2014-03-14 00:00:00','MersalService',NULL,NULL),(19403,'92342316',32,'90','180','MersalService','New Charge','PrePaid',90,NULL,'2014-10-11 00:00:00','MersalService',NULL,NULL),(8003,'92670986',26,'30','37','MersalService','New Charge','PrePaid',7,NULL,'2014-02-08 00:00:00','MersalService',NULL,NULL),(14638,'42462714',29,'90','180','MersalService','New Charge','PrePaid',90,NULL,'2014-07-08 00:00:00','MersalService',NULL,NULL),(12519,'92386516',33,'30','37','MersalService','New Charge','PrePaid',7,NULL,'2014-06-03 00:00:00','MersalService',NULL,NULL);
/*!40000 ALTER TABLE `billing_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing_plans`
--

DROP TABLE IF EXISTS `billing_plans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing_plans` (
  `id` int NOT NULL AUTO_INCREMENT,
  `planName` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `sharing` int DEFAULT NULL,
  `planType` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `planBandwidthUp` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `planBandwidthDown` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `planTrafficTotal` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `planTrafficUp` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `planTrafficDown` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `planTrafficRefillCost` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Prepaid cost (NEW)',
  `planRecurring` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'new paltel',
  `planRecurringPeriod` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `planRecurringBillingSchedule` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT 'Fixed',
  `planCost` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'PrePaid Cost (OLD)',
  `planSetupCost` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'PostPaid Cost',
  `planTax` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `planCurrency` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `planActive` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT 'yes',
  `notes` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `creationdate` datetime DEFAULT '2000-01-01 00:00:00',
  `creationby` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT 'admin',
  `updatedate` datetime DEFAULT '2000-01-01 00:00:00',
  `updateby` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT 'admin',
  PRIMARY KEY (`id`),
  UNIQUE KEY `planName` (`planName`)
) ENGINE=MyISAM AUTO_INCREMENT=83 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing_plans`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `billing_plans` WRITE;
/*!40000 ALTER TABLE `billing_plans` DISABLE KEYS */;
INSERT INTO `billing_plans` VALUES (2,'H1Mb',24,'Home','192Kbps','1Mbps',NULL,NULL,NULL,'58','58','Monthly','Fixed','58','41',NULL,'NIS','yes',NULL,'2000-01-01 00:00:00','admin','2000-01-01 00:00:00',NULL),(56,'TS1Mb',24,'TS',NULL,NULL,NULL,NULL,NULL,'20','20',NULL,'Fixed','20','20',NULL,NULL,'yes',NULL,'2000-01-01 00:00:00','admin','2000-01-01 00:00:00','admin'),(66,'NH16Mb',24,'NH',NULL,NULL,NULL,NULL,NULL,'90','90',NULL,'Fixed','90','90',NULL,NULL,'yes',NULL,'2000-01-01 00:00:00','admin','2000-01-01 00:00:00','admin'),(13,'S0.5Mb',24,'Silver',NULL,NULL,NULL,NULL,NULL,'20','20',NULL,'Fixed','20','20',NULL,NULL,'yes',NULL,'2000-01-01 00:00:00','admin','2000-01-01 00:00:00','admin'),(9,'L0.5Mb',24,'Limited',NULL,NULL,NULL,NULL,NULL,'31','31','Monthly','Fixed','31','31',NULL,NULL,'yes',NULL,'2000-01-01 00:00:00','admin','2000-01-01 00:00:00','admin'),(71,'DC50Mb',24,'DC',NULL,NULL,NULL,NULL,NULL,'1000','1000',NULL,'Fixed','1000','700',NULL,NULL,'yes',NULL,NULL,NULL,NULL,NULL),(23,'DC4Mb',24,'DCommercial',NULL,NULL,NULL,NULL,NULL,'100','100',NULL,'Fixed','100','60',NULL,NULL,'yes',NULL,'2000-01-01 00:00:00','admin','2000-01-01 00:00:00','admin'),(16,'S4Mb',24,'Silver',NULL,NULL,NULL,NULL,NULL,'80','80',NULL,'Fixed','80','50',NULL,NULL,'yes',NULL,'2000-01-01 00:00:00','admin','2000-01-01 00:00:00','admin'),(40,'DS6Mb',24,'DS',NULL,NULL,NULL,NULL,NULL,'50','50',NULL,'Fixed','50','40',NULL,NULL,'yes',NULL,'2000-01-01 00:00:00','admin','2000-01-01 00:00:00','admin'),(78,'SH8Mb',24,NULL,NULL,NULL,NULL,NULL,NULL,'90','90',NULL,'Fixed','90','57',NULL,NULL,'yes',NULL,'2000-01-01 00:00:00','admin','2000-01-01 00:00:00','admin');
/*!40000 ALTER TABLE `billing_plans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `financial_summary`
--

DROP TABLE IF EXISTS `financial_summary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `financial_summary` (
  `id` int NOT NULL AUTO_INCREMENT,
  `finDate` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `total` double(32,2) DEFAULT NULL,
  `num_trans` int DEFAULT NULL,
  `num_customers` int DEFAULT NULL,
  `note` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `financial_summary`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `financial_summary` WRITE;
/*!40000 ALTER TABLE `financial_summary` DISABLE KEYS */;
INSERT INTO `financial_summary` VALUES (25,'2016/07',509429.50,0,30516,NULL),(14,'2015/10',684412.55,0,0,NULL),(27,'2016/09',861450.98,0,30080,NULL),(12,'2015/08',510949.57,0,0,NULL),(15,'2015/11',823647.05,0,0,NULL),(10,'2015/06',413431.67,0,0,NULL),(5,'2015/05',600027.30,0,0,NULL),(13,'2015/09',592922.82,0,0,NULL),(3,'2015/03',549255.30,0,0,NULL),(29,'2016/11',691405.02,0,30814,NULL);
/*!40000 ALTER TABLE `financial_summary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoice`
--

DROP TABLE IF EXISTS `invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoice` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL COMMENT 'user id of the userbillinfo table',
  `plan_id` int DEFAULT NULL COMMENT 'the plan_id of the billing_plans table',
  `date` datetime NOT NULL DEFAULT '2010-01-01 12:00:00',
  `amount` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'the amount cost of an item',
  `tax_amount` decimal(10,2) NOT NULL DEFAULT '0.15' COMMENT 'the tax amount for an item',
  `total` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'the total amount',
  `statusId` int NOT NULL,
  `notes` varchar(128) DEFAULT NULL COMMENT 'general notes/description',
  `creationdate` date DEFAULT '2010-01-01',
  `creationby` varchar(128) DEFAULT NULL,
  `updatedate` datetime DEFAULT '2010-01-01 12:00:00',
  `updateby` varchar(128) DEFAULT NULL,
  `discount` decimal(10,2) NOT NULL DEFAULT '0.00',
  `btype` varchar(3) DEFAULT NULL COMMENT '(n:normal generation,d:disconnected,r:reverse) and p: printed,u:unprinted',
  `nid` int DEFAULT NULL COMMENT 'this field for Reverse Invoice',
  `prefix` varchar(2) DEFAULT 'ZI' COMMENT 'ex(ZI,XI,...)',
  `generationid` int DEFAULT NULL,
  `offerName` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `generationID` (`generationid`),
  KEY `creationdate` (`creationdate`)
) ENGINE=MyISAM AUTO_INCREMENT=836509 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoice`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `invoice` WRITE;
/*!40000 ALTER TABLE `invoice` DISABLE KEYS */;
INSERT INTO `invoice` VALUES (394717,12756,26,'2014-07-15 00:00:00',30.00,4.80,34.80,5,'Done by MersalWS','2014-07-02','ISPSerever','2014-09-16 00:00:00',NULL,0.00,'nu',0,'ZI',45,NULL),(625940,30557,33,'2016-07-15 00:00:00',30.00,4.80,34.80,5,'Done by MersalWS','2016-07-01','ISPSerever','2016-07-17 00:00:00',NULL,0.00,'nu',0,'ZI',69,NULL),(88775,5099,2,'2012-06-15 00:00:00',58.00,8.41,66.41,5,'Done by MersalWS','2012-06-01','ISPSerever','2012-08-13 00:00:00',NULL,0.00,'nu',0,'ZI',20,NULL),(446213,11507,32,'2014-11-15 00:00:00',30.00,4.80,34.80,5,'Done by MersalWS','2014-11-01','ISPSerever','2014-12-17 00:00:00',NULL,0.00,'nu',0,'ZI',49,NULL),(226079,19789,4,'2013-06-15 00:00:00',110.00,17.60,127.60,5,'Done by MersalWS','2013-06-02','ISPSerever','2013-09-29 00:00:00',NULL,0.00,'nu',0,'ZI',32,NULL),(499723,8629,27,'2015-04-15 00:00:00',40.00,6.40,46.40,5,'Done by MersalWS','2015-04-01','ISPSerever','2015-06-17 00:00:00',NULL,0.00,'nu',0,'ZI',54,NULL),(167469,16072,14,'2013-02-15 00:00:00',28.23,4.23,32.46,5,'Done by MersalWS','2013-02-01','ISPSerever','2013-02-06 00:00:00',NULL,0.00,'nu',0,'ZI',28,NULL),(442200,12578,33,'2014-11-15 00:00:00',18.06,2.89,20.95,4,'Generated by ISP System _ Debited Line ','2014-11-01','ISPSerever',NULL,NULL,0.00,'nu',0,'ZI',49,NULL),(16524,4229,1,'2011-05-15 00:00:00',41.00,5.94,46.95,5,'Done by MersalWS','2011-05-01','ISPSerever','2011-05-11 00:00:00',NULL,0.00,'nu',0,'ZI',7,NULL),(237528,15207,14,'2013-07-15 00:00:00',35.00,5.60,40.60,5,'Done by MersalWS','2013-07-02','ISPSerever','2013-09-10 00:00:00',NULL,0.00,'nu',0,'ZI',33,NULL);
/*!40000 ALTER TABLE `invoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoice_status`
--

DROP TABLE IF EXISTS `invoice_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoice_status` (
  `id` int NOT NULL AUTO_INCREMENT,
  `value` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL DEFAULT '' COMMENT 'status value',
  `notes` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT 'general notes/description',
  `creationdate` datetime DEFAULT '0000-00-00 00:00:00',
  `creationby` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `updatedate` datetime DEFAULT '0000-00-00 00:00:00',
  `updateby` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoice_status`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `invoice_status` WRITE;
/*!40000 ALTER TABLE `invoice_status` DISABLE KEYS */;
INSERT INTO `invoice_status` VALUES (6,'partial','','2010-05-27 00:00:00','operator','2010-05-27 00:00:00','operator'),(3,'draft','','2010-05-27 00:00:00','operator','2010-05-27 00:00:00','operator'),(4,'sent','','2010-05-27 00:00:00','operator','2010-05-27 00:00:00','operator'),(1,'open','','2010-05-27 00:00:00','operator','2010-05-27 00:00:00','operator'),(2,'disputed','','2010-05-27 00:00:00','operator','2010-05-27 00:00:00','operator'),(5,'paid','','2010-05-27 00:00:00','operator','2010-05-27 00:00:00','operator');
/*!40000 ALTER TABLE `invoice_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `iptv_trans`
--

DROP TABLE IF EXISTS `iptv_trans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `iptv_trans` (
  `id` int NOT NULL AUTO_INCREMENT,
  `creationdate` date DEFAULT NULL,
  `new_iptv` int DEFAULT NULL,
  `activated_iptv` int DEFAULT NULL,
  `note` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=464 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iptv_trans`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `iptv_trans` WRITE;
/*!40000 ALTER TABLE `iptv_trans` DISABLE KEYS */;
INSERT INTO `iptv_trans` VALUES (171,'2018-11-11',25,627,NULL),(25,'2018-06-18',0,661,NULL),(360,'2019-05-18',24,778,NULL),(363,'2019-05-21',24,766,NULL),(375,'2019-06-02',25,749,NULL),(112,'2018-09-13',25,605,NULL),(281,'2019-02-28',27,786,NULL),(14,'2018-06-07',0,640,NULL),(328,'2019-04-16',23,795,NULL),(80,'2018-08-12',24,625,NULL);
/*!40000 ALTER TABLE `iptv_trans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mersalbills`
--

DROP TABLE IF EXISTS `mersalbills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mersalbills` (
  `phone` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `billID` int DEFAULT NULL,
  `paidDate` date DEFAULT NULL,
  `paidTime` time DEFAULT NULL,
  `amount` decimal(11,2) DEFAULT NULL,
  KEY `NewIndex1` (`billID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mersalbills`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `mersalbills` WRITE;
/*!40000 ALTER TABLE `mersalbills` DISABLE KEYS */;
INSERT INTO `mersalbills` VALUES (NULL,816059,NULL,NULL,NULL),(NULL,822322,NULL,NULL,NULL),(NULL,815328,NULL,NULL,NULL),(NULL,813245,NULL,NULL,NULL),(NULL,818431,NULL,NULL,NULL),(NULL,815153,NULL,NULL,NULL),(NULL,817958,NULL,NULL,NULL),(NULL,816632,NULL,NULL,NULL),(NULL,627547,NULL,NULL,NULL),(NULL,812155,NULL,NULL,NULL);
/*!40000 ALTER TABLE `mersalbills` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mersalbillsrollback`
--

DROP TABLE IF EXISTS `mersalbillsrollback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mersalbillsrollback` (
  `phone` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `billID` int DEFAULT NULL,
  `paidDate` date DEFAULT NULL,
  `paidTime` time DEFAULT NULL,
  `amount` decimal(11,2) DEFAULT NULL,
  KEY `NewIndex1` (`billID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mersalbillsrollback`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `mersalbillsrollback` WRITE;
/*!40000 ALTER TABLE `mersalbillsrollback` DISABLE KEYS */;
INSERT INTO `mersalbillsrollback` VALUES ('22793880.0',146391,'2013-02-02','18:32:10',90.85),('22321624.0',322532,'2014-01-28','13:31:33',35.36),('22218046.0',199616,'2013-04-06','09:37:18',30.19),('22561232.0',254498,'2014-02-06','16:02:47',40.60),('92385196.0',370829,'2014-06-08','12:04:15',34.80),('92383682.0',30256,'2013-09-03','13:01:02',54.30),('92577248.0',95311,'2012-08-28','19:33:38',20.04),('92397045.0',453911,'2014-11-23','16:43:53',25.52),('92383682.0',39840,'2013-11-04','15:24:18',120.23),('22793880.0',125641,'2013-02-02','18:32:08',90.85);
/*!40000 ALTER TABLE `mersalbillsrollback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mersalpaid`
--

DROP TABLE IF EXISTS `mersalpaid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mersalpaid` (
  `billID` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  PRIMARY KEY (`billID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mersalpaid`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `mersalpaid` WRITE;
/*!40000 ALTER TABLE `mersalpaid` DISABLE KEYS */;
INSERT INTO `mersalpaid` VALUES ('757852'),('748871'),('753677'),('763431'),('804816'),('752657'),('761177'),('769535'),('796764'),('792983');
/*!40000 ALTER TABLE `mersalpaid` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `invoice_id` int NOT NULL COMMENT 'invoice id of the invoices table',
  `amount` decimal(10,2) NOT NULL COMMENT 'the amount paid',
  `date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `type_id` int NOT NULL DEFAULT '1' COMMENT 'the type of the payment from payment_type',
  `notes` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT 'general notes/description',
  `creationdate` date DEFAULT '0000-00-00',
  `creationby` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `updatedate` date DEFAULT '0000-00-00',
  `updateby` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `NewIndex1` (`creationdate`)
) ENGINE=MyISAM AUTO_INCREMENT=733115 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES (263023,285084,58.00,'2013-12-08 12:21:32',1,'Done by Mersal WebSite ','2013-12-08','MersalWS',NULL,NULL),(498236,542611,34.80,'2015-09-19 12:18:13',1,'Done by Mersal WebSite ','2015-09-19','MersalWS',NULL,NULL),(210366,226722,40.60,'2013-07-27 19:26:16',1,'Done by Mersal WebSite ','2013-07-27','MersalWS',NULL,NULL),(289201,329083,35.96,'2014-02-11 20:21:31',1,'Done by Mersal WebSite ','2014-02-11','MersalWS',NULL,NULL),(378324,424855,40.60,'2014-09-16 20:56:25',1,'Done by Mersal WebSite ','2014-09-16','MersalWS',NULL,NULL),(49370,52303,40.08,'2012-01-21 12:52:45',1,'Done by Mersal WebSite ','2012-01-21','MersalWS',NULL,NULL),(617639,679759,44.85,'2017-04-30 11:40:58',1,'Done by Mersal WebSite ','2017-04-30','MersalWS',NULL,NULL),(545900,604992,34.80,'2016-04-07 13:17:37',1,'Done by Mersal WebSite ','2016-04-07','MersalWS',NULL,NULL),(358173,416165,1.50,'2014-08-03 11:26:48',1,'Done by Mersal WebSite ','2014-08-03','MersalWS',NULL,NULL),(609134,665809,46.40,'2017-03-10 18:05:49',1,'Done by Mersal WebSite ','2017-03-10','MersalWS',NULL,NULL);
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_type`
--

DROP TABLE IF EXISTS `payment_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `value` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL DEFAULT '' COMMENT 'type value',
  `notes` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT 'general notes/description',
  `creationdate` datetime DEFAULT '0000-00-00 00:00:00',
  `creationby` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `updatedate` datetime DEFAULT '0000-00-00 00:00:00',
  `updateby` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_type`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `payment_type` WRITE;
/*!40000 ALTER TABLE `payment_type` DISABLE KEYS */;
INSERT INTO `payment_type` VALUES (4,'PostPaid_RollBack','','2011-11-19 00:00:00','operator','0000-00-00 00:00:00',NULL),(1,'PostPaid','','2010-05-27 00:00:00','operator','2010-05-27 00:00:00','operator'),(3,'PrePaid_CARD','','2010-05-27 00:00:00','operator','2010-05-27 00:00:00','operator'),(2,'PrePaid_TOPUP','','2010-05-27 00:00:00','operator','2010-05-27 00:00:00','operator');
/*!40000 ALTER TABLE `payment_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prepaid_transaction`
--

DROP TABLE IF EXISTS `prepaid_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prepaid_transaction` (
  `id` int NOT NULL AUTO_INCREMENT,
  `balance_before` int NOT NULL,
  `amount` int NOT NULL,
  `bounce` int NOT NULL,
  `allowance` int NOT NULL,
  `balance_current` int NOT NULL,
  `due_date` date NOT NULL COMMENT 'Last Date (Finishing Date)',
  `userID` int NOT NULL,
  `trans_status` tinyint(1) NOT NULL,
  `creationdate` datetime NOT NULL,
  `note` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `type` int DEFAULT NULL COMMENT '1: normal charge, 2: rollback , 3: upgrade speed, 4: Allawance Trans(minus Trans Service# 68), 5: stoped (allowance==Balance)',
  PRIMARY KEY (`id`),
  KEY `userID` (`userID`),
  KEY `status` (`trans_status`),
  KEY `NewIndex1` (`creationdate`),
  KEY `NewIndex2` (`due_date`)
) ENGINE=MyISAM AUTO_INCREMENT=848143 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prepaid_transaction`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `prepaid_transaction` WRITE;
/*!40000 ALTER TABLE `prepaid_transaction` DISABLE KEYS */;
INSERT INTO `prepaid_transaction` VALUES (557115,0,90,90,0,180,'2018-08-18',48422,1,'2018-02-19 00:00:00',NULL,1),(391525,0,60,80,0,140,'2017-09-20',23269,1,'2017-05-03 00:00:00',NULL,1),(267244,0,150,201,0,351,'2017-08-17',64861,1,'2016-08-31 00:00:00',NULL,1),(335659,-1,90,121,0,210,'2017-08-15',56700,1,'2017-01-17 00:00:00',NULL,1),(700379,0,0,0,-5,0,'2018-12-06',54775,1,'2018-12-06 00:00:00',NULL,4),(611918,0,30,45,0,75,'2018-08-05',75881,1,'2018-05-22 00:00:00',NULL,1),(510469,0,90,121,0,211,'2018-07-11',55651,1,'2017-12-12 00:00:00',NULL,1),(677867,0,0,0,0,0,'2018-10-14',47470,1,'2018-10-14 00:00:00',NULL,5),(663168,0,0,0,0,0,'2018-09-05',87964,1,'2018-09-05 00:00:00',NULL,5),(841462,-2,90,90,0,178,'2020-02-13',54407,1,'2019-08-19 00:00:00',NULL,1);
/*!40000 ALTER TABLE `prepaid_transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prepaidcustomers`
--

DROP TABLE IF EXISTS `prepaidcustomers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prepaidcustomers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `counter` int DEFAULT NULL,
  `creationdate` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1234 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prepaidcustomers`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `prepaidcustomers` WRITE;
/*!40000 ALTER TABLE `prepaidcustomers` DISABLE KEYS */;
INSERT INTO `prepaidcustomers` VALUES (710,23510,'2018-03-25'),(912,19985,'2018-10-13'),(858,20377,'2018-08-20'),(272,25835,'2017-01-11'),(1176,19966,'2019-07-04'),(789,21788,'2018-06-12'),(529,25060,'2017-09-25'),(7,21951,'2016-04-21'),(328,26811,'2017-03-08'),(256,25651,'2016-12-26');
/*!40000 ALTER TABLE `prepaidcustomers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblactivationdate`
--

DROP TABLE IF EXISTS `tblactivationdate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblactivationdate` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uid` int NOT NULL,
  `activationdate` date DEFAULT NULL,
  `activationtime` time DEFAULT NULL,
  `note` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3246 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblactivationdate`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `tblactivationdate` WRITE;
/*!40000 ALTER TABLE `tblactivationdate` DISABLE KEYS */;
INSERT INTO `tblactivationdate` VALUES (2317,4955,'2016-06-07','15:52:08','Reconnect'),(2755,5730,'2017-05-22','13:28:20','Reconnect'),(91,6144,'2011-11-03','12:26:30','Reconnect'),(1192,8140,'2014-07-06','14:07:25','Reconnect'),(2985,6696,'2018-08-02','14:53:00','Reconnect'),(2832,4931,'2017-09-24','12:23:42','Reconnect'),(513,15945,'2013-04-10','14:20:03','Reconnect'),(319,11112,'2012-09-07','01:26:13','Reconnect'),(199,3974,'2012-05-13','15:49:26','Reconnect'),(572,11833,'2013-05-26','15:26:28','Reconnect');
/*!40000 ALTER TABLE `tblactivationdate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblbounce`
--

DROP TABLE IF EXISTS `tblbounce`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblbounce` (
  `id` int NOT NULL AUTO_INCREMENT,
  `bstart` int DEFAULT NULL,
  `bend` int DEFAULT NULL,
  `bstatus` varchar(11) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `bounce` float DEFAULT NULL,
  `creationdate` date DEFAULT NULL,
  `creationby` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `note` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblbounce`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `tblbounce` WRITE;
/*!40000 ALTER TABLE `tblbounce` DISABLE KEYS */;
INSERT INTO `tblbounce` VALUES (9,90,91,'Active',0,'2018-11-18',NULL,'new_paltel'),(17,30,31,'Active',2,'2018-11-18',NULL,'new_paltel'),(19,30,180,'Active',1,'2018-12-01',NULL,'old'),(1,0,29,'Active',0,'2018-11-18','me','old'),(16,0,29,'Active',0,'2018-11-18',NULL,'new_paltel'),(20,30,180,'Active',1.5,'2019-01-06',NULL,'old'),(15,30,31,'Active',2,'2018-11-18',NULL,'new'),(11,90,91,'Active',0,'2018-11-18',NULL,'new'),(7,60,180,'Active',1.34,'2018-11-18',NULL,'old'),(14,0,29,'Active',0,'2018-11-18',NULL,'new');
/*!40000 ALTER TABLE `tblbounce` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblcampaign`
--

DROP TABLE IF EXISTS `tblcampaign`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblcampaign` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `value` float NOT NULL,
  `cstatus` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Campaign Status',
  `cstart` date DEFAULT NULL COMMENT 'Campaign Start',
  `cend` date DEFAULT NULL COMMENT 'Campaign End',
  `speeds` varbinary(300) DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `creationdate` datetime DEFAULT '0000-00-00 00:00:00',
  `creationby` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `updatedate` datetime DEFAULT '0000-00-00 00:00:00',
  `updateby` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `period` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UniqueName` (`Name`)
) ENGINE=MyISAM AUTO_INCREMENT=211 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblcampaign`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `tblcampaign` WRITE;
/*!40000 ALTER TABLE `tblcampaign` DISABLE KEYS */;
INSERT INTO `tblcampaign` VALUES (9,'Colors 2011-05-24',0.25,'InActive','2011-05-24','2050-11-29',_binary 'C0.5Mb,C1Mb,C2Mb,C4Mb,H0.5Mb,H1Mb,H2Mb,H4Mb','كملنا الألوان-2','2011-05-28 00:00:00','CRM_ISP','2011-05-28 00:00:00','CRM_ISP',4),(14,'Ministry of Religious Endowments',0.25,'Active','0002-11-30','2050-11-29',_binary 'H1Mb','وزارة الأوقاف 25 بالمئة','2012-07-01 00:00:00','CRM_ISP','2013-05-01 00:00:00','CRM_ISP',0),(20,'tmayz w t2laq',0.5,'InActive','2013-04-08','2050-11-29',_binary 'C0.5Mb,C1Mb,C2Mb,C4Mb,H0.5Mb,H1Mb,H2Mb,H4Mb,L1Mb,L2Mb,L4Mb,S0.5Mb,S1Mb,S2Mb,S4Mb,C8Mb,H8Mb,S8Mb','تميز وتألق','2013-04-13 00:00:00','CRM_ISP','2013-04-13 00:00:00','CRM_ISP',3),(15,'kammel betak',0.25,'InActive','2012-10-13','2050-11-29',_binary 'C2Mb,H0.5Mb,H1Mb,H2Mb,H4Mb,L0.5Mb,L1Mb,L2Mb,L4Mb,S0.5Mb,S1Mb,S2Mb,C8Mb,H8Mb,S8Mb,DS1Mb,DS2Mb,DS4Mb,DS8Mb,DH1Mb,DH2Mb,DH4Mb,DH8Mb,DH12Mb,DC1Mb,DC2Mb,DC4Mb,DC8Mb','كمل بيتك','2012-10-13 00:00:00','CRM_ISP','2013-10-21 00:00:00','CRM_ISP',6),(6,'خصم 50 بالمئة',0.5,'Active','2010-12-04','2050-11-29',_binary 'C2Mb,H0.5Mb,H1Mb,H2Mb,H4Mb,L0.5Mb,L1Mb,L2Mb,L4Mb,S0.5Mb,S1Mb,S2Mb,S4Mb,C8Mb,H8Mb,S8Mb,DS1Mb,DS2Mb,DS4Mb,DS8Mb,DH1Mb,DH2Mb,DH4Mb,DH8Mb,DH12Mb,DC1Mb,DC2Mb,DC4Mb,DC8Mb,DH16Mb,DH30Mb,DS16Mb,DH50Mb,DC30Mb,DC50Mb,ST8Mb,ST16Mb,ST30Mb,ST50Mb','خصم مرسال 50 بالمئة','2011-01-03 00:00:00','CRM_ISP','2017-05-28 00:00:00','CRM_ISP',0),(203,'DS2 DH6 DC6',0.17,'InActive','2014-10-18','2050-11-29',_binary 'DS2Mb,DH6Mb,DC6Mb','DS2 DH6 DC6','2014-10-18 00:00:00','CRM_ISP','2014-10-18 00:00:00','CRM_ISP',6),(23,'yalla nteer2 2m',0.25,'InActive','2013-06-01','2050-11-29',_binary 'DC1Mb','تابع يلانطير2 خصم شهرين','2013-06-01 00:00:00','CRM_ISP','2013-10-21 00:00:00','CRM_ISP',2),(210,'ST80',0.8,'Active','0002-11-30','2050-11-29',_binary 'ST8Mb,ST16Mb,ST30Mb,ST50Mb','st 0.8 off','2017-05-27 00:00:00','CRM_ISP',NULL,NULL,0),(4,'Mersal 25%',0.25,'Active','2010-11-29','2050-11-29',_binary 'C2Mb,H0.5Mb,H1Mb,H2Mb,H4Mb,L0.5Mb,L1Mb,L2Mb,L4Mb,S0.5Mb,S1Mb,S2Mb,S4Mb,C8Mb,H8Mb,S8Mb,DS1Mb,DS2Mb,DS4Mb,DS8Mb,DH1Mb,DH2Mb,DH4Mb,DH8Mb,DH12Mb,DC1Mb,DC2Mb,DC4Mb,DC8Mb,DH16Mb,DC16Mb,DH30Mb,DS16Mb,DH50Mb,DC30Mb,DC50Mb,ST8Mb,ST16Mb,ST30Mb,ST50Mb','خصم مرسال 25 بالمئة','2010-11-01 00:00:00','CRM_ISP','2017-05-28 00:00:00','CRM_ISP',0),(13,'FreeLines',1,'Active','0002-11-30','0002-11-30',_binary 'C2Mb,H0.5Mb,H1Mb,H2Mb,H4Mb,L0.5Mb,L1Mb,L2Mb,L4Mb,S0.5Mb,S1Mb,S2Mb,S4Mb,C8Mb,H8Mb,S8Mb,DS1Mb,DS2Mb,DS4Mb,DS8Mb,DH1Mb,DH2Mb,DH4Mb,DH8Mb,DH12Mb,DC1Mb,DC2Mb,DC4Mb,DC8Mb,TM1,TM2,TM4,TM8,TM12,DH16Mb,DH30Mb,DH50Mb,ST8Mb,ST16Mb,ST30Mb,ST50Mb,DH24Mb,ST24Mb','الخطوط المجانية','2012-06-01 00:00:00','CRM_ISP','2018-07-31 00:00:00','CRM_ISP',0);
/*!40000 ALTER TABLE `tblcampaign` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblchangespeed`
--

DROP TABLE IF EXISTS `tblchangespeed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblchangespeed` (
  `id` int NOT NULL AUTO_INCREMENT,
  `planid` int NOT NULL,
  `userid` int NOT NULL,
  `changedate` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=87059 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblchangespeed`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `tblchangespeed` WRITE;
/*!40000 ALTER TABLE `tblchangespeed` DISABLE KEYS */;
INSERT INTO `tblchangespeed` VALUES (64227,28,56725,'2018-01-01'),(58281,28,49239,'2017-04-04'),(30994,27,42103,'2015-04-02'),(71449,28,24795,'2018-01-29'),(11217,14,17151,'2013-06-15'),(54569,27,35323,'2016-12-31'),(5772,13,14489,'2012-10-20'),(70755,29,51701,'2018-01-25'),(72381,29,82898,'2018-02-12'),(41369,32,17873,'2015-12-10');
/*!40000 ALTER TABLE `tblchangespeed` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbldebited`
--

DROP TABLE IF EXISTS `tbldebited`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tbldebited` (
  `id` int NOT NULL AUTO_INCREMENT,
  `number` int DEFAULT NULL,
  `amount` decimal(32,0) DEFAULT NULL,
  `debitedType` int DEFAULT NULL,
  `creationdate` date DEFAULT NULL,
  `note` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6527 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbldebited`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `tbldebited` WRITE;
/*!40000 ALTER TABLE `tbldebited` DISABLE KEYS */;
INSERT INTO `tbldebited` VALUES (934,51804,1990248,1,'2015-01-15','InvoiceDebited'),(4955,57674,2287793,1,'2018-08-04','InvoiceDebited'),(1545,432,4959,3,'2015-08-06','InvoiceDebited'),(1770,341,4061,3,'2015-10-20','InvoiceDebited'),(4100,3939,39416,2,'2017-12-06','InvoiceDebited'),(624,353,4053,3,'2014-10-03','InvoiceDebited'),(4214,3939,39416,2,'2018-01-13','InvoiceDebited'),(1065,279,3203,3,'2015-02-27','InvoiceDebited'),(1865,4075,40778,2,'2015-11-21','InvoiceDebited'),(3731,3952,39546,2,'2017-08-05','InvoiceDebited');
/*!40000 ALTER TABLE `tbldebited` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbldeviceinstallments`
--

DROP TABLE IF EXISTS `tbldeviceinstallments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tbldeviceinstallments` (
  `insID` int NOT NULL AUTO_INCREMENT,
  `transID` int NOT NULL,
  `userID` int NOT NULL,
  `amount` decimal(11,2) NOT NULL,
  `invoiceStatus` tinyint(1) NOT NULL,
  `invoiceId` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `paid` tinyint(1) NOT NULL DEFAULT '0',
  `paymentDate` date DEFAULT NULL,
  `creationdate` date NOT NULL,
  `note` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `tax` decimal(11,2) DEFAULT NULL,
  `total` decimal(11,2) DEFAULT NULL,
  PRIMARY KEY (`insID`),
  KEY `InvoiceID` (`invoiceId`)
) ENGINE=InnoDB AUTO_INCREMENT=38502 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbldeviceinstallments`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `tbldeviceinstallments` WRITE;
/*!40000 ALTER TABLE `tbldeviceinstallments` DISABLE KEYS */;
INSERT INTO `tbldeviceinstallments` VALUES (12631,870,12749,8.70,1,'ZI0376362',0,NULL,'2013-06-15','1',1.30,10.00),(31447,1961,4587,10.00,1,'ZI0537324',1,'2015-09-15','2015-08-02','2',1.60,11.60),(25748,1896,31532,8.62,1,'ZI0413928',1,'2014-09-11','2014-01-08','1',1.38,10.00),(16338,1122,26513,8.62,1,'ZI0412128',1,'2014-08-07','2013-07-17','1',1.38,10.00),(27401,2040,31707,8.62,1,'ZI0439523',1,'2014-12-08','2014-02-23','1',1.38,10.00),(7239,498,23409,8.70,1,'ZI0227947',1,'2013-06-08','2013-05-04','1',1.30,10.00),(27470,2046,26333,8.62,1,'ZI0390790',1,'2014-12-16','2014-02-23','1',1.38,10.00),(26521,1956,30949,8.62,1,'ZI0439302',1,'2014-10-14','2014-01-28','1',1.38,10.00),(23516,1696,2431,8.62,1,'ZI0418190',1,'2014-09-13','2013-12-17','1',1.38,10.00),(19083,1313,27926,8.62,1,'ZI0399786',1,'2014-08-02','2013-09-21','1',1.38,10.00);
/*!40000 ALTER TABLE `tbldeviceinstallments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbldevices`
--

DROP TABLE IF EXISTS `tbldevices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tbldevices` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `deviceName` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `deviceDesc` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `cost` decimal(11,2) DEFAULT NULL,
  `creationdate` date DEFAULT NULL,
  `note` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT '0: Device Installment, 1: Fix IP',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `deviceName` (`deviceName`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbldevices`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `tbldevices` WRITE;
/*!40000 ALTER TABLE `tbldevices` DISABLE KEYS */;
INSERT INTO `tbldevices` VALUES (11,'TP-Link  1  Port','TP-Link  1  Port',120.00,'2013-04-02','1'),(20,'FIXIP','FIXIP',10.00,'2013-10-26','2'),(25,'IPTV','IP-TV',40.00,'2017-01-28','4'),(23,'TP-LINK-TD-W8901N','TP-LINK-TD-W8901N',120.00,'2013-12-25','1'),(4,'TestName','TestDesc',2000.00,'2013-03-23','1'),(22,'Debited','Debited',0.00,NULL,'1'),(12,'TP-Link 8951 4port wireless','TP-Link 4port wireless',150.00,'2013-04-02','1'),(17,'TP-Link 1 Port Wiry','TP-Link 1 Port Wiry',90.00,'2013-05-04','1'),(26,'SHOWTV','ShowTV-2',100.00,'2019-03-30','5'),(16,'GoldWeb 4port Wireless','GoldWeb 4port Wireless',150.00,'2013-05-04','1');
/*!40000 ALTER TABLE `tbldevices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbldevicetrans`
--

DROP TABLE IF EXISTS `tbldevicetrans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tbldevicetrans` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `itemID` int NOT NULL,
  `UserId` int DEFAULT NULL,
  `Cost` decimal(10,2) DEFAULT NULL,
  `Months` int DEFAULT NULL,
  `creationdate` datetime DEFAULT NULL,
  `note` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT '0: Devices Installments, 1: Fix IP',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=6519 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbldevicetrans`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `tbldevicetrans` WRITE;
/*!40000 ALTER TABLE `tbldevicetrans` DISABLE KEYS */;
INSERT INTO `tbldevicetrans` VALUES (3924,24,65604,5.00,0,'2016-09-29 00:00:00','3'),(5836,24,41319,5.00,0,'2018-08-11 00:00:00','3'),(1316,13,27900,103.45,12,'2013-09-22 00:00:00','1'),(4989,20,20729,0.00,0,'2017-07-27 00:00:00','2'),(1770,21,30546,103.45,12,'2013-12-24 00:00:00','1'),(829,12,25553,130.43,15,'2013-05-30 00:00:00','1'),(6514,24,25667,5.00,0,'2019-08-28 00:00:00','3'),(5652,20,65217,10.00,0,'2018-04-24 00:00:00','2'),(278,13,21812,104.35,12,'2013-04-06 00:00:00','1'),(5784,24,75299,5.00,0,'2018-07-18 00:00:00','3');
/*!40000 ALTER TABLE `tbldevicetrans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblgeneration`
--

DROP TABLE IF EXISTS `tblgeneration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblgeneration` (
  `gid` int NOT NULL AUTO_INCREMENT,
  `gdate` date DEFAULT NULL,
  `gtime` time DEFAULT NULL,
  `month` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `note` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`gid`)
) ENGINE=InnoDB AUTO_INCREMENT=107 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblgeneration`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `tblgeneration` WRITE;
/*!40000 ALTER TABLE `tblgeneration` DISABLE KEYS */;
INSERT INTO `tblgeneration` VALUES (103,'2019-05-03',NULL,'2019-04',NULL),(83,'2017-09-02',NULL,'2017-08',NULL),(6,'2011-04-01','01:00:00','2011-03',NULL),(46,'2014-08-01',NULL,'2014-07',NULL),(3,'2011-01-04','23:40:54','2011-12',NULL),(11,'2011-09-03',NULL,'2011-08',NULL),(23,'2012-09-01',NULL,'2012-08',NULL),(79,'2017-05-03',NULL,'2017-04',NULL),(78,'2017-04-02',NULL,'2017-03',NULL),(29,'2013-03-01',NULL,'2013-02',NULL);
/*!40000 ALTER TABLE `tblgeneration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbllinetransactions`
--

DROP TABLE IF EXISTS `tbllinetransactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tbllinetransactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `transdate` date NOT NULL,
  `transtime` time DEFAULT '00:00:00',
  `typeid` int DEFAULT NULL,
  `billid` int DEFAULT NULL,
  `description` varbinary(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `NewIndex1` (`typeid`),
  KEY `NewIndex2` (`billid`)
) ENGINE=InnoDB AUTO_INCREMENT=1222439 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbllinetransactions`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `tbllinetransactions` WRITE;
/*!40000 ALTER TABLE `tbllinetransactions` DISABLE KEYS */;
INSERT INTO `tbllinetransactions` VALUES (43245,'2012-08-15','14:53:50',4,2470,_binary 'Reconnect'),(119588,'2013-11-25','08:24:29',6,8309,_binary 'Debited with 3 or more'),(128836,'2014-01-01','11:08:27',1,0,_binary 'New Line'),(151103,'2014-03-31','10:28:26',1,0,_binary 'New Line'),(904386,'2018-02-08','13:22:00',18,71851,_binary 'Active_Debited'),(1039492,'2018-10-07','21:52:47',18,87783,_binary 'Active_Debited'),(2423,'2011-01-16','23:16:01',3,3156,_binary 'Activated'),(211669,'2014-11-12','07:21:52',6,6890,_binary 'Debited with 3 or more'),(167410,'2014-06-11','12:56:17',16,26529,_binary 'No Credits'),(998796,'2018-07-16','13:02:19',18,39969,_binary 'Active_Debited');
/*!40000 ALTER TABLE `tbllinetransactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbllinetype`
--

DROP TABLE IF EXISTS `tbllinetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tbllinetype` (
  `id` int NOT NULL AUTO_INCREMENT,
  `transtype` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `creationdate` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbllinetype`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `tbllinetype` WRITE;
/*!40000 ALTER TABLE `tbllinetype` DISABLE KEYS */;
INSERT INTO `tbllinetype` VALUES (12,'Abuse',NULL),(4,'Reconnect',NULL),(10,'ReActivate',NULL),(1,'New Line',NULL),(6,'Debited',NULL),(7,'PostPaid',NULL),(14,'VIP',NULL),(9,'PrePaid',NULL),(18,'Post2Pre',NULL),(11,'Decancelled',NULL);
/*!40000 ALTER TABLE `tbllinetype` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-21 12:28:43
