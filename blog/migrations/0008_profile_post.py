# Generated by Django 3.2.8 on 2022-04-30 02:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20210910_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.post'),
        ),
    ]