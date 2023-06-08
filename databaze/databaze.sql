-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: game
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `abilities`
--

DROP TABLE IF EXISTS `abilities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `abilities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nazev` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `hp` int NOT NULL,
  `atk` int NOT NULL,
  `speed` int NOT NULL,
  `damage` int NOT NULL,
  `effect` tinyint(1) NOT NULL,
  `rounds_of_effect` int NOT NULL,
  `mana_cost` int NOT NULL,
  `code` varchar(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `abilities`
--

LOCK TABLES `abilities` WRITE;
/*!40000 ALTER TABLE `abilities` DISABLE KEYS */;
INSERT INTO `abilities` VALUES (1,'ohnivá koule',0,0,0,35,0,0,30,'A001');
/*!40000 ALTER TABLE `abilities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `building`
--

DROP TABLE IF EXISTS `building`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `building` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nazev` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `id_lokace` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_building_lokace` (`id_lokace`),
  CONSTRAINT `fk_building_lokace` FOREIGN KEY (`id_lokace`) REFERENCES `lokace` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `building`
--

LOCK TABLES `building` WRITE;
/*!40000 ALTER TABLE `building` DISABLE KEYS */;
INSERT INTO `building` VALUES (1,'hospoda',1),(2,'hospoda',5);
/*!40000 ALTER TABLE `building` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class`
--

DROP TABLE IF EXISTS `class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nazev` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `hp` int NOT NULL,
  `atk` int NOT NULL,
  `speed` int NOT NULL,
  `mana` int NOT NULL,
  `info` varchar(1000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT 'O této třídě nejsou informace',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_class_nazev` (`nazev`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class`
--

LOCK TABLES `class` WRITE;
/*!40000 ALTER TABLE `class` DISABLE KEYS */;
INSERT INTO `class` VALUES (1,'knight',150,80,50,50,'O této třídě nejsou informace'),(2,'assasin',80,120,100,60,'O této třídě nejsou informace'),(3,'mage',100,100,80,100,'O této třídě nejsou informace');
/*!40000 ALTER TABLE `class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item`
--

DROP TABLE IF EXISTS `item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `item` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nazev` varchar(500) NOT NULL,
  `id_typu` int NOT NULL,
  `player_hp` int NOT NULL,
  `player_damage` int NOT NULL,
  `player_mana` int NOT NULL,
  `player_speed` int NOT NULL,
  `ability_info` varchar(1000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `kod` varchar(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `kod` (`kod`),
  KEY `fk_item_typ` (`id_typu`),
  CONSTRAINT `fk_item_typ` FOREIGN KEY (`id_typu`) REFERENCES `item_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item`
--

LOCK TABLES `item` WRITE;
/*!40000 ALTER TABLE `item` DISABLE KEYS */;
INSERT INTO `item` VALUES (1,'bronzový meč',1,0,12,0,-10,NULL,'0001'),(2,'zlatý meč',1,0,20,0,-15,NULL,'0002'),(3,'diamantový meč',1,0,30,0,-25,NULL,'0003'),(4,'kouzelný proutek',1,0,15,30,0,'každé kouzlo stojí o 10 many méně','0004'),(5,'kouzelnická hůl',1,0,50,45,-10,'	každé kouzlo stojí o 5 many méně a přidá 10 poškození','0005'),(6,'zlatá přilba',2,15,0,0,-2,NULL,'0006'),(7,'kožené boty',4,0,0,0,5,NULL,'0007'),(8,'hermesovy boty',4,0,0,0,50,NULL,'0008'),(9,'léčivý lektvar',5,20,0,0,0,NULL,'0009'),(10,'mana lektvar',5,0,0,30,0,NULL,'0010'),(11,'energy drink',6,0,0,0,10,'efekt trvá po dobu 3 kol','0011'),(12,'kouzelnický klobouk',2,20,5,10,-5,NULL,'0012'),(13,'pivo',5,50,0,0,0,NULL,'0013'),(14,'ohnivá koule svitek',7,0,0,0,0,'získáte schopnost \"ohnivá koule\"','0014');
/*!40000 ALTER TABLE `item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item_type`
--

DROP TABLE IF EXISTS `item_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `item_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nazev` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nazev` (`nazev`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item_type`
--

LOCK TABLES `item_type` WRITE;
/*!40000 ALTER TABLE `item_type` DISABLE KEYS */;
INSERT INTO `item_type` VALUES (4,'boty'),(6,'combat_useable'),(7,'non_combat_useable'),(3,'oblek'),(2,'přilba'),(5,'useable'),(1,'zbraň');
/*!40000 ALTER TABLE `item_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lokace`
--

DROP TABLE IF EXISTS `lokace`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lokace` (
  `id` int NOT NULL AUTO_INCREMENT,
  `kod` int NOT NULL,
  `nazev` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_kod` (`kod`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lokace`
--

LOCK TABLES `lokace` WRITE;
/*!40000 ALTER TABLE `lokace` DISABLE KEYS */;
INSERT INTO `lokace` VALUES (1,1,'Hlavní město'),(2,2,'Route1'),(3,3,'Route2'),(4,4,'Les života'),(5,5,'Rubínové město');
/*!40000 ALTER TABLE `lokace` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `missions_completed`
--

DROP TABLE IF EXISTS `missions_completed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `missions_completed` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_playera` int NOT NULL,
  `id_questu` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UC_mc` (`id_playera`,`id_questu`),
  KEY `fk_mc_quests` (`id_questu`),
  CONSTRAINT `fk_mc_player` FOREIGN KEY (`id_playera`) REFERENCES `player` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_mc_quests` FOREIGN KEY (`id_questu`) REFERENCES `quests` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `missions_completed`
--

LOCK TABLES `missions_completed` WRITE;
/*!40000 ALTER TABLE `missions_completed` DISABLE KEYS */;
/*!40000 ALTER TABLE `missions_completed` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `own_ability`
--

DROP TABLE IF EXISTS `own_ability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `own_ability` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_playera` int NOT NULL,
  `id_ability` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_oa_player` (`id_playera`),
  KEY `fk_oa_abilities` (`id_ability`),
  CONSTRAINT `fk_oa_abilities` FOREIGN KEY (`id_ability`) REFERENCES `abilities` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_oa_player` FOREIGN KEY (`id_playera`) REFERENCES `player` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `own_ability`
--

LOCK TABLES `own_ability` WRITE;
/*!40000 ALTER TABLE `own_ability` DISABLE KEYS */;
/*!40000 ALTER TABLE `own_ability` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `own_item`
--

DROP TABLE IF EXISTS `own_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `own_item` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_itemu` int NOT NULL,
  `id_playera` int NOT NULL,
  `is_using` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_own_item` (`id_itemu`),
  KEY `fk_own_player` (`id_playera`),
  CONSTRAINT `fk_own_item` FOREIGN KEY (`id_itemu`) REFERENCES `item` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_own_player` FOREIGN KEY (`id_playera`) REFERENCES `player` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `own_item`
--

LOCK TABLES `own_item` WRITE;
/*!40000 ALTER TABLE `own_item` DISABLE KEYS */;
/*!40000 ALTER TABLE `own_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `player`
--

DROP TABLE IF EXISTS `player`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `passwd` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `add_hp` int NOT NULL DEFAULT '0',
  `add_atk` int NOT NULL DEFAULT '0',
  `add_speed` int NOT NULL DEFAULT '0',
  `add_mana` int NOT NULL DEFAULT '0',
  `coins` int NOT NULL DEFAULT '0',
  `building` int DEFAULT NULL,
  `is_online` bit(1) NOT NULL DEFAULT b'0',
  `id_class` int NOT NULL,
  `id_lokace` int NOT NULL,
  `id_building` int DEFAULT NULL,
  `current_hp` int NOT NULL,
  `current_mana` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `FK_player_building` (`id_building`),
  KEY `fk_player_class` (`id_class`),
  KEY `fk_player_lokace` (`id_lokace`),
  CONSTRAINT `FK_player_building` FOREIGN KEY (`id_building`) REFERENCES `building` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_player_class` FOREIGN KEY (`id_class`) REFERENCES `class` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_player_lokace` FOREIGN KEY (`id_lokace`) REFERENCES `lokace` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `player`
--

LOCK TABLES `player` WRITE;
/*!40000 ALTER TABLE `player` DISABLE KEYS */;
INSERT INTO `player` VALUES (13,'michal','56b1db8133d9eb398aabd376f07bf8ab5fc584ea0b8bd6a1770200cb613ca005',0,0,0,0,0,NULL,_binary '\0',3,1,NULL,100,100);
/*!40000 ALTER TABLE `player` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quests`
--

DROP TABLE IF EXISTS `quests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nazev` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `kod` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nazev` (`nazev`),
  UNIQUE KEY `kod` (`kod`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quests`
--

LOCK TABLES `quests` WRITE;
/*!40000 ALTER TABLE `quests` DISABLE KEYS */;
INSERT INTO `quests` VALUES (1,'Capital city tawer quest',1);
/*!40000 ALTER TABLE `quests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'game'
--

--
-- Dumping routines for database 'game'
--
/*!50003 DROP PROCEDURE IF EXISTS `mp_register` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `mp_register`(
    IN p_username NVARCHAR(250),
    IN p_passwd NVARCHAR(250),
    IN p_class NVARCHAR(250)
)
BEGIN
    -- pokud existuje, vyhodíme chybu
    IF EXISTS (SELECT * FROM player WHERE username = p_username) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Hráč s tímto uživatelským jménem již existuje';
    END IF;
    
    SET @lokace_id = (SELECT id FROM lokace WHERE nazev = 'Hlavní město');
    SET @current_hp = (SELECT hp FROM class WHERE nazev = p_class LIMIT 1);
    SET @current_mana = (SELECT mana FROM class WHERE nazev = p_class LIMIT 1);

    -- jinak vytvoříme nový záznam pro hráče
    INSERT INTO player (username, passwd, id_class,id_lokace,current_hp,current_mana) VALUES (p_username, p_passwd, (SELECT id FROM class WHERE nazev = p_class LIMIT 1),@lokace_id,@current_hp,@current_mana);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-08 23:56:45
