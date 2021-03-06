# Generated by Django 2.1.7 on 2020-05-12 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0018_auto_20200512_1744'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chart',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='chart',
            name='service',
        ),
        migrations.RemoveField(
            model_name='deals',
            name='request',
        ),
        migrations.RemoveField(
            model_name='deals',
            name='service',
        ),
        migrations.AddField(
            model_name='deals',
            name='employee',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='website.Employee'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='requests',
            name='deal',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='website.Deals'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Chart',
        ),
    ]
