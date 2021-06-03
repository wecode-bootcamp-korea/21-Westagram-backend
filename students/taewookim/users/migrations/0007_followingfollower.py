# Generated by Django 3.2.3 on 2021-06-02 22:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowingFollower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='users.user')),
                ('following_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='users.user')),
            ],
            options={
                'db_table': 'following_followers',
            },
        ),
    ]
