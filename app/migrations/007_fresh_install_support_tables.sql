-- Required empty support tables for fresh native installations.
CREATE TABLE IF NOT EXISTS `aircraft_manual_registry` (
  `registration` varchar(10) NOT NULL,
  `hexcode` varchar(10) DEFAULT NULL,
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
  `monthmanu` int(11) DEFAULT NULL,
  `icaotypedesig` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

CREATE TABLE IF NOT EXISTS `disclaimer_acceptance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `disclaimer_version` varchar(10) NOT NULL,
  `accepted_at` datetime NOT NULL,
  `expires_at` datetime NOT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_version_expires` (`disclaimer_version`, `expires_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
