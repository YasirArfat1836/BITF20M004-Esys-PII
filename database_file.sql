-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
SHOW WARNINGS;
-- -----------------------------------------------------
-- Schema student_interest_system
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `student_interest_system` ;

-- -----------------------------------------------------
-- Schema student_interest_system
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `student_interest_system` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
SHOW WARNINGS;
USE `student_interest_system` ;

-- -----------------------------------------------------
-- Table `student_interest_system`.`student_interests`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `student_interest_system`.`student_interests` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `student_interest_system`.`student_interests` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `full_name` VARCHAR(255) NOT NULL,
  `roll_number` VARCHAR(20) NOT NULL,
  `email_address` VARCHAR(255) NOT NULL,
  `gender` VARCHAR(10) NULL DEFAULT NULL,
  `date_of_birth` DATE NULL DEFAULT NULL,
  `city` VARCHAR(100) NULL DEFAULT NULL,
  `interest` VARCHAR(255) NULL DEFAULT NULL,
  `department` VARCHAR(100) NULL DEFAULT NULL,
  `degree_title` VARCHAR(100) NULL DEFAULT NULL,
  `subject` VARCHAR(100) NULL DEFAULT NULL,
  `start_date` DATE NULL DEFAULT NULL,
  `end_date` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 15
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `student_interest_system`.`user_activity_log`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `student_interest_system`.`user_activity_log` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `student_interest_system`.`user_activity_log` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NULL DEFAULT NULL,
  `activity_type` VARCHAR(255) NULL DEFAULT NULL,
  `timestamp` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

SHOW WARNINGS;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
