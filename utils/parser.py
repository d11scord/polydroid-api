import urllib.request
import json
import codecs
from schedule.models import Groups, Classroom, Teacher, Lesson, LessonType

Groups.objects.all().delete()
Classroom.objects.all().delete()
Teacher.objects.all().delete()
Lesson.objects.all().delete()
LessonType.objects.all().delete()

with codecs.open('utils/schedule.json', 'r', 'utf_8_sig') as json_file:
    data = json.load(json_file)

    for content in data['contents']:
        group = Groups(name=content['group']['title'], is_evening=content['group']['evening'] == 1)
        group.save()
        grid = content['grid']
        for day in grid:
            for number in grid[day]:
                for lesson in grid[day][number]:
                    teachers = list()
                    for teacher in lesson['teacher'].split(','):
                        obj, _ = Teacher.objects.get_or_create(
                            name=teacher.strip()
                        )
                        teachers.append(obj)
                    classrooms = list()
                    for classroom in lesson['auditories']:
                        obj1, _ = Classroom.objects.get_or_create(
                            name=classroom['title'],
                            color=classroom.get('color', '#000000')
                        )
                        classrooms.append(obj1)

                    lesson_type, _ = LessonType.objects.get_or_create(
                        name=lesson['type']
                    )

                    saved_lesson = Lesson(
                        name=lesson['sbj'],
                        day_of_week=Lesson.DAYS_OF_WEEK[int(day) - 1][0],
                        number=number,
                        group=group,
                        type=lesson_type,
                        # date_from=time.strptime(lesson['df'], "%Y-%m-%d"),
                        # date_to=time.strptime(lesson['dt'], "%Y-%m-%d"),
                        date_from=lesson['df'],
                        date_to=lesson['dt'],
                        week=1 if lesson['week'] == 'even' else 2 if lesson['week'] == 'odd' else 3,
                    )
                    saved_lesson.save()
                    saved_lesson.teachers.add(*teachers)
                    saved_lesson.classrooms.add(*classrooms)
                    saved_lesson.save()
