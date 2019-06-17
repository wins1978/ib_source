CREATE TABLE `basic_contract_random_name` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT '',
  `name` VARCHAR(5) DEFAULT NULL COMMENT '',
  `last_update_date` DATETIME DEFAULT NULL COMMENT '',
  PRIMARY KEY (`id`),
  INDEX `basic_contract_random_name_idx1` (`last_update_date`)
) ENGINE=INNODB; 