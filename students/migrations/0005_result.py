# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-10 16:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_exam'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField(null=True, verbose_name='\u041e\u0446\u0456\u043d\u043a\u0430')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Exam', verbose_name='\u041d\u0430\u0437\u0432\u0430 \u043f\u0440\u0435\u0434\u043c\u0435\u0442\u0443')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Student', verbose_name='\u0421\u0442\u0443\u0434\u0435\u043d\u0442')),
            ],
            options={
                'verbose_name': '\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u0406\u0441\u043f\u0438\u0442\u0443',
                'verbose_name_plural': '\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0438 \u0406\u0441\u043f\u0438\u0442\u0456\u0432',
            },
        ),
    ]
