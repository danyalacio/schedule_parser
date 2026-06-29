-- Создание базы данных (выполните один раз, если БД ещё не существует)
CREATE DATABASE IF NOT EXISTS imsitid
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

USE imsitid;

CREATE TABLE IF NOT EXISTS `schedule` (
  `id` int NOT NULL,
  `group_name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `week_number` tinyint(1) NOT NULL COMMENT '1 или 2 неделя',
  `day_of_week` tinyint(1) NOT NULL COMMENT '1-7 (Пн-Вс)',
  `lesson_number` tinyint(1) NOT NULL COMMENT '1-7 пара',
  `subject_name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `room_number` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `teacher_name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS `teachers` (
  `id` int NOT NULL,
  `full_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Полное ФИО преподавателя',
  `short_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Краткое имя',
  `department` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '---',
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '-Email преподавателя',
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '-Телефон',
  `is_active` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'Активен ли преподаватель(везде 1)',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Справочник преподавателей';

CREATE TABLE IF NOT EXISTS `teacher_schedule` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `teacher_id` int NOT NULL COMMENT 'ID преподавателя из таблицы teachers',
  `week_number` tinyint(1) NOT NULL COMMENT '1 или 2 неделя',
  `day_of_week` tinyint(1) NOT NULL COMMENT '1-6 (Пн-Сб)',
  `lesson_number` tinyint(1) NOT NULL COMMENT '1-7 пара',
  `subject_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Название предмета',
  `room_number` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Номер аудитории',
  `group_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Название группы',
  `start_time` time NOT NULL COMMENT 'Время начала пары',
  `end_time` time NOT NULL COMMENT 'Время окончания пары',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Расписание преподавателей';
