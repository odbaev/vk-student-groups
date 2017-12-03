-- MySQL dump 10.13  Distrib 5.7.12, for Win64 (x86_64)
--
-- Host: localhost    Database: vk17
-- ------------------------------------------------------
-- Server version	5.7.17

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
-- Dumping data for table `alcohol`
--

LOCK TABLES `alcohol` WRITE;
/*!40000 ALTER TABLE `alcohol` DISABLE KEYS */;
INSERT INTO `alcohol` VALUES (1,'резко негативное'),(2,'негативное'),(3,'компромиссное'),(4,'нейтральное'),(5,'положительное');
/*!40000 ALTER TABLE `alcohol` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `education`
--

LOCK TABLES `education` WRITE;
/*!40000 ALTER TABLE `education` DISABLE KEYS */;
INSERT INTO `education` VALUES (1,'общее'),(2,'профессиональное'),(3,'высшее');
/*!40000 ALTER TABLE `education` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `life_main`
--

LOCK TABLES `life_main` WRITE;
/*!40000 ALTER TABLE `life_main` DISABLE KEYS */;
INSERT INTO `life_main` VALUES (1,'семья и дети'),(2,'карьера и деньги'),(3,'развлечения и отдых'),(4,'наука и исследования'),(5,'совершенствование мира'),(6,'саморазвитие'),(7,'красота и искусство'),(8,'слава и влияние');
/*!40000 ALTER TABLE `life_main` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `occupation`
--

LOCK TABLES `occupation` WRITE;
/*!40000 ALTER TABLE `occupation` DISABLE KEYS */;
INSERT INTO `occupation` VALUES (1,'school'),(2,'university'),(3,'work');
/*!40000 ALTER TABLE `occupation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `people_main`
--

LOCK TABLES `people_main` WRITE;
/*!40000 ALTER TABLE `people_main` DISABLE KEYS */;
INSERT INTO `people_main` VALUES (1,'ум и креативность'),(2,'доброта и честность'),(3,'красота и здоровье'),(4,'власть и богатство'),(5,'смелость и упорство'),(6,'юмор и жизнелюбие');
/*!40000 ALTER TABLE `people_main` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `political`
--

LOCK TABLES `political` WRITE;
/*!40000 ALTER TABLE `political` DISABLE KEYS */;
INSERT INTO `political` VALUES (1,'коммунистические'),(2,'социалистические'),(3,'умеренные'),(4,'либеральные'),(5,'консервативные'),(6,'монархические'),(7,'ультраконсервативные'),(8,'индифферентные'),(9,'либертарианские');
/*!40000 ALTER TABLE `political` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `relation`
--

LOCK TABLES `relation` WRITE;
/*!40000 ALTER TABLE `relation` DISABLE KEYS */;
INSERT INTO `relation` VALUES (1,'не женат/не замужем'),(2,'есть друг/есть подруга'),(3,'помолвлен/помолвлен'),(4,'женат/замужем'),(5,'всё сложно'),(6,'в активном поиске'),(7,'влюблён/влюблена'),(8,'в гражданском браке');
/*!40000 ALTER TABLE `relation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `religion`
--

LOCK TABLES `religion` WRITE;
/*!40000 ALTER TABLE `religion` DISABLE KEYS */;
INSERT INTO `religion` VALUES (1,'Иудаизм'),(2,'Православие'),(3,'Католицизм'),(4,'Протестантизм'),(5,'Ислам'),(6,'Буддизм'),(7,'Конфуцианство'),(8,'Светский гуманизм'),(9,'Пастафарианство');
/*!40000 ALTER TABLE `religion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `school_types`
--

LOCK TABLES `school_types` WRITE;
/*!40000 ALTER TABLE `school_types` DISABLE KEYS */;
INSERT INTO `school_types` VALUES (0,'школа'),(1,'гимназия'),(2,'лицей'),(3,'школа-интернат'),(4,'школа вечерняя'),(5,'школа музыкальная'),(6,'школа спортивная'),(7,'школа художественная'),(8,'колледж'),(9,'профессиональный лицей'),(10,'техникум'),(11,'ПТУ'),(12,'училище'),(13,'школа искусств');
/*!40000 ALTER TABLE `school_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `sex`
--

LOCK TABLES `sex` WRITE;
/*!40000 ALTER TABLE `sex` DISABLE KEYS */;
INSERT INTO `sex` VALUES (1,'женский'),(2,'мужской');
/*!40000 ALTER TABLE `sex` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `smoking`
--

LOCK TABLES `smoking` WRITE;
/*!40000 ALTER TABLE `smoking` DISABLE KEYS */;
INSERT INTO `smoking` VALUES (1,'резко негативное'),(2,'негативное'),(3,'компромиссное'),(4,'нейтральное'),(5,'положительное');
/*!40000 ALTER TABLE `smoking` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-11-25 21:06:28
