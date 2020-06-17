import urllib.request
import json
import codecs
import datetime
from utils.list_utils import list_equals
from django.db import connection
from django.utils import timezone
import logging


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(process)d %(filename)s %(levelname)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    filename='schedule_parser/log/parser.log',
                    filemode='a')


def parse():
    logging.info('\n\n-------------------------------------------------------')

    download_start_time = timezone.datetime.now()
    logging.info('Start downloading')
    download_session_file()
    download_semester_file()
    diff_start_time = timezone.datetime.now()
    logging.info('Downloaded in ' + str((diff_start_time - download_start_time).seconds) + ' seconds\nStart parsing in diff mode')
    write_database(False, False)
    write_database(False, True)
    rewrite_start_time = timezone.datetime.now()
    logging.info('Parsing in diff mode success in ' + str((rewrite_start_time - diff_start_time).seconds / 60) + ' minutes\nStart parsing in rewrite mode')
    clear_database()
    write_database(True, False)
    write_database(True, True)
    logging.info('Parsing in rewrite mode success in ' +
                 str((timezone.datetime.now() - rewrite_start_time).seconds / 60) + ' minutes')


def download_semester_file():
    json_url = 'https://rasp.dmami.ru/semester.json'
    file_url = 'schedule_parser/json/schedule.json'
    urllib.request.urlretrieve(json_url, file_url)


def download_session_file():
    json_url = 'https://rasp.dmami.ru/session.json'
    file_url = 'schedule_parser/json/session.json'
    urllib.request.urlretrieve(json_url, file_url)


def file_as_bytes(file):
    with file:
        return file.read()


def write_database(is_rewrite, is_session):
    """
    :param is_rewrite: Boolean. False if function should only detect changes,
     True if should rewrite old database
    :param is_session: Boolean
    """
    from schedule.models import Groups, Classroom, Teacher, Lesson, LessonType, Notification
    try:
        with codecs.open('schedule_parser/json/schedule.json', 'r', 'utf_8_sig') as json_file:
            data = json.load(json_file)
            diffs_count = 0
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
                            group__name=group.name,
                            is_session=is_session)
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
                                is_session=is_session
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
                                    time=datetime.datetime.timestamp(timezone.datetime.now()) + 3 * 60 * 60 * 1000,
                                    old_lesson=old_lesson.to_json(),
                                    new_lesson="",
                                    targets=get_notification_targets(old_lesson)
                                ).save()
                                diffs_count += 1
                            for new_lesson in new_lessons_array:
                                Notification(
                                    time=datetime.datetime.timestamp(timezone.datetime.now()) + 3 * 60 * 60 * 1000,
                                    old_lesson="",
                                    new_lesson=new_lesson.to_json(),
                                    targets=get_notification_targets(new_lesson)
                                ).save()
                                diffs_count += 1
        if not is_rewrite:
            logging.info('Diffs count: ' + str(diffs_count))
    except Exception as e:
        if group is not None and day is not None and number is not None:
            logging.exception('Exception in group: ' + group.name + ', day: ' + day + ', number: ' + number)
            logging.exception(e)
        raise


def get_notification_targets(lesson):
    targets = "[" + lesson.group.name
    for teacher in lesson.teachers.all():
        targets += (", " + teacher.name)
    return targets + "]"


def clear_database():
    from schedule.models import Groups, Classroom, Teacher, Lesson, LessonType

    try:
        Lesson.objects.all().delete()
        Classroom.objects.all().delete()
        Teacher.objects.all().delete()
        Groups.objects.all().delete()
        LessonType.objects.all().delete()

        cursor = connection.cursor()
        cursor.execute("UPDATE sqlite_sequence SET seq=0 WHERE name = 'schedule_lesson'")
        cursor.execute("UPDATE sqlite_sequence SET seq=0 WHERE name = 'schedule_lesson_classrooms'")
        cursor.execute("UPDATE sqlite_sequence SET seq=0 WHERE name = 'schedule_classroom'")
        cursor.execute("UPDATE sqlite_sequence SET seq=0 WHERE name = 'schedule_lesson_teachers'")
        cursor.execute("UPDATE sqlite_sequence SET seq=0 WHERE name = 'schedule_teacher'")
        cursor.execute("UPDATE sqlite_sequence SET seq=0 WHERE name = 'schedule_lessontype'")
        cursor.execute("UPDATE sqlite_sequence SET seq=0 WHERE name = 'schedule_groups'")
    except Exception as e:
        logging.exception(e)
        raise
