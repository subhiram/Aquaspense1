# Generated by Django 4.1.5 on 2023-02-25 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_main_crop_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='type',
            field=models.CharField(default='feed', max_length=50),
            preserve_default=False,
        ),
    ]
