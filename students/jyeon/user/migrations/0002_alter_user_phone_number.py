# Generated by Django 3.2.3 on 2021-05-29 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
