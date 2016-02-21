# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-10 16:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='exam',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='students.Exam', verbose_name='\u041d\u0430\u0437\u0432\u0430 \u043f\u0440\u0435\u0434\u043c\u0435\u0442\u0443'),
        ),
        migrations.AlterField(
            model_name='result',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='students.Student', verbose_name='\u0421\u0442\u0443\u0434\u0435\u043d\u0442'),
        ),
    ]