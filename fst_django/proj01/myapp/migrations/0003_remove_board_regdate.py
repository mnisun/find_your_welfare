# Generated by Django 4.2.7 on 2023-11-20 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_board'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='regdate',
        ),
    ]