# Generated by Django 2.1.3 on 2018-12-07 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='icon',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='菜单图标'),
        ),
    ]