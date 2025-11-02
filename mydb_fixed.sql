-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `bed_applications`
--

DROP TABLE IF EXISTS `bed_applications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bed_applications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `student_name` varchar(100) NOT NULL,
  `student_id` varchar(50) DEFAULT NULL,
  `contact` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `status` enum('Pending','Approved','Rejected') DEFAULT 'Pending',
  `applied_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `reviewed_date` datetime DEFAULT NULL,
  `bed_no` int DEFAULT NULL,
  `notes` text,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`),
  KEY `idx_applied_date` (`applied_date`),
  CONSTRAINT `bed_applications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bed_applications`
--

LOCK TABLES `bed_applications` WRITE;
/*!40000 ALTER TABLE `bed_applications` DISABLE KEYS */;
INSERT INTO `bed_applications` VALUES (1,2,'suraj',NULL,NULL,'surajbdr218318@gmail.com','Approved','2025-10-31 23:37:52','2025-10-31 23:38:40',2,NULL),(2,3,'adithya','305',NULL,'bhuvaneshadithya294@gmail.com','Approved','2025-10-31 23:41:40','2025-10-31 23:42:21',3,NULL);
/*!40000 ALTER TABLE `bed_applications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `beds`
--

DROP TABLE IF EXISTS `beds`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `beds` (
  `BedNo` int NOT NULL,
  PRIMARY KEY (`BedNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `beds`
--

LOCK TABLES `beds` WRITE;
/*!40000 ALTER TABLE `beds` DISABLE KEYS */;
INSERT INTO `beds` VALUES (1),(2),(3),(4),(5);
/*!40000 ALTER TABLE `beds` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hostel`
--

DROP TABLE IF EXISTS `hostel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hostel` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) DEFAULT NULL,
  `StudentID` varchar(50) DEFAULT NULL,
  `Contact` varchar(20) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `CheckInDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `PaymentStatus` enum('Paid','Pending') DEFAULT 'Pending',
  `user_id` int DEFAULT NULL,
  `BedNo` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `BedNo` (`BedNo`),
  KEY `fk_hostel_user` (`user_id`),
  CONSTRAINT `fk_hostel_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hostel`
--

LOCK TABLES `hostel` WRITE;
/*!40000 ALTER TABLE `hostel` DISABLE KEYS */;
INSERT INTO `hostel` VALUES (4,'Aditya mc','305','9874563210',NULL,'2025-10-31 23:24:27','Paid',NULL,1),(5,'suraj',NULL,NULL,'surajbdr218318@gmail.com','2025-10-31 23:38:40','Pending',2,2),(6,'adithya','305',NULL,'bhuvaneshadithya294@gmail.com','2025-10-31 23:42:21','Pending',3,3);
/*!40000 ALTER TABLE `hostel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','user') DEFAULT 'user',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_username` (`username`),
  KEY `idx_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','admin@hostel.com','scrypt:32768:8:1$jRmeYL1RTlUjzWXh$328f9e4e74e8a097f5125cb00842016a657c6cda38338adb7fb696401de9ada07a3d544ded654a1b7d2018a5ba99cae24a81c97a2cbeca6a027ecad0df66a0f6','admin','2025-10-31 23:20:51'),(2,'surajbenur','surajbdr218318@gmail.com','scrypt:32768:8:1$9twhbFTxnUoDpdAR$84bdc8ecc814522cb0d7e7c77d1595998b70da6476d7769f1d047ec890fc9b57dc6064a85ac5626c3bc7d5c1a7d24d24cf017fdb41707a1313cdcd5570294a33','user','2025-10-31 23:26:06'),(3,'aditya','bhuvaneshadithya294@gmail.com','scrypt:32768:8:1$TKCMfnlgLG6wgDWt$ca9ec8b1730f4aba4667a6b965a10818b2f79e6322eabe06bbe7068191791e12cd76ccb541ece70895d1510cdea413a0bc74772de7a1abd5266f1694923808a9','user','2025-10-31 23:40:36');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-02 21:33:26
