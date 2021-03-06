# Generated by Django 3.2.3 on 2021-05-30 15:44

from django.db import migrations, models
import user.validations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=70, unique=True, validators=[user.validations.validate_email]),
        ),
    ]
