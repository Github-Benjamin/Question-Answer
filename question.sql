/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 50718
Source Host           : 127.0.0.1:3306
Source Database       : question

Target Server Type    : MYSQL
Target Server Version : 50718
File Encoding         : 65001

Created By			  : Benjamin
Date			 	  : 2017-08-17 15:43:46
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for question
-- ----------------------------
DROP TABLE IF EXISTS `question`;
CREATE DATABASE question;
USE question;
CREATE TABLE `question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `content` text,
  `fbtime` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `click` int(255) DEFAULT NULL,
  `keywords` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of question
-- ----------------------------
INSERT INTO `question` VALUES ('1', '1', '1', '2017-08-16 17:49:46', '5', 'Keyword1', 'tester1');
INSERT INTO `question` VALUES ('2', '2', '2', '2017-08-12 22:21:05', '2', 'Keyword2', 'tester2');
INSERT INTO `question` VALUES ('3', '3', '3', '2017-08-12 22:21:06', '3', 'Keyword3', 'tester3');
INSERT INTO `question` VALUES ('4', '4', '4', '2017-08-12 22:21:06', '4', 'Keyword4', 'tester4');
INSERT INTO `question` VALUES ('5', '5', '5', '2017-08-12 22:21:06', '5', 'Keyword5', 'tester5');
INSERT INTO `question` VALUES ('6', '6', '6', '2017-08-12 22:21:07', '6', 'Keyword6', 'tester6');
INSERT INTO `question` VALUES ('7', '7', '7', '2017-08-12 22:21:09', '7', 'Keyword7', 'tester7');
INSERT INTO `question` VALUES ('8', '8', '8', '2017-08-12 22:21:10', '8', 'Keyword8', 'tester8');
INSERT INTO `question` VALUES ('9', '9', '9', '2017-08-16 10:14:22', '999', 'Keyword9', 'tester9');
INSERT INTO `question` VALUES ('10', '10', '10', '2017-08-12 22:21:13', '10', 'Keyword10', 'tester10');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `regtime` datetime DEFAULT NULL,
  `ip` varchar(255) DEFAULT NULL,
  `status` int(1) DEFAULT '0',
  `activationtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', 'Benjamin', '123', 'Benjamin_v@qq.com', '2017-08-17 11:17:20', '127.0.0.1', '1', '2017-08-02 11:17:34');
SET FOREIGN_KEY_CHECKS=1;
