/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.4.9-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: airtrack
-- ------------------------------------------------------
-- Server version	11.4.9-MariaDB-ubu2404

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `aircraft`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `aircraft` (
  `AircraftID` int(11) NOT NULL AUTO_INCREMENT,
  `AirlineID` int(11) DEFAULT NULL,
  `FlightNumber` varchar(255) DEFAULT NULL,
  `Registration` varchar(255) DEFAULT NULL,
  `Aircraft_Type` varchar(255) DEFAULT NULL,
  `MSN` varchar(100) DEFAULT NULL,
  `Times_Seen` int(11) DEFAULT NULL,
  `Departure` varchar(255) DEFAULT NULL,
  `Arrival` varchar(255) DEFAULT NULL,
  `Country_of_Reg` varchar(255) DEFAULT NULL,
  `Country_Flag` varchar(255) DEFAULT NULL,
  `Aircraft_Image` varchar(255) DEFAULT NULL,
  `Notes` text DEFAULT NULL,
  `Age` int(11) DEFAULT NULL,
  `First_Sighted` datetime DEFAULT NULL,
  `Sightings` int(11) DEFAULT 1,
  `Timestamp` datetime DEFAULT current_timestamp(),
  `Manufacture_Year` year(4) DEFAULT NULL,
  `Manufacture_Month` tinyint(4) DEFAULT NULL,
  `Category` varchar(100) DEFAULT NULL,
  `Engine_Type` varchar(50) DEFAULT NULL,
  `Orphaned` tinyint(4) DEFAULT 0,
  `Aircraft_Updated` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Spotted_At` varchar(255) DEFAULT NULL,
  `ICAO_Address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`AircraftID`),
  KEY `AirlineID` (`AirlineID`),
  CONSTRAINT `aircraft_ibfk_1` FOREIGN KEY (`AirlineID`) REFERENCES `airlines` (`AirlineID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=910 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `airlines`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `airlines` (
  `AirlineID` int(11) NOT NULL AUTO_INCREMENT,
  `AirlineName` varchar(255) NOT NULL,
  `Last_Updated` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Logo` varchar(255) DEFAULT NULL,
  `Country` varchar(100) DEFAULT NULL,
  `IATA` varchar(10) DEFAULT NULL,
  `ICAO` varchar(10) DEFAULT NULL,
  `Callsign` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`AirlineID`),
  UNIQUE KEY `AirlineName` (`AirlineName`)
) ENGINE=InnoDB AUTO_INCREMENT=336 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `airports`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `airports` (
  `ICAO` varchar(10) NOT NULL,
  `IATA` varchar(3) DEFAULT NULL,
  `AirportName` varchar(255) NOT NULL,
  `Country` varchar(50) NOT NULL,
  `id` int(11) NOT NULL,
  `ident` varchar(10) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `latitude_deg` decimal(10,8) DEFAULT NULL,
  `longitude_deg` decimal(11,8) DEFAULT NULL,
  `elevation_ft` int(11) DEFAULT NULL,
  `continent` varchar(2) DEFAULT NULL,
  `iso_country` varchar(2) DEFAULT NULL,
  `iso_region` varchar(10) DEFAULT NULL,
  `municipality` varchar(100) DEFAULT NULL,
  `scheduled_service` varchar(3) DEFAULT NULL,
  `gps_code` varchar(10) DEFAULT NULL,
  `local_code` varchar(10) DEFAULT NULL,
  `home_link` text DEFAULT NULL,
  `wikipedia_link` text DEFAULT NULL,
  `keywords` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_icao` (`ICAO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_settings`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `app_settings` (
  `SettingKey` varchar(100) NOT NULL,
  `SettingValue` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`SettingKey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `argentina`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `argentina` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `armenia`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `armenia` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `airline` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `audit_country_updates`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `audit_country_updates` (
  `AircraftID` int(11) NOT NULL,
  `Registration` varchar(255) DEFAULT NULL,
  `Existing_Country_of_Reg` varchar(255) DEFAULT NULL,
  `Suggested_Country_of_Reg` varchar(255) DEFAULT NULL,
  `Status` enum('Pending','Approved','Rejected') DEFAULT 'Pending',
  PRIMARY KEY (`AircraftID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `australia`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `australia` (
  `registration` varchar(10) NOT NULL,
  `aircraftmanufacturer` varchar(100) DEFAULT NULL,
  `aircraftmodel` varchar(50) DEFAULT NULL,
  `msn` varchar(50) DEFAULT NULL,
  `maxtakeoffweight` int(11) DEFAULT NULL,
  `enginecount` int(11) DEFAULT NULL,
  `enginemanufacturer` varchar(100) DEFAULT NULL,
  `enginetype` varchar(50) DEFAULT NULL,
  `enginemodel` varchar(50) DEFAULT NULL,
  `fueltype` varchar(50) DEFAULT NULL,
  `registrationtype` varchar(50) DEFAULT NULL,
  `registeredowner` varchar(150) DEFAULT NULL,
  `registeredownercountry` varchar(50) DEFAULT NULL,
  `operatorname` varchar(150) DEFAULT NULL,
  `operatorcountry` varchar(50) DEFAULT NULL,
  `firstregistrationdate` date DEFAULT NULL,
  `airframe` varchar(100) DEFAULT NULL,
  `propmanu` varchar(100) DEFAULT NULL,
  `propmodel` varchar(50) DEFAULT NULL,
  `typecert` varchar(50) DEFAULT NULL,
  `countrymanu` varchar(50) DEFAULT NULL,
  `yearmanu` int(11) DEFAULT NULL,
  `icaotypedesig` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `austria`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `austria` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bahamas`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `bahamas` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `belgium`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `belgium` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bhutan`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `bhutan` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bolivia`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `bolivia` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `brazil`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `brazil` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `canada`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `canada` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cayman_islands`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `cayman_islands` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `chile`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `chile` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `china`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `china` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `costa_rica`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `costa_rica` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `croatia`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `croatia` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cuba`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `cuba` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `customers`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `customers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `stripe_customer_id` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `country` varchar(120) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `Email` (`email`),
  UNIQUE KEY `email_2` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cyprus`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `cyprus` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `czech_republic`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `czech_republic` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `denmark`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `denmark` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egypt`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `egypt` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `estonia`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `estonia` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ethiopia`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `ethiopia` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `flights`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `flights` (
  `FlightID` int(11) NOT NULL AUTO_INCREMENT,
  `AircraftID` int(11) DEFAULT NULL,
  `AirlineID` int(11) DEFAULT NULL,
  `FlightNumber` varchar(255) DEFAULT NULL,
  `Registration` varchar(255) DEFAULT NULL,
  `MSN` varchar(50) DEFAULT NULL,
  `Aircraft_Type` varchar(255) DEFAULT NULL,
  `Times_Seen` int(11) DEFAULT NULL,
  `Departure` varchar(255) DEFAULT NULL,
  `Arrival` varchar(255) DEFAULT NULL,
  `Country_of_Reg` varchar(255) DEFAULT NULL,
  `Country_Flag` varchar(255) DEFAULT NULL,
  `Flight_Image` varchar(255) DEFAULT NULL,
  `Notes` text DEFAULT NULL,
  `Flight_Updated` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Timestamp` datetime DEFAULT current_timestamp(),
  `Spotted_At` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`FlightID`),
  KEY `AirlineID` (`AirlineID`),
  CONSTRAINT `flights_ibfk_1` FOREIGN KEY (`AirlineID`) REFERENCES `airlines` (`AirlineID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1085 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `france`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `france` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `georgia`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `georgia` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `germany`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `germany` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `greece`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `greece` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `guernsey`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `guernsey` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `hungary`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `hungary` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `iceland`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `iceland` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `indonesia`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `indonesia` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `iran`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `iran` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ireland`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `ireland` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `italy`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `italy` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `japan`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `japan` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `liberia`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `liberia` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `license_activity`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `license_activity` (
  `ActivityID` int(11) NOT NULL AUTO_INCREMENT,
  `LicenseID` int(11) NOT NULL,
  `EventType` varchar(100) NOT NULL,
  `EventDetails` text DEFAULT NULL,
  `CreatedAt` datetime DEFAULT NULL,
  PRIMARY KEY (`ActivityID`),
  KEY `LicenseID` (`LicenseID`),
  CONSTRAINT `license_activity_ibfk_1` FOREIGN KEY (`LicenseID`) REFERENCES `licenses` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `licenses`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `licenses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) NOT NULL,
  `license_type` enum('standard','professional','institutional') NOT NULL,
  `license_key` varchar(64) NOT NULL,
  `stripe_session_id` varchar(255) DEFAULT NULL,
  `stripe_payment_intent` varchar(255) DEFAULT NULL,
  `purchase_amount` decimal(10,2) DEFAULT NULL,
  `purchase_currency` varchar(10) DEFAULT 'AUD',
  `active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `expires_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `LicenseKey` (`license_key`),
  KEY `fk_license_customer` (`customer_id`),
  CONSTRAINT `fk_license_customer` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`),
  CONSTRAINT `licenses_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lithuania`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `lithuania` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `luxembourg`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `luxembourg` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `morocco`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `morocco` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `netherlands`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `netherlands` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `new_zealand`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `new_zealand` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `norway`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `norway` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pakistan`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `pakistan` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `panama`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `panama` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `poland`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `poland` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `prefixes`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `prefixes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `country` varchar(100) DEFAULT NULL,
  `last_registry_update` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `qatar`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `qatar` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `registration_prefixes`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `registration_prefixes` (
  `Reg_Prefix` varchar(10) NOT NULL,
  `Country_of_Reg` varchar(255) NOT NULL,
  PRIMARY KEY (`Reg_Prefix`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `romania`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `romania` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `russia`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `russia` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `san_marino`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `san_marino` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `saudi_arabia`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `saudi_arabia` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `settings`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `settings` (
  `id` int(11) NOT NULL DEFAULT 1,
  `show_disclaimer` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `slovakia`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `slovakia` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `south_africa`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `south_africa` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `south_korea`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `south_korea` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `spain`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `spain` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `suriname`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `suriname` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `switzerland`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `switzerland` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `thailand`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `thailand` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `turkey`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `turkey` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `united_arab_emirates`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `united_arab_emirates` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `united_kingdom`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `united_kingdom` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `united_states`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `united_states` (
  `n_number` varchar(10) DEFAULT NULL,
  `serial_number` varchar(50) DEFAULT NULL,
  `mfr_mdl_code` varchar(10) DEFAULT NULL,
  `eng_mfr_mdl` varchar(50) DEFAULT NULL,
  `year_mfr` varchar(4) DEFAULT NULL,
  `type_aircraft` varchar(2) DEFAULT NULL,
  `type_engine` varchar(2) DEFAULT NULL,
  `certification` varchar(10) DEFAULT NULL,
  `status_code` varchar(2) DEFAULT NULL,
  `mode_s_code` varchar(15) DEFAULT NULL,
  `mode_s_hex` varchar(10) DEFAULT NULL,
  `air_worth_date` varchar(10) DEFAULT NULL,
  `expiration_date` varchar(10) DEFAULT NULL,
  `unique_id` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `uruguay`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `uruguay` (
  `registration` varchar(20) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  `serial` varchar(50) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `icao_address` varchar(6) DEFAULT NULL,
  `date_of_registration` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping events for database 'airtrack'
--

--
-- Dumping routines for database 'airtrack'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-12-26  4:18:14
