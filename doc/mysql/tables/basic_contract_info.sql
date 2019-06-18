CREATE TABLE `basic_contract_info` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT '',
  `symbol` VARCHAR(64) DEFAULT NULL COMMENT '',
  `sec_type` VARCHAR(20) DEFAULT NULL COMMENT '',
  `currency` VARCHAR(10) DEFAULT NULL COMMENT '',
  `exchange` VARCHAR(30) DEFAULT NULL COMMENT '',
  `primary_exchange` VARCHAR(200) DEFAULT NULL COMMENT '',
  `last_byday_import_date` DATETIME DEFAULT NULL COMMENT '',
  `disabled` VARCHAR(5) DEFAULT 'N' COMMENT 'Y/N',
  `publish_time` DATETIME DEFAULT NULL COMMENT 'new stock day',
  `create_time` DATETIME DEFAULT NULL COMMENT '',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `basic_contract_info_idx1` (`symbol`)
) ENGINE=INNODB; 