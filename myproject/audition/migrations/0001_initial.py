# Generated by Django 3.1 on 2021-09-18 13:57

import audition.models
from django.db import migrations, models
import django.utils.timezone
import django_mysql.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Band',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='バンド')),
                ('is_first_grade_band', models.BooleanField(default=False, verbose_name='一年生バンド')),
            ],
            options={
                'verbose_name': 'バンド',
                'verbose_name_plural': 'バンド',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('band_num', models.IntegerField(default=7, validators=[audition.models.check_vote_num], verbose_name='通過バンド数(一年生バンド数を含む)')),
                ('first_grade_band_num', models.IntegerField(default=1, validators=[audition.models.check_vote_num], verbose_name='一年生バンド数')),
                ('pass_band', django_mysql.models.ListCharField(models.CharField(max_length=150), blank=True, editable=False, max_length=7550, size=50)),
                ('is_active', models.BooleanField(default=False, verbose_name='投票中')),
                ('announce', models.BooleanField(default=False, verbose_name='結果の公開')),
                ('date_joined', models.DateTimeField(auto_now=True, verbose_name='作成日')),
            ],
            options={
                'verbose_name': '投票設定',
                'verbose_name_plural': '投票設定',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=150, verbose_name='氏名')),
                ('user_id', models.CharField(max_length=150, unique=True, verbose_name='ユーザーID')),
                ('vote_contents', django_mysql.models.ListCharField(models.CharField(max_length=150), blank=True, max_length=7550, size=50)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('suffrage', models.BooleanField(default=False, verbose_name='投票権')),
                ('vote_finish', models.BooleanField(default=False, verbose_name='投票済')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('band', models.ManyToManyField(blank=True, related_name='user_set', related_query_name='user', to='audition.Band', verbose_name='所属バンド')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'ユーザー',
                'db_table': 'User',
            },
        ),
    ]
