# Generated by Django 2.0.3 on 2018-04-03 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitor', '0008_visitor_request_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='request_id',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]