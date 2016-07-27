DROP TABLE IF EXISTS `preprocess`;
CREATE TABLE `preprocess` (
    `id`            int(11)         NOT NULL AUTO_INCREMENT,
    `created_at`    varchar(255)    NOT NULL,
    `id_str`        varchar(255)    NOT NULL,
    `word_list_str` varchar(1024)   NOT NULL,
    `stem_list_str` varchar(1024)   NOT NULL,
    `is_process`    int(11)         NOT NULL DEFAULT 0,
    `lastupdate`    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
