# Generated by Django 3.1 on 2021-09-14 13:17

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('audition', '0003_vote_pass_band'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='pass_band',
            field=django_mysql.models.ListCharField(models.CharField(max_length=150), blank=True, editable=False, max_length=7550, size=50),
        ),
    ]
