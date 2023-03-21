# Generated by Django 3.2.8 on 2023-03-19 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('efficiency', '0003_attendance_project_alter_profile_picture_timer_task_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='efficiency',
            name='year',
            field=models.PositiveIntegerField(default=2023),
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('1', 'Employee'), ('2', 'Team Leader'), ('3', 'Admin')], default='1', max_length=15),
        ),
    ]
