# Generated by Django 4.1.5 on 2023-01-30 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_expenses_exp_cost'),
    ]

    operations = [
        migrations.CreateModel(
            name='sample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField()),
            ],
        ),
    ]