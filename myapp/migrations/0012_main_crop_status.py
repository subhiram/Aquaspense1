# Generated by Django 4.1.5 on 2023-02-21 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_main_crop_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='main_crop',
            name='status',
            field=models.CharField(default='ongoing', max_length=70),
            preserve_default=False,
        ),
    ]
