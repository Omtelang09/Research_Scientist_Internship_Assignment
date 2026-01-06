CREATE TABLE `organizations` (
  `org_id` text PRIMARY KEY,
  `name` text NOT NULL,
  `domain` text NOT NULL
);

CREATE TABLE `teams` (
  `team_id` text PRIMARY KEY,
  `org_id` text NOT NULL,
  `name` text NOT NULL
);

CREATE TABLE `users` (
  `user_id` text PRIMARY KEY,
  `org_id` text NOT NULL,
  `full_name` text NOT NULL,
  `email` text UNIQUE NOT NULL,
  `role` text NOT NULL
);

CREATE TABLE `team_memberships` (
  `team_id` text,
  `user_id` text,
  PRIMARY KEY (`team_id`, `user_id`)
);

CREATE TABLE `projects` (
  `project_id` text PRIMARY KEY,
  `team_id` text NOT NULL,
  `name` text NOT NULL,
  `created_at` timestamp
);

CREATE TABLE `sections` (
  `section_id` text PRIMARY KEY,
  `project_id` text NOT NULL,
  `name` text NOT NULL
);

CREATE TABLE `tasks` (
  `task_id` text PRIMARY KEY,
  `project_id` text NOT NULL,
  `section_id` text NOT NULL,
  `assignee_id` text,
  `parent_task_id` text,
  `name` text NOT NULL,
  `description` text,
  `due_date` date,
  `completed` boolean,
  `created_at` timestamp,
  `completed_at` timestamp
);

CREATE TABLE `tags` (
  `tag_id` text PRIMARY KEY,
  `name` text NOT NULL
);

CREATE TABLE `task_tags` (
  `task_id` text,
  `tag_id` text,
  PRIMARY KEY (`task_id`, `tag_id`)
);

CREATE TABLE `custom_field_definitions` (
  `field_id` text PRIMARY KEY,
  `org_id` text NOT NULL,
  `name` text NOT NULL,
  `type` text NOT NULL
);

CREATE TABLE `custom_field_values` (
  `value_id` text PRIMARY KEY,
  `task_id` text NOT NULL,
  `field_id` text NOT NULL,
  `text_value` text,
  `number_value` float
);

ALTER TABLE `teams` ADD FOREIGN KEY (`org_id`) REFERENCES `organizations` (`org_id`);

ALTER TABLE `users` ADD FOREIGN KEY (`org_id`) REFERENCES `organizations` (`org_id`);

ALTER TABLE `team_memberships` ADD FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`);

ALTER TABLE `team_memberships` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `projects` ADD FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`);

ALTER TABLE `sections` ADD FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`);

ALTER TABLE `tasks` ADD FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`);

ALTER TABLE `tasks` ADD FOREIGN KEY (`section_id`) REFERENCES `sections` (`section_id`);

ALTER TABLE `tasks` ADD FOREIGN KEY (`assignee_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `tasks` ADD FOREIGN KEY (`parent_task_id`) REFERENCES `tasks` (`task_id`);

ALTER TABLE `task_tags` ADD FOREIGN KEY (`task_id`) REFERENCES `tasks` (`task_id`);

ALTER TABLE `task_tags` ADD FOREIGN KEY (`tag_id`) REFERENCES `tags` (`tag_id`);

ALTER TABLE `custom_field_definitions` ADD FOREIGN KEY (`org_id`) REFERENCES `organizations` (`org_id`);

ALTER TABLE `custom_field_values` ADD FOREIGN KEY (`task_id`) REFERENCES `tasks` (`task_id`);

ALTER TABLE `custom_field_values` ADD FOREIGN KEY (`field_id`) REFERENCES `custom_field_definitions` (`field_id`);
