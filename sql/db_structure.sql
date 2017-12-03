CREATE DATABASE  IF NOT EXISTS `vk17` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `vk17`;
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
-- Table structure for table `alcohol`
--

DROP TABLE IF EXISTS `alcohol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alcohol` (
  `alcohol_id` tinyint(4) NOT NULL,
  `alcohol_type` varchar(45) NOT NULL,
  PRIMARY KEY (`alcohol_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cities`
--

DROP TABLE IF EXISTS `cities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cities` (
  `city_id` int(11) NOT NULL,
  `city_title` varchar(65) NOT NULL,
  `region_id` int(11) DEFAULT NULL,
  `country_id` int(11) NOT NULL,
  `area` varchar(65) DEFAULT NULL,
  PRIMARY KEY (`city_id`),
  KEY `fk_cities_region_idx` (`region_id`),
  KEY `fk_cities_country_idx` (`country_id`),
  CONSTRAINT `fk_cities_country` FOREIGN KEY (`country_id`) REFERENCES `countries` (`country_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_cities_region` FOREIGN KEY (`region_id`) REFERENCES `regions` (`region_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `countries`
--

DROP TABLE IF EXISTS `countries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `countries` (
  `country_id` int(11) NOT NULL,
  `country_title` varchar(45) NOT NULL,
  PRIMARY KEY (`country_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `education`
--

DROP TABLE IF EXISTS `education`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `education` (
  `education_id` tinyint(4) NOT NULL,
  `education_type` varchar(45) NOT NULL,
  PRIMARY KEY (`education_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `life_main`
--

DROP TABLE IF EXISTS `life_main`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `life_main` (
  `life_main_id` tinyint(4) NOT NULL,
  `life_main_type` varchar(45) NOT NULL,
  PRIMARY KEY (`life_main_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `occupation`
--

DROP TABLE IF EXISTS `occupation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `occupation` (
  `occupation_id` tinyint(4) NOT NULL,
  `occupation_type` varchar(45) NOT NULL,
  PRIMARY KEY (`occupation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `people_main`
--

DROP TABLE IF EXISTS `people_main`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people_main` (
  `people_main_id` tinyint(4) NOT NULL,
  `people_main_type` varchar(45) NOT NULL,
  PRIMARY KEY (`people_main_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `political`
--

DROP TABLE IF EXISTS `political`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `political` (
  `political_id` tinyint(4) NOT NULL,
  `political_type` varchar(45) NOT NULL,
  PRIMARY KEY (`political_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `regions`
--

DROP TABLE IF EXISTS `regions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `regions` (
  `region_id` int(11) NOT NULL,
  `region_title` varchar(65) NOT NULL,
  `country_id` int(11) NOT NULL,
  PRIMARY KEY (`region_id`),
  KEY `fk_regions_country_idx` (`country_id`),
  CONSTRAINT `fk_regions_country` FOREIGN KEY (`country_id`) REFERENCES `countries` (`country_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `relation`
--

DROP TABLE IF EXISTS `relation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `relation` (
  `relation_id` tinyint(4) NOT NULL,
  `relation_type` varchar(45) NOT NULL,
  PRIMARY KEY (`relation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `religion`
--

DROP TABLE IF EXISTS `religion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `religion` (
  `religion_id` tinyint(4) NOT NULL,
  `religion_type` varchar(45) NOT NULL,
  PRIMARY KEY (`religion_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `school_students`
--

DROP TABLE IF EXISTS `school_students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_students` (
  `student_id` int(11) NOT NULL,
  PRIMARY KEY (`student_id`),
  CONSTRAINT `fk_school_students_student` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `school_types`
--

DROP TABLE IF EXISTS `school_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_types` (
  `school_type` tinyint(4) NOT NULL,
  `school_type_str` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`school_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sex`
--

DROP TABLE IF EXISTS `sex`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sex` (
  `sex_id` tinyint(3) NOT NULL,
  `sex_type` varchar(45) NOT NULL,
  PRIMARY KEY (`sex_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `smoking`
--

DROP TABLE IF EXISTS `smoking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smoking` (
  `smoking_id` tinyint(4) NOT NULL,
  `smoking_type` varchar(45) NOT NULL,
  PRIMARY KEY (`smoking_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `university_students`
--

DROP TABLE IF EXISTS `university_students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `university_students` (
  `student_id` int(11) NOT NULL,
  PRIMARY KEY (`student_id`),
  CONSTRAINT `fk_university_students_student` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `photo` varchar(255) DEFAULT NULL,
  `sex` tinyint(4) DEFAULT NULL,
  `age` tinyint(3) unsigned DEFAULT NULL,
  `country` int(11) DEFAULT NULL,
  `city` int(11) DEFAULT NULL,
  `relation` tinyint(4) DEFAULT NULL,
  `child` bit(1) DEFAULT NULL,
  `occupation` tinyint(4) DEFAULT NULL,
  `education` tinyint(4) DEFAULT NULL,
  `school_id` int(11) DEFAULT NULL,
  `school_class` varchar(5) DEFAULT NULL,
  `school_type` tinyint(4) DEFAULT NULL,
  `school_city` int(11) DEFAULT NULL,
  `school_grad_year` smallint(4) unsigned DEFAULT NULL,
  `school_grad_age` tinyint(3) unsigned DEFAULT NULL,
  `university_id` int(11) DEFAULT NULL,
  `university_faculty` int(11) DEFAULT NULL,
  `university_chair` int(11) DEFAULT NULL,
  `university_city` int(11) DEFAULT NULL,
  `university_grad_year` smallint(4) unsigned DEFAULT NULL,
  `university_grad_age` tinyint(3) unsigned DEFAULT NULL,
  `first_job_company` varchar(100) DEFAULT NULL,
  `first_job_position` varchar(100) DEFAULT NULL,
  `first_job_city` int(11) DEFAULT NULL,
  `first_job_age` tinyint(3) unsigned DEFAULT NULL,
  `cur_job_company` varchar(100) DEFAULT NULL,
  `cur_job_position` varchar(100) DEFAULT NULL,
  `cur_job_city` int(11) DEFAULT NULL,
  `cur_job_age` tinyint(3) unsigned DEFAULT NULL,
  `religion` tinyint(4) DEFAULT NULL,
  `political` tinyint(4) DEFAULT NULL,
  `life_main` tinyint(4) DEFAULT NULL,
  `people_main` tinyint(4) DEFAULT NULL,
  `smoking` tinyint(4) DEFAULT NULL,
  `alcohol` tinyint(4) DEFAULT NULL,
  `music` text,
  `movies` text,
  `books` text,
  `games` text,
  `last_seen` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_users_sex_idx` (`sex`),
  KEY `fk_users_country_idx` (`country`),
  KEY `fk_users_city_idx` (`city`),
  KEY `fk_users_relation_idx` (`relation`),
  KEY `fk_users_occupation_idx` (`occupation`),
  KEY `fk_users_education_idx` (`education`),
  KEY `fk_users_school_city_idx` (`school_city`),
  KEY `fk_users_university_city_idx` (`university_city`),
  KEY `fk_users_first_job_city_idx` (`first_job_city`),
  KEY `fk_users_cur_job_city_idx` (`cur_job_city`),
  KEY `fk_users_religion_idx` (`religion`),
  KEY `fk_users_political_idx` (`political`),
  KEY `fk_users_life_main_idx` (`life_main`),
  KEY `fk_users_people_main_idx` (`people_main`),
  KEY `fk_users_smoking_idx` (`smoking`),
  KEY `fk_users_alcohol_idx` (`alcohol`),
  KEY `fk_users_school_type_idx` (`school_type`),
  CONSTRAINT `fk_users_alcohol` FOREIGN KEY (`alcohol`) REFERENCES `alcohol` (`alcohol_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_city` FOREIGN KEY (`city`) REFERENCES `cities` (`city_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_country` FOREIGN KEY (`country`) REFERENCES `countries` (`country_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_cur_job_city` FOREIGN KEY (`cur_job_city`) REFERENCES `cities` (`city_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_education` FOREIGN KEY (`education`) REFERENCES `education` (`education_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_first_job_city` FOREIGN KEY (`first_job_city`) REFERENCES `cities` (`city_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_life_main` FOREIGN KEY (`life_main`) REFERENCES `life_main` (`life_main_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_occupation` FOREIGN KEY (`occupation`) REFERENCES `occupation` (`occupation_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_people_main` FOREIGN KEY (`people_main`) REFERENCES `people_main` (`people_main_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_political` FOREIGN KEY (`political`) REFERENCES `political` (`political_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_relation` FOREIGN KEY (`relation`) REFERENCES `relation` (`relation_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_religion` FOREIGN KEY (`religion`) REFERENCES `religion` (`religion_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_school_city` FOREIGN KEY (`school_city`) REFERENCES `cities` (`city_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_school_type` FOREIGN KEY (`school_type`) REFERENCES `school_types` (`school_type`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_sex` FOREIGN KEY (`sex`) REFERENCES `sex` (`sex_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_smoking` FOREIGN KEY (`smoking`) REFERENCES `smoking` (`smoking_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_university_city` FOREIGN KEY (`university_city`) REFERENCES `cities` (`city_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-11-25 20:59:35
