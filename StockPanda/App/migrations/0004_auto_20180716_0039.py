# Generated by Django 2.0.7 on 2018-07-16 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_auto_20180715_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptocurrency',
            name='current_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='cash',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='total_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='stock',
            name='current_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='superportfolio',
            name='total_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
    ]