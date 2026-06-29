import pandas as pd
from pathlib import Path
import DB
from time import sleep
import re
DB.ClearAllBase()

sleep(0.5)
DB.RecreateTables()
def getWeek(name):
    if(name == "ПОНЕДЕЛЬНИК"):
        return 1
    elif(name == "ВТОРНИК"):
        return 2
    elif(name == "СРЕДА"):
        return 3
    elif(name == "ЧЕТВЕРГ"):
        return 4
    elif(name == "ПЯТНИЦА"):
        return 5
    elif(name == "СУББОТА"):
        return 6
lessonID = 0
def getLessonNumber(time):
    if(time == "08.00-09.30"):
        return 1
    if(time == "09.40-11.10"):
        return 2
    if(time == "11.30-13.00"):
        return 3
    if(time == "13.10-14.40"):
        return 4
    if(time == "14.50-16.20"):
        return 5
    if(time == "16.30-18.00"):
        return 6
    if(time == "18.10-19.40"):
        return 7

xls = [f for f in Path('normalized').iterdir() if f.is_file() and f.suffix in ['.xlsx', '.xls']]
teachers = list()
teacherID = 0

for i in xls:
    print(i)
    # Для .xlsx файлов используем openpyxl, для .xls - xlrd
    engine = 'openpyxl' if i.suffix == '.xlsx' else 'xlrd'
    dt = pd.read_excel(str(i), engine=engine)
    # dt = dt.ffill(limit=1)
    print(dt['Дни'])
    groups = dt.columns[2:]
    for days in range(len(dt['Дни'])-1):
        if(str(dt['Дни'][days]) != 'nan'):
            curDay = str(dt['Дни'][days]).strip()
        for group in groups:
            if(str(dt[str(group)][days]) != 'nan'):
                lesson_text = str(dt[str(group)][days])
                lesson_lines = lesson_text.split('\n')
                
                # Безопасная обработка: проверяем наличие элементов
                subject_name = lesson_lines[0].strip() if len(lesson_lines) > 0 else ''
                
                # Получаем преподавателя и аудиторию из второй строки, если она есть
                if len(lesson_lines) > 1:
                    teacher_room_line = lesson_lines[1].strip()
                    
                    # Пробуем разделить по трем пробелам
                    teacher_room = teacher_room_line.split('   ')
                    if len(teacher_room) >= 2:
                        teacher_name = teacher_room[0].strip()
                        room_number = teacher_room[1].strip()
                    else:
                        # Если разделителя нет, пытаемся найти номер кабинета в конце строки
                        # Ищем паттерны: "1-103", "1-103-1", "103", "с/зал" и т.д.
                        # Сначала ищем полные номера кабинетов (например, "1-103", "1-103-1")
                        # Паттерн ищет номер кабинета в конце строки (может быть с пробелами перед ним)
                        room_patterns = [
                            r'\s+(\d+-\d+(?:-\d+)*(?:-\d+)*)\s*$',  # Полные номера типа "1-103", "1-103-1"
                            r'\s+(с/зал)\s*$',  # Спортивный зал
                            r'\s+(\d+)\s*$',  # Просто число в конце
                        ]
                        
                        match = None
                        for pattern in room_patterns:
                            match = re.search(pattern, teacher_room_line)
                            if match:
                                break
                        
                        if match:
                            # Найден номер кабинета
                            room_number = match.group(1).strip()
                            # Извлекаем имя преподавателя (все до номера кабинета)
                            teacher_name = teacher_room_line[:match.start()].strip()
                            # Убираем лишние пробелы из имени преподавателя
                            teacher_name = ' '.join(teacher_name.split())
                        else:
                            # Если номер кабинета не найден, вся строка - это преподаватель
                            teacher_name = teacher_room_line
                            room_number = ''
                else:
                    # Если нет второй строки, используем пустые значения
                    teacher_name = ''
                    room_number = ''
                
                # Дополнительная проверка: если кабинет не найден, но в имени преподавателя есть номер кабинета
                if not room_number and teacher_name:
                    # Ищем номер кабинета в конце имени преподавателя
                    room_patterns_check = [
                        r'\s+(\d+-\d+(?:-\d+)*(?:-\d+)*)\s*$',  # Полные номера типа "1-103"
                        r'\s+(с/зал)\s*$',  # Спортивный зал
                    ]
                    for pattern in room_patterns_check:
                        match_check = re.search(pattern, teacher_name)
                        if match_check:
                            room_number = match_check.group(1).strip()
                            teacher_name = teacher_name[:match_check.start()].strip()
                            break
                
                current_lesson = [subject_name, teacher_name, room_number]
                newteach = current_lesson[1]
                
                # Добавляем префикс "1-" только если кабинет не пустой, не равен "1-", 
                # не содержит уже "-" и не является "с/зал"
                if current_lesson[2] and current_lesson[2] != '1-' and ('-' not in current_lesson[2]) and ('с/зал' not in current_lesson[2]):
                    current_lesson[2] = '1-'+current_lesson[2]
                if("преп. " in current_lesson[1]):
                    newteach = current_lesson[1][6:]
                    if (newteach not in teachers):
                        teachers.append(newteach)
                elif(current_lesson[1] not in teachers):
                    if(current_lesson[1] == ''):
                        current_lesson[1] = '-'
                    if(current_lesson[1] not in teachers):
                        teachers.append(current_lesson[1])

                # print(group)
                if(days % 2 == 0):
                    time = str(dt['Часы'][days]).strip()
                    fullLessonDataForGroup = (lessonID
                                              ,group, 
                                      1, 
                                      getWeek(curDay), 
                                      getLessonNumber(time), 
                                      current_lesson[0], 
                                      current_lesson[2], 
                                      current_lesson[1], 
                                      ':'.join(time.split('-')[0].split('.')),
                                      ':'.join(time.split('-')[1].split('.')))
                    # print(curDay)
                else:
                    time = str(dt['Часы'][days-1]).strip()
                    fullLessonDataForGroup = [
                                      lessonID,
                                      group, 
                                      2, 
                                      getWeek(str(curDay)), 
                                      getLessonNumber(str(time)), 
                                      current_lesson[0], 
                                      current_lesson[2], 
                                      current_lesson[1], 
                                      ':'.join(time.split('-')[0].split('.')),
                                      ':'.join(time.split('-')[1].split('.'))]
                # print(fullLessonDataForGroup)
                    
                DB.AddToSchedule(fullLessonDataForGroup[0], 
                                 fullLessonDataForGroup[1], 
                                 fullLessonDataForGroup[2], 
                                 fullLessonDataForGroup[3], 
                                 fullLessonDataForGroup[4], 
                                 fullLessonDataForGroup[5], 
                                 fullLessonDataForGroup[6], 
                                 fullLessonDataForGroup[7], 
                                 fullLessonDataForGroup[8],
                                 fullLessonDataForGroup[9])
                lessonID += 1
                # print('\n')
                
# print(teachers)
for i in teachers:
    DB.AddToTeachers(teacherID, i)
    teacherID += 1
DB.CreateTeachersSchedule()