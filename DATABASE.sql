/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.4.21-MariaDB : Database - bitcoin
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`bitcoin` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `bitcoin`;

/*Table structure for table `bitcoinreg` */

DROP TABLE IF EXISTS `bitcoinreg`;

CREATE TABLE `bitcoinreg` (
  `id` int(200) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `bitcoins` varchar(100) DEFAULT '0',
  `password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

/*Data for the table `bitcoinreg` */

insert  into `bitcoinreg`(`id`,`name`,`email`,`bitcoins`,`password`) values (1,'Mouli','mouli@gmail.com','-184','mouli'),(2,'nani','nani@gmail.com','-74','nani'),(3,'kumar','kumar@gmail.com','-15','kumar');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
