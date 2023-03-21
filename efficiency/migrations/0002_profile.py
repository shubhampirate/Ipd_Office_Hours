# Generated by Django 4.1.1 on 2022-10-02 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('efficiency', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('role', models.PositiveSmallIntegerField(choices=[(1, 'Employee'), (2, 'Team Leader'), (3, 'Admin')], default=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('joining_date', models.DateField(default=django.utils.timezone.now)),
                ('picture', models.ImageField(blank=True, upload_to='stations/')),
            ],
        ),
    ]
