# Generated by Django 3.0.4 on 2020-03-27 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_auto_20200327_2025'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classroom',
            options={},
        ),
        migrations.AlterField(
            model_name='classroom',
            name='name',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]