DROP TABLE IF EXISTS `submit`;
CREATE TABLE `submit` (
    `id`            int(11)         NOT NULL AUTO_INCREMENT,
    `qid`           varchar(255)    NOT NULL,
    `tid`           varchar(255)    NOT NULL,
    `client_id`     varchar(255)    NOT NULL,
    `is_process`    int(11)         NOT NULL DEFAULT 0,
    `lastupdate`    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
