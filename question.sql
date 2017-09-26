/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 50718
Source Host           : 127.0.0.1:3306
Source Database       : question

Target Server Type    : MYSQL
Target Server Version : 50718
File Encoding         : 65001

Date: 2017-09-26 13:32:19
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for content_in_content
-- ----------------------------
DROP TABLE IF EXISTS `content_in_content`;
CREATE TABLE `content_in_content` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` varchar(5000) CHARACTER SET utf8 DEFAULT NULL,
  `fbtime` varchar(30) CHARACTER SET utf8 DEFAULT NULL,
  `content_id` int(11) DEFAULT NULL,
  `content_user` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `main_user` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for question
-- ----------------------------
DROP TABLE IF EXISTS `question`;
CREATE TABLE `question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `content` text,
  `fbtime` varchar(24) DEFAULT NULL,
  `click` int(255) DEFAULT NULL,
  `keywords` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for question_content
-- ----------------------------
DROP TABLE IF EXISTS `question_content`;
CREATE TABLE `question_content` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `content` varchar(5000) CHARACTER SET utf8 DEFAULT NULL,
  `fbtime` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  `title_id` int(10) DEFAULT NULL,
  `content_user` varchar(30) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
SET FOREIGN_KEY_CHECKS=1;
