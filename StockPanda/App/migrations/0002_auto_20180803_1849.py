# Generated by Django 2.0.7 on 2018-08-03 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='all_time_performance_amount',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='all_time_performance_percent',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='one_day_performance_amount',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='one_day_performance_percent',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='one_month_performance_amount',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='one_month_performance_percent',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='one_week_performance_amount',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='one_week_performance_percent',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='one_year_performance_amount',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='one_year_performance_percent',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='three_month_performance_amount',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='three_month_performance_percent',
        ),
        migrations.RemoveField(
            model_name='superportfolio',
            name='all_time_performance_amount',
        ),
        migrations.RemoveField(
            model_name='superportfolio',
            name='all_time_performance_percent',
        ),
        migrations.RemoveField(
            model_name='superportfolio',
            name='one_day_performance_amount',
        ),
        migrations.RemoveField(
            model_name='superportfolio',
            name='one_day_performance_percent',
        ),
        migrations.RemoveField(
            model_name='superportfolio',
            name='one_month_performance_amount',
        ),
        migrations.RemoveField(
            model_name='superportfolio',
            name='one_month_performance_percent',
        ),
        migrations.RemoveField(
            model_name='superportfolio',
            name='one_week_performance_amount',
        ),
        migrations.RemoveField(
            model_name='superportfolio',
            name='one_week_performance_percent',
        ),
        migrations.RemoveField(
            model_name='superportfolio',
            name='one_year_performance_amount',
        ),
        migrations.RemoveField(
            model_name='superportfolio',
            name='one_year_performance_percent',
        ),
        migrations.RemoveField(
            model_name='superportfolio',
            name='three_month_performance_amount',
        ),
        migrations.RemoveField(
            model_name='superportfolio',
            name='three_month_performance_percent',
        ),
    ]
