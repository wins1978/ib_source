CREATE TABLE `historical_data_byday` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT '',
  `symbol` VARCHAR(64) DEFAULT NULL COMMENT '',
  `req_id` INT(10) DEFAULT NULL COMMENT '',
  `stock_time` DATETIME DEFAULT NULL COMMENT '',
  `stock_time_str` VARCHAR(20) DEFAULT NULL COMMENT '',
  `open_pri` DOUBLE(10,2) DEFAULT NULL COMMENT '',
  `high_pri` DOUBLE(10,2) DEFAULT NULL COMMENT '',
  `low_pri` DOUBLE(10,2) DEFAULT NULL COMMENT '',
  `close_pri` DOUBLE(10,2) DEFAULT NULL COMMENT '',
  `import_time` DATETIME DEFAULT NULL COMMENT '',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `historical_data_byday_idx1` (`symbol`,`stock_time_str`),
  INDEX `historical_data_byday_idx2` (`stock_time`)
) ENGINE=INNODB; 