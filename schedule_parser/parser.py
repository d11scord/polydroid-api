def parse():
    print('start downloading')
    download_file()
    print('Downloaded')
    print('Start parsing in diff mode')
    write_database(False)
    print('Start parsing in rewrite mode')
    write_database(True)
    print('End parsing')


def download_file():
    json_url = 'https://rasp.dmami.ru/semester.json'
    file_url = 'schedule_parser/json/schedule.json'
    urllib.request.urlretrieve(json_url, file_url)


def write_database(is_rewrite):
    """
    :param is_rewrite: Boolean. False if function should only detect changes,
     True if should rewrite old database
    """
    from schedule.models import Groups, Classroom, Teacher, Lesson, LessonType, Notification
    with codecs.open('schedule_parser/json/schedule.json', 'r', 'utf_8_sig') as json_file:
        data = json.load(json_file)
        if is_rewrite:
            clear_database()
        for content in data['contents']:
            group, _ = Groups.objects.get_or_create(
                name=content['group']['title'],
                course=content['group']['course'],
                date_from=datetime.datetime.strptime(content['group']['dateFrom'], "%Y-%m-%d").date(),
                date_to=datetime.datetime.strptime(content['group']['dateTo'], "%Y-%m-%d").date(),
                is_evening=content['group']['evening'] == 1, )

            grid = content['grid']
            for day in grid:
                for number in grid[day]:

                    old_lessons_array = list(Lesson.objects.filter(
                            day_of_week=int(day),
                            number=int(number),
                            group__name=group.name)
                    )

                    new_lessons_array = list()
                    for lesson in grid[day][number]:
                        new_lesson_teachers = list()
                        for teacher in lesson['teacher'].split(','):
                            new_teacher, _ = Teacher.objects.get_or_create(
                                name=teacher.strip()
                            )
                            new_lesson_teachers.append(new_teacher)

                        new_lesson_classrooms = list()
                        for classroom in lesson['auditories']:
                            new_classroom, _ = Classroom.objects.get_or_create(
                                name=classroom['title'],
                                color=classroom.get('color', '#000000')
                            )
                            new_lesson_classrooms.append(new_classroom)

                        new_lesson_type, _ = LessonType.objects.get_or_create(
                            name=lesson['type']
                        )

                        new_lesson = Lesson(
                            name=lesson['sbj'],
                            day_of_week=int(day),
                            number=int(number),
                            group=group,
                            type=new_lesson_type,
                            date_from=datetime.datetime.strptime(lesson['df'], "%Y-%m-%d").date(),
                            date_to=datetime.datetime.strptime(lesson['dt'], "%Y-%m-%d").date(),
                            week=1 if lesson['week'] == 'even' else 2 if lesson['week'] == 'odd' else 3,
                        )
                        new_lesson.save()
                        new_lesson.teachers.add(*new_lesson_teachers)
                        new_lesson.classrooms.add(*new_lesson_classrooms)
                        new_lesson.save()

                        new_lessons_array.append(new_lesson)
                    if not is_rewrite and not list_equals(old_lessons_array, new_lessons_array):
                        for old_lesson in old_lessons_array:
                            for new_lesson in new_lessons_array:
                                if old_lesson.equals(new_lesson):
                                    old_lessons_array.remove(old_lesson)
                                    new_lessons_array.remove(new_lesson)

                        for new_lesson in new_lessons_array:
                            for old_lesson in old_lessons_array:
                                if new_lesson.equals(old_lesson):
                                    new_lessons_array.remove(new_lesson)
                                    old_lessons_array.remove(old_lesson)
                        for old_lesson in old_lessons_array:
                            Notification(
                                time=timezone.now(),
                                old_lesson=old_lesson.to_json(),
                                new_lesson="",
                                targets=get_notification_targets(old_lesson)
                            ).save()
                        for new_lesson in new_lessons_array:
                            Notification(
                                time=timezone.now(),
                                old_lesson="",
                                new_lesson=new_lesson.to_json(),
                                targets=get_notification_targets(new_lesson)
                            ).save()


def get_notification_targets(lesson):
    targets = "[" + lesson.group.name
    for teacher in lesson.teachers.all():
        targets += (", " + teacher.name)
    return targets + "]"


def clear_database():
    from schedule.models import Groups, Classroom, Teacher, Lesson, LessonType

    Lesson.objects.all().delete()
    Classroom.objects.all().delete()
    Teacher.objects.all().delete()
    Groups.objects.all().delete()
    LessonType.objects.all().delete()

    # cursor = connection.cursor()
    # cursor.execute("UPDATE sqlite_sequence SET seq=0 WHERE name = 'schedule_lesson'")
    # cursor.execute("UPDATE sqlite_sequence SET seq=0 WHERE name = 'schedule_lesson_classrooms'")
    # cursor.execute("UPDATE sqlite_sequence SET seq=0 WHERE name = 'schedule_classroom'")
    # cursor.execute("UPDATE sqlite_sequence SET seq=0 WHERE name = 'schedule_lesson_teachers'")
    # cursor.execute("UPDATE sqlite_sequence SET seq=0 WHERE name = 'schedule_teacher'")
    # cursor.execute("UPDATE sqlite_sequence SET seq=0 WHERE name = 'schedule_lessontype'")
    # cursor.execute("UPDATE sqlite_sequence SET seq=0 WHERE name = 'schedule_groups'")


def list_equals(first, second):
    is_equals = True
    if len(first) != len(second):
        return False
    else:
        for element_first, element_second in zip(first, second):
            if not element_first.equals(element_second):
                is_equals = False
    return is_equals


def list_to_json(objects):
    json = '['
    for obj in objects:
        json = json+obj.to_json()
    json = json+']'
    return json


if __name__ == "__main__":
    import django
    import urllib.request
    import json
    import codecs
    import datetime
    from django.db import connection
    from django.utils import timezone

    django.setup()
    parse()