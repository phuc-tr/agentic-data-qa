-- MySQL dump 10.13  Distrib 8.0.44, for Linux (x86_64)
--
-- Host: localhost    Database: bsadb
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
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket` (
  `ticket_id` int NOT NULL AUTO_INCREMENT,
  `ticket_customer_id` int unsigned NOT NULL,
  `ticket_status_id` int NOT NULL,
  `ticket_type_id` int NOT NULL,
  `ticket_description` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci,
  `ticket_priority_id` int NOT NULL,
  `ticket_owner_id` int NOT NULL,
  `ticket_assignedto_id` int DEFAULT NULL,
  `ticket_creationdate` date NOT NULL,
  `ticket_creationtime` time NOT NULL,
  `ticket_closed_by_id` int DEFAULT NULL,
  `ticket_closedate` date DEFAULT NULL,
  `ticket_closetime` time DEFAULT NULL,
  `ticket_updated_by_id` int DEFAULT NULL,
  `ticket_updated_date` datetime DEFAULT NULL,
  `ticket_note` varchar(1000) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `ticket_followup_id` int DEFAULT NULL,
  PRIMARY KEY (`ticket_id`),
  KEY `FK_Userbillinfo` (`ticket_customer_id`),
  KEY `FK_ticket_Status` (`ticket_status_id`),
  KEY `FK_ticket_type` (`ticket_type_id`),
  KEY `FK_ticket_priority` (`ticket_priority_id`),
  KEY `FK_ticket_user` (`ticket_owner_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11127 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `ticket` WRITE;
/*!40000 ALTER TABLE `ticket` DISABLE KEYS */;
INSERT INTO `ticket` VALUES (8372,38977,5,40,'خلل شبك على جهاز تغيير كلمة مرور خلل تشفير _ CRC Errors	974',0,32,-1,'2019-08-17','23:27:12',-1,NULL,NULL,-1,'2019-08-17 00:00:00','',4),(11122,87794,2,45,'شحن رصيد او تسديد فواتير      _ No_Credit',0,97,-1,'2019-08-31','13:08:35',97,'2019-08-31','13:08:37',-1,'2019-08-31 00:00:00','',4),(9806,20592,2,38,'اعادة تشغيل الراوتر بعد الدفع',0,97,-1,'2019-08-24','10:53:49',97,'2019-08-24','10:54:10',97,'2019-08-24 00:00:00','',4),(10130,3162,2,45,'شحن رصيد او تسديد فواتير      _ .',0,88,-1,'2019-08-25','16:13:15',88,'2019-08-25','16:13:16',-1,'2019-08-25 00:00:00','',4),(3124,97471,2,31,'superlink _ عندو فواتير هون 92578350.. حكيتلو ييجي يفصل القديم حتى نبرمجلو عالرقم الجديد',4,87,-1,'2019-07-14','10:44:45',12,'2019-07-15','12:19:33',-1,'2019-07-15 00:00:00','',0),(2439,35397,5,33,'شبك مباشر _ شبك مباشر عشان البرمجة راوتر اتصالات بس يثبت اللينك برنلنا',20,78,-1,'2019-04-28','17:34:59',-1,NULL,NULL,-1,'2019-04-28 00:00:00','',4),(53,57159,5,37,'ضمن المعدل الطبيعي',7,10,-1,'2016-10-02','22:11:28',-1,NULL,NULL,-1,'2016-10-02 00:00:00','',4),(7231,77861,2,45,'شحن رصيد او تسديد فواتير	 _ No_Credit',0,97,-1,'2019-08-07','08:43:55',97,'2019-08-07','08:43:58',-1,'2019-08-07 00:00:00','',4),(9918,26930,5,41,'newline or reset _ رح يشغل جهاز ويتصل',20,30,-1,'2019-08-24','17:09:03',-1,NULL,NULL,-1,'2019-08-24 00:00:00','',4),(10924,32583,2,57,'عطل عام _ Customer Phone is in MAINTINANCE, For \'مشتركنا الكريم ، طواقمنا الفنية تقوم حالياً بفحص الشبكة لمعرفة سبب تأثر الخدمة لدى حضرتك، وفي حال وجود مشكلة سيتم متابعتها وحلها باسرع وقت. شكرا لتفهمك \', from date: 2019-08-29 16:45:58.0 to date: 2019-08-30 16:45:58.0\n',9,87,-1,'2019-08-29','18:02:57',87,'2019-08-29','18:03:02',-1,'2019-08-29 00:00:00','',3);
/*!40000 ALTER TABLE `ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket_followup`
--

DROP TABLE IF EXISTS `ticket_followup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket_followup` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ticket_followup` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `ticket_followup_desc` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `creationdate` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Followup` (`ticket_followup`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket_followup`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `ticket_followup` WRITE;
/*!40000 ALTER TABLE `ticket_followup` DISABLE KEYS */;
INSERT INTO `ticket_followup` VALUES (0,'None','None','2018-03-31'),(7,'W.L_Superlink+Paltel','White List','2016-10-09'),(9,'فولو اب1','فولو اب1','2017-08-26'),(11,'TH Superlink','قليل استعياب','2018-04-12'),(5,'Visit','طلب زيارة ','2016-09-17'),(6,'B.L_Superlink+Paltel','Black list','2016-10-09'),(12,'VIP.SuperLink.PALTEL','vip','2018-11-19'),(4,'Superlink','متابعة داخلية','2016-09-17'),(1,'FU1','Followup1','2016-09-17'),(3,'Paltel','عطل للاتصالات او مراسلة لهم','2016-09-17');
/*!40000 ALTER TABLE `ticket_followup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket_note`
--

DROP TABLE IF EXISTS `ticket_note`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket_note` (
  `ticket_note_id` int NOT NULL AUTO_INCREMENT,
  `ticket_note_details` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `ticket_creationdate` date DEFAULT NULL,
  `creationtime` time DEFAULT NULL,
  `ticket_id` int DEFAULT NULL,
  `userid` int DEFAULT NULL,
  `note_type` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT 'normal' COMMENT 'normal or visit',
  PRIMARY KEY (`ticket_note_id`),
  KEY `FK_ticket_note` (`ticket_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2001 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket_note`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `ticket_note` WRITE;
/*!40000 ALTER TABLE `ticket_note` DISABLE KEYS */;
INSERT INTO `ticket_note` VALUES (192,'شبك مباشر لمدة ساعه لديه تقطيع على الخط راوتر ال بي لينك واخر قراءة 2019-02-11 210432 وبدي اتواصل معاه على الجوال بعد ساعه','2019-02-11','21:47:44',765,28,'Normal'),(768,'ع الاغلب المشكلة من الفلتر  اخد لنك بعد الاتصال ','2019-07-27','22:45:04',5592,83,'SOLVED'),(1058,'توضيح المباشر','2019-08-03','16:39:57',6643,30,'Normal'),(836,'No_Credit','2019-07-29','12:14:17',5829,97,NULL),(1136,'رح تجيب الراوتر ع الشركه للفحص ','2019-08-04','21:25:02',6886,32,NULL),(440,'الواضح انه المشترك بلغ عن تشويش The customer already has a trouble ticket\n','2019-07-21','19:01:29',4514,88,'Paltel Followup 	'),(74,'سيتم اعادة البرمجة','2016-10-01','23:16:44',51,10,'Normal'),(960,'تمت البرمجة والخط اون-لاين','2019-07-31','17:52:58',6255,35,'SOLVED'),(367,'تم رفع عطل تقطيع','2019-07-19','20:18:20',3542,30,'Paltel Followup 	'),(1607,'سكر من طرفه-كان في عندو تشويش','2019-08-19','10:26:38',1214,87,NULL);
/*!40000 ALTER TABLE `ticket_note` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket_note_type`
--

DROP TABLE IF EXISTS `ticket_note_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket_note_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `note_type` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `note_type_desc` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `creationdate` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Note_Type` (`note_type`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket_note_type`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `ticket_note_type` WRITE;
/*!40000 ALTER TABLE `ticket_note_type` DISABLE KEYS */;
INSERT INTO `ticket_note_type` VALUES (2,'Normal','Normal Ticket Note','2016-09-17'),(3,'Paltel Followup 	','اضافة عطل للمشترك بعد المتابعة','2016-09-17'),(1,'Visting','Visiting Note','2016-09-17'),(4,'SOLVED','Done','2016-10-09');
/*!40000 ALTER TABLE `ticket_note_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket_priority`
--

DROP TABLE IF EXISTS `ticket_priority`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket_priority` (
  `ticket_priority_id` int NOT NULL AUTO_INCREMENT,
  `ticket_priority_type` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `ticket_creation_date` date DEFAULT NULL,
  PRIMARY KEY (`ticket_priority_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket_priority`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `ticket_priority` WRITE;
/*!40000 ALTER TABLE `ticket_priority` DISABLE KEYS */;
INSERT INTO `ticket_priority` VALUES (1,'Low',NULL),(3,'High',NULL),(2,'Medium',NULL),(4,'Urgent',NULL);
/*!40000 ALTER TABLE `ticket_priority` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket_status`
--

DROP TABLE IF EXISTS `ticket_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket_status` (
  `ticket_status_id` int NOT NULL AUTO_INCREMENT,
  `ticket_status_name` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `ticket_status_desc` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `creation_date` date DEFAULT NULL,
  PRIMARY KEY (`ticket_status_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket_status`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `ticket_status` WRITE;
/*!40000 ALTER TABLE `ticket_status` DISABLE KEYS */;
INSERT INTO `ticket_status` VALUES (4,'Local_Pending',NULL,NULL),(5,'New_Ticket',NULL,NULL),(1,'Assigned',NULL,NULL),(3,'Paltel_Pending',NULL,NULL),(2,'Closed',NULL,NULL);
/*!40000 ALTER TABLE `ticket_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket_transactions`
--

DROP TABLE IF EXISTS `ticket_transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket_transactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ticket_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `ticket_trans_summury` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `ticket_trans_creation_date` date DEFAULT NULL,
  `ticket_trans_creation_time` time DEFAULT NULL,
  `ticket_trans_note` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_ticket_user` (`user_id`),
  KEY `FK_ticket_transactions` (`ticket_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21870 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket_transactions`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `ticket_transactions` WRITE;
/*!40000 ALTER TABLE `ticket_transactions` DISABLE KEYS */;
INSERT INTO `ticket_transactions` VALUES (5156,3415,12,'Closing Ticket','2019-07-16','11:19:00',NULL),(16445,8710,88,'Closing Ticket','2019-08-19','12:59:39',NULL),(10845,6371,96,'Closing Ticket','2019-08-01','12:30:07',NULL),(4812,3180,28,'Closing Ticket','2019-07-14','21:56:26',NULL),(14869,0,83,'Adding New Ticket','2019-08-14','01:33:19',NULL),(2806,0,28,'Adding New Ticket','2019-02-18','23:34:41',NULL),(352,0,32,'Adding New Ticket','2018-02-19','18:31:54',NULL),(3506,2351,88,'Closing Ticket','2019-04-27','12:39:54',NULL),(16425,8686,88,'Closing Ticket','2019-08-19','12:30:26',NULL),(2284,1260,83,'Closing Ticket','2019-02-06','12:36:31',NULL);
/*!40000 ALTER TABLE `ticket_transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket_type`
--

DROP TABLE IF EXISTS `ticket_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket_type` (
  `ticket_type_id` int NOT NULL AUTO_INCREMENT,
  `ticket_type_name` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `ticket_type_desc` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `creation_date` date DEFAULT NULL,
  PRIMARY KEY (`ticket_type_id`),
  UNIQUE KEY `NewIndex1` (`ticket_type_name`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket_type`
--
-- WHERE:  true ORDER BY RAND() LIMIT 10

LOCK TABLES `ticket_type` WRITE;
/*!40000 ALTER TABLE `ticket_type` DISABLE KEYS */;
INSERT INTO `ticket_type` VALUES (62,'خدمة امان aman','تقديم خدمة او خلل بالخدمة','2019-08-03'),(31,'Superlink','superlink','2016-07-11'),(60,'اتصال من نفس الرقم',' سواء للتاكد من الحرارة او التفعيل او للمتابعة','2019-07-14'),(51,'Faulty Modem','router is broken','2018-03-27'),(52,'FUP','سياسة استخدام عادل','2018-03-27'),(47,'تشويش noise','ابلاغ 199','2018-03-04'),(41,'ROUTER CONFIG','newline or reset','2016-10-10'),(58,'internal خلل داخلي','شبكة داخلية وتمديدات','2019-03-24'),(38,'OTHER','استفسارات عامة','2016-09-17'),(61,'fixed ip تثبيت ايبي','تقديم طلب او خلل بالايبي','2019-08-03');
/*!40000 ALTER TABLE `ticket_type` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-21  8:19:22
