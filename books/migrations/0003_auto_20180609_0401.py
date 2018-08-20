# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20180527_1217'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('brief', models.CharField(null=True, blank=True, max_length=255)),
                ('max_members', models.IntegerField(default=200)),
            ],
            options={
                'verbose_name_plural': '聊天组',
                'verbose_name': '聊天组',
            },
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name_plural': '用户表', 'verbose_name': '用户表'},
        ),
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(related_name='_user_friends_+', to='books.User', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='head_img',
            field=models.ImageField(upload_to='uploads', null=True, blank=True, verbose_name='头像'),
        ),
        migrations.AddField(
            model_name='user',
            name='signature',
            field=models.CharField(null=True, blank=True, max_length=255, verbose_name='签名'),
        ),
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(verbose_name='年龄'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=30, verbose_name='昵称'),
        ),
        migrations.AlterField(
            model_name='user',
            name='passwd',
            field=models.CharField(max_length=32, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.BooleanField(verbose_name='性别'),
        ),
        migrations.AddField(
            model_name='webgroup',
            name='admins',
            field=models.ManyToManyField(related_name='group_admins', to='books.User', blank=True),
        ),
        migrations.AddField(
            model_name='webgroup',
            name='members',
            field=models.ManyToManyField(related_name='group_members', to='books.User', blank=True),
        ),
        migrations.AddField(
            model_name='webgroup',
            name='owner',
            field=models.ForeignKey(to='books.User',on_delete=models.CASCADE),
        ),
    ]
