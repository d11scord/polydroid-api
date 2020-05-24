from django.db import models
from schedule.modelmixin import ModelDiffMixin
from utils.list_utils import list_to_json, list_equals


class Groups(models.Model):
    name = models.CharField(max_length=20, unique=True)
    course = models.SmallIntegerField(null=True, blank=True)
    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)
    is_evening = models.BooleanField(default=False)

    def __str__(self):
        return '{} {}'.format(self.id, self.name)

    def equals(self, other):
        return self.name == other.name \
               and self.course == other.course \
               and self.date_from == other.date_from \
               and self.date_to == other.date_to \
               and self.is_evening == other.is_evening

    def to_json(self):
        return '{name: '+self.name + \
               ', course: '+str(self.course) + \
               ', date_from: '+str(self.date_from) + \
               ', date_to: '+str(self.date_to) + \
               ', is_evening: '+str(self.is_evening) + '}'

    class Meta:
        verbose_name_plural = 'Group'
        verbose_name = 'group'


class Teacher(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

    def equals(self, other):
        return self.name == other.name

    def to_json(self):
        return '{name: ' + self.name + '}'


class Classroom(models.Model, ModelDiffMixin):
    name = models.CharField(max_length=150, unique=True)
    color = models.CharField(max_length=8)

    def __str__(self):
        return self.name

    def equals(self, other):
        return self.name == other.name and self.color == other.color

    def to_json(self):
        return '{name: ' + self.name + ', color: ' + self.color + '}'


class LessonType(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return str('{}: {}'.format(self.id, self.name))

    def equals(self, other):
        return self.name == other.name

    def to_json(self):
        return '{name: ' + self.name + '}'


class Lesson(models.Model):
    LESSON_WEEK = (
        (1, 'even'),
        (2, 'odd'),
        (3, 'both')
    )
    DAYS_OF_WEEK = (
        (1, 'monday'),
        (2, 'tuesday'),
        (3, 'wednesday'),
        (4, 'thursday'),
        (5, 'friday'),
        (6, 'saturday'),
        (7, 'sunday'),
    )
    name = models.CharField(max_length=200)
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    number = models.IntegerField()
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    classrooms = models.ManyToManyField(Classroom)
    teachers = models.ManyToManyField(Teacher)
    type = models.ForeignKey(LessonType, on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()
    week = models.IntegerField(choices=LESSON_WEEK)

    def __str__(self):
        return '{} {}'.format(self.name, self.group)

    def equals(self, other):
        return self.name == other.name \
               and self.day_of_week == other.day_of_week \
               and self.number == other.number \
               and self.type.name == other.type.name \
               and self.date_from == other.date_from \
               and list_equals(self.teachers.all(), other.teachers.all()) \
               and list_equals(self.classrooms.all(), other.classrooms.all()) \
               and self.date_to == other.date_to \
               and self.week == other.week

    def to_json(self):
        return '{name: ' + self.name + ', day_of_week: ' + str(self.day_of_week) + ', number: ' + str(self.number) \
               + ', group: ' + self.group.to_json() + ', classrooms: ' + list_to_json(self.classrooms.all()) + ', teachers: ' \
               + list_to_json(self.teachers.all()) + ', type: ' + self.type.name+', date_from: ' + str(self.date_from) \
               + ', date_to: ' + str(self.date_to) + ', week: ' + str(self.week) + '}'


class Notification(models.Model):
    time = models.DateTimeField()
    old_lesson = models.TextField()
    new_lesson = models.TextField()
    targets = models.TextField()

    def equals(self, other):
        return self.time == other.time \
               and self.old_lesson == other.old_lesson \
               and self.new_lesson == other.new_lesson
