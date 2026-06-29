import mysql.connector
from time import sleep
mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="imsitid"
        )
print("Connection")



def ClearAllBase():
    cursor = mydb.cursor()
    cursor.execute((f"DROP TABLE IF EXISTS schedule"))
    cursor.execute((f"DROP TABLE IF EXISTS teacher_schedule"))
    cursor.execute((f"DROP TABLE IF EXISTS teachers"))
    mydb.commit()

def RecreateTables():
    cursor = mydb.cursor()
    cursor.execute("""CREATE TABLE `schedule` (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;""")
    cursor.execute("""CREATE TABLE `teachers` (
  `id` int NOT NULL,
  `full_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Полное ФИО преподавателя',
  `short_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Краткое имя',
  `department` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '---',
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '-Email преподавателя',
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '-Телефон',
  `is_active` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'Активен ли преподаватель(везде 1)',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Справочник преподавателей';""")
    cursor.execute("""CREATE TABLE `teacher_schedule` (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Расписание преподавателей';""")
    mydb.commit()

    
def AddToTeachers(id,name):
    cursor = mydb.cursor()
    cursor.execute(f"INSERT into teachers(id,full_name, short_name) values ({id}, '{name}', '{name}')")
    with open('create.sql', 'a', encoding='utf-8') as file:
        file.write(f"INSERT into teachers(id,full_name, short_name) values ({id}, '{name}', '{name}');\n")
    mydb.commit()

def AddToSchedule(id,group_name,week_number,day_of_week,lesson_number,subject_name,room_number,teacher_name,start_time,end_time):
    cursor = mydb.cursor()
    
    # Проверяем, существует ли уже такая запись (дубликат)
    # Проверяем по ключевым полям: группа, неделя, день недели, номер пары
    check_query = """SELECT id FROM schedule 
                     WHERE group_name = %s 
                     AND week_number = %s 
                     AND day_of_week = %s 
                     AND lesson_number = %s
                     LIMIT 1"""
    cursor.execute(check_query, (group_name, week_number, day_of_week, lesson_number))
    existing = cursor.fetchone()
    
    if existing:
        # Запись уже существует, пропускаем (или можно обновить)
        print(f"Дубликат пропущен: группа={group_name}, неделя={week_number}, день={day_of_week}, пара={lesson_number}")
        return
    
    # Если записи нет, добавляем новую
    # with open('createSh.sql', 'a', encoding='utf-8') as file:
    #     file.write(f"insert into schedule(id,group_name,week_number,day_of_week,lesson_number,subject_name,room_number,teacher_name,start_time,end_time) values ({id}, '{group_name}', {week_number}, {day_of_week}, {lesson_number}, '{subject_name}', '{room_number}', '{teacher_name}', '{start_time}', '{end_time}');\n")
    cursor.execute(f"insert into schedule(id,group_name,week_number,day_of_week,lesson_number,subject_name,room_number,teacher_name,start_time,end_time) values ({id}, '{group_name}', {week_number}, {day_of_week}, {lesson_number}, '{subject_name}', '{room_number}', '{teacher_name}', '{start_time}', '{end_time}')")
    mydb.commit()

def CreateTeachersSchedule():
    cursor = mydb.cursor()
    cursor.execute("""INSERT INTO teacher_schedule (
    teacher_id,
    week_number,
    day_of_week,
    lesson_number,
    subject_name,
    room_number,
    group_name,
    start_time,
    end_time,
    created_at,
    updated_at
)
SELECT 
    t.id AS teacher_id,
    s.week_number,
    s.day_of_week,
    s.lesson_number,
    s.subject_name,
    s.room_number,
    s.group_name,
    s.start_time AS start_time,
    s.end_time,
    NOW() AS created_at,
    NOW() AS updated_at
FROM schedule s
INNER JOIN teachers t ON s.teacher_name COLLATE utf8mb4_unicode_ci = t.full_name COLLATE utf8mb4_unicode_ci;""")
    mydb.commit()