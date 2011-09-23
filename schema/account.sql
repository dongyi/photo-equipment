CREATE TABLE `account` (
    `userid` int(11) NOT NULL auto_increment,
    `email` text character set utf8 NOT NULL,
    `username` varchar(32) NOT NULL,
    `weiboid` bigint(20) default NULL,
    `renrenid` bigint(20) default NULL,
    `doubanid` bigint(20) default NULL,
    `lastlogin` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
    PRIMARY KEY  (`userid`,`email`(255)))
ENGINE=MyISAM DEFAULT CHARSET=utf8
