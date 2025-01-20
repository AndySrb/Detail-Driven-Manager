CREATE TABLE `global_premissions` (
    `id_premission_level` bigint NOT NULL AUTO_INCREMENT,
    `role_name` varchar(16) NOT NULL DEFAULT '"USER"',
    `remove_group` tinyint(1) NOT NULL DEFAULT '0',
    `add_group` tinyint(1) NOT NULL DEFAULT '0',
    `modify_users` tinyint(1) NOT NULL DEFAULT '0',
    `mute_users` tinyint(1) NOT NULL DEFAULT '0',
    `delete_message` tinyint(1) NOT NULL DEFAULT '0',
    `set_tasks` tinyint(1) NOT NULL DEFAULT '0',
    `modify_task` tinyint(1) NOT NULL DEFAULT '0',
    `remove_task` tinyint(1) NOT NULL DEFAULT '0',
    PRIMARY KEY (`id_premission_level`)
  );


CREATE TABLE
  `users` (
    `id_user` bigint NOT NULL AUTO_INCREMENT,
    `username` varchar(24) NOT NULL,
    `password` varchar(24) NOT NULL,
    `first_name` varchar(24) NOT NULL,
    `last_name` varchar(24) NOT NULL,
    `birth_date` date NOT NULL,
    `sex` char(1) NOT NULL,
    `creation_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `status` int NOT NULL,
    `id_premission_level` bigint NOT NULL,
    PRIMARY KEY (`id_user`),
    KEY `fk_id_premission_level` (`id_premission_level`),
    CONSTRAINT `fk_id_premission_level` FOREIGN KEY (`id_premission_level`) REFERENCES `global_premissions` (`id_premission_level`)
  );
  
CREATE TABLE
  `group_data` (
    `id_group` bigint NOT NULL AUTO_INCREMENT,
    `group_name` varchar(24) NOT NULL,
    `creation_date` datetime NOT NULL,
    PRIMARY KEY (`id_group`)
  );
  

  
CREATE TABLE
  `group_premissions` (
    `id_premission_level` bigint NOT NULL AUTO_INCREMENT,
    `id_user` bigint NOT NULL,
    `id_group` bigint NOT NULL,
    `role_name` varchar(16) NOT NULL,
    `remove_group` tinyint(1) NOT NULL,
    `add_group` tinyint(1) NOT NULL,
    `modify_users` tinyint(1) NOT NULL,
    `mute_users` tinyint(1) NOT NULL,
    `delete_message` tinyint(1) NOT NULL,
    `set_tasks` tinyint(1) NOT NULL,
    `modify_task` tinyint(1) NOT NULL,
    `remove_task` tinyint(1) NOT NULL,
    PRIMARY KEY (`id_premission_level`),
    KEY `fk_id_user` (`id_user`),
    KEY `fk_id_group` (`id_group`),
    CONSTRAINT `fk_id_group` FOREIGN KEY (`id_group`) REFERENCES `group_data` (`id_group`),
    CONSTRAINT `fk_id_user` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`)
  );
  
CREATE TABLE
  `group_user_permissions` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `id_group` bigint NOT NULL,
    `id_user` bigint NOT NULL,
    `id_group_premission` bigint NOT NULL,
    PRIMARY KEY (`id`),
    KEY `id_group_permissions` (`id_group`),
    KEY `id_user_permissions` (`id_user`),
    KEY `id_group_premission` (`id_group_premission`),
    CONSTRAINT `id_group_permissions` FOREIGN KEY (`id_group`) REFERENCES `group_data` (`id_group`),
    CONSTRAINT `id_group_premission` FOREIGN KEY (`id_group_premission`) REFERENCES `group_premissions` (`id_premission_level`),
    CONSTRAINT `id_user_permissions` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`)
  );
  
CREATE TABLE
  `tasks` (
    `id_task` bigint NOT NULL AUTO_INCREMENT,
    `id_group` bigint NOT NULL,
    `created_by_id` bigint NOT NULL,
    `updated_by_id` bigint NOT NULL,
    `title` varchar(32) NOT NULL,
    `description` text,
    `hours` float DEFAULT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `planned_start_date` datetime DEFAULT NULL,
    `planned_end_date` datetime DEFAULT NULL,
    `actual_start_date` datetime DEFAULT NULL,
    `actual_end_date` datetime DEFAULT NULL,
    `is_done` tinyint(1) DEFAULT NULL,
    `content` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`id_task`),
    KEY `tasks_relation_1` (`id_group`),
    KEY `tasks_relation_2` (`created_by_id`),
    KEY `tasks_relation_3` (`updated_by_id`),
    CONSTRAINT `tasks_relation_1` FOREIGN KEY (`id_group`) REFERENCES `group_data` (`id_group`),
    CONSTRAINT `tasks_relation_2` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id_user`),
    CONSTRAINT `tasks_relation_3` FOREIGN KEY (`updated_by_id`) REFERENCES `users` (`id_user`)
  );
  
CREATE TABLE
  `sub_group_data` (
    `id_sub_group` bigint NOT NULL AUTO_INCREMENT,
    `id_group` bigint NOT NULL,
    `sub_group_name` varchar(24) NOT NULL,
    `creation_date` datetime NOT NULL,
    PRIMARY KEY (`id_sub_group`),
    KEY `fk2_id_group` (`id_group`),
    CONSTRAINT `fk2_id_group` FOREIGN KEY (`id_group`) REFERENCES `group_data` (`id_group`)
  );
  
CREATE TABLE
  `task_history` (
    `id_history_task` bigint NOT NULL AUTO_INCREMENT,
    `id_task` bigint NOT NULL,
    `id_group` bigint NOT NULL,
    `updated_by_id` bigint NOT NULL,
    `title` varchar(32) DEFAULT NULL,
    `description` text,
    `hours` float DEFAULT NULL,
    `updated_at` datetime DEFAULT NULL,
    `planned_start_date` datetime DEFAULT NULL,
    `planned_end_date` datetime DEFAULT NULL,
    `actual_start_date` datetime DEFAULT NULL,
    `actual_end_date` datetime DEFAULT NULL,
    `is_done` tinyint(1) DEFAULT NULL,
    `content` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`id_history_task`),
    KEY `task_history_relation_1` (`id_task`),
    KEY `task_history_relation_2` (`id_group`),
    KEY `task_history_relation_3` (`updated_by_id`),
    CONSTRAINT `task_history_relation_1` FOREIGN KEY (`id_task`) REFERENCES `tasks` (`id_task`),
    CONSTRAINT `task_history_relation_2` FOREIGN KEY (`id_group`) REFERENCES `group_data` (`id_group`),
    CONSTRAINT `task_history_relation_3` FOREIGN KEY (`updated_by_id`) REFERENCES `users` (`id_user`)
  );
  
  
  
CREATE TABLE
  `message_user` (
    `id_message` bigint NOT NULL,
    `from_user_id` bigint NOT NULL,
    `to_user_id` bigint NOT NULL,
    `content` text NOT NULL,
    `content_attachment` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`id_message`),
    KEY `message_user_relation_1` (`from_user_id`),
    KEY `message_user_relation_2` (`to_user_id`),
    CONSTRAINT `message_user_relation_1` FOREIGN KEY (`from_user_id`) REFERENCES `users` (`id_user`),
    CONSTRAINT `message_user_relation_2` FOREIGN KEY (`to_user_id`) REFERENCES `users` (`id_user`)
  );
  
CREATE TABLE
  `message_task` (
    `id_message` bigint NOT NULL,
    `from_user_id` bigint NOT NULL,
    `to_id_task` bigint NOT NULL,
    `content` text NOT NULL,
    `content_attachment` varchar(255) DEFAULT NULL,
    KEY `message_task_relation_1` (`from_user_id`),
    KEY `message_task_relation_2` (`to_id_task`),
    CONSTRAINT `message_task_relation_1` FOREIGN KEY (`from_user_id`) REFERENCES `users` (`id_user`),
    CONSTRAINT `message_task_relation_2` FOREIGN KEY (`to_id_task`) REFERENCES `tasks` (`id_task`)
  );
  
CREATE TABLE
  `message_sub_group` (
    `id_message` bigint NOT NULL,
    `from_user_id` bigint NOT NULL,
    `to_id_sub_group` bigint NOT NULL,
    `content` text NOT NULL,
    `content_attachment` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`id_message`),
    KEY `message_sub_group_relation_1` (`from_user_id`),
    KEY `message_sub_group_relation_2` (`to_id_sub_group`),
    CONSTRAINT `message_sub_group_relation_1` FOREIGN KEY (`from_user_id`) REFERENCES `users` (`id_user`),
    CONSTRAINT `message_sub_group_relation_2` FOREIGN KEY (`to_id_sub_group`) REFERENCES `sub_group_data` (`id_sub_group`)
  );
  
CREATE TABLE
  `message_group` (
    `id_message` bigint NOT NULL,
    `from_user_id` bigint NOT NULL,
    `to_id_group` bigint NOT NULL,
    `content` text NOT NULL,
    `content_attachment` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`id_message`),
    KEY `message_group_relation_1` (`from_user_id`),
    KEY `message_group_relation_2` (`to_id_group`),
    CONSTRAINT `message_group_relation_1` FOREIGN KEY (`from_user_id`) REFERENCES `users` (`id_user`),
    CONSTRAINT `message_group_relation_2` FOREIGN KEY (`to_id_group`) REFERENCES `group_data` (`id_group`)
  );
  
  
