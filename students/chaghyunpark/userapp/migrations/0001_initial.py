# Generated by Django 3.2.3 on 2021-05-28 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=45)),
                ('phone_number', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'account',
            },
        ),
    ]
