# Generated by Django 4.0.5 on 2022-06-24 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(editable=False),
        ),
    ]
