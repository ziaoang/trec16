DROP TABLE IF EXISTS `raw`;
CREATE TABLE `raw` (
    `id`            int(11)     NOT NULL AUTO_INCREMENT,
    `json`          text        NOT NULL,
    `is_process`    int(11)     NOT NULL DEFAULT 0,
    `lastupdate`    timestamp   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
