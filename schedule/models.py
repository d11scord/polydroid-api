from django.db import models


class Groups(models.Model):
    title = models.CharField(max_length=10)
    course = models.SmallIntegerField()
    date_from = models.DateField()
    date_to = models.DateField()
    evening = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Group'
        verbose_name = 'group'


class Teacher(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Auditory(models.Model):
    name = models.CharField(max_length=10)
    color = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Auditories'


class Lesson(models.Model):
    lab_work = 'Laboratory work'
    lecture = 'Lecture'
    practice = 'Practice'
    exam = 'Exam'
    credit = 'Credit'
    other = 'Other'
    TYPES = (
        (lab_work, 'Laboratory work'),
        (lecture, 'Lecture'),
        (practice, 'Practice'),
        (exam, 'Exam'),
        (credit, 'Credit'),
        (other, 'Other'),
    )

    first_module = 'first_module'
    second_module = 'second_module'
    no_module = 'no_module'
    none = 'none'
    MODULES = (
        (first_module, 'first_module'),
        (second_module, 'second_module'),
        (no_module, 'no_module'),
        (none, 'none'),
    )

    name = models.CharField(max_length=50)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    teachers = models.ManyToManyField(Teacher)
    type = models.CharField(max_length=20, choices=TYPES, null=False, blank=False)
    date_from = models.DateField()
    date_to = models.DateField()
    module = models.CharField(max_length=15, choices=MODULES, null=False, blank=False)

    def __str__(self):
        return '{} {}'.format(self.name, self.group)
