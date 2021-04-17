# Generated by Django 3.0.6 on 2021-03-06 12:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='download',
            fields=[
                ('DownloadID', models.AutoField(primary_key=True, serialize=False)),
                ('UserID', models.IntegerField(default=0)),
                ('ResourceID', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=1)),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now)),
                ('mtime', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='store',
            fields=[
                ('StoreID', models.AutoField(primary_key=True, serialize=False)),
                ('UserID', models.IntegerField(default=0)),
                ('ResourceID', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=1)),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now)),
                ('mtime', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='userInfo',
            fields=[
                ('UserID', models.AutoField(primary_key=True, serialize=False)),
                ('nickName', models.CharField(max_length=100)),
                ('account', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('studentID', models.CharField(blank=True, max_length=50, null=True)),
                ('studentName', models.CharField(blank=True, max_length=100, null=True)),
                ('avatarUrl', models.CharField(max_length=500)),
                ('role', models.IntegerField(default=1)),
                ('ctrl', models.IntegerField(default=7)),
                ('status', models.IntegerField(default=1)),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now)),
                ('mtime', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]