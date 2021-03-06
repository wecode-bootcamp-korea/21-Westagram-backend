# Generated by Django 3.2.3 on 2021-05-28 02:57

from django.db import migrations, models
import user.validators


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210527_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=50, validators=[user.validators.validate_email]),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=50, validators=[user.validators.validate_password]),
        ),
    ]
