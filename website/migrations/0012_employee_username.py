# Generated by Django 2.1.7 on 2020-05-10 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_remove_employee_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='username',
            field=models.CharField(default=725725, max_length=50, unique=True),
            preserve_default=False,
        ),
    ]