# Generated by Django 3.2.3 on 2021-06-02 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210602_0702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(default='', max_length=45),
            preserve_default=False,
        ),
    ]
