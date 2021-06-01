# Generated by Django 2.2.12 on 2021-05-31 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0004_auto_20210530_1515'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blank_F_null_F', models.CharField(max_length=20)),
                ('blank_T_null_F', models.CharField(blank=True, max_length=20)),
                ('blank_F_null_T', models.CharField(max_length=20, null=True)),
                ('blank_T_null_T', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'chartests',
            },
        ),
        migrations.CreateModel(
            name='IntTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blank_F_null_F', models.IntegerField()),
                ('blank_T_null_F', models.IntegerField(blank=True)),
                ('blank_F_null_T', models.IntegerField(null=True)),
                ('blank_T_null_T', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'inttests',
            },
        ),
        migrations.AlterField(
            model_name='posting',
            name='image',
            field=models.ImageField(upload_to='photos/'),
        ),
    ]
