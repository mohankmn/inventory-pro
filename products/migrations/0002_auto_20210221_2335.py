# Generated by Django 3.1.6 on 2021-02-21 18:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='salesman',
        ),
        migrations.AddField(
            model_name='product',
            name='average_daily_demand',
            field=models.PositiveIntegerField(default='0', null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='carrying_cost',
            field=models.PositiveIntegerField(default='0', help_text='Enter as percentage of unit cost', validators=[products.models.validate_even]),
        ),
        migrations.AddField(
            model_name='product',
            name='eoq',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='lead_time',
            field=models.PositiveIntegerField(blank=True, default='0', null=True, validators=[products.models.validate_zero]),
        ),
        migrations.AddField(
            model_name='product',
            name='no_of_workingdays',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='ordering_cost',
            field=models.PositiveIntegerField(default='0', null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='rq',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='service_level',
            field=models.PositiveIntegerField(blank=True, default='0', null=True, validators=[products.models.validate_even]),
        ),
        migrations.AddField(
            model_name='product',
            name='standard_deviation',
            field=models.PositiveIntegerField(blank=True, default='0', null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='total_inventory',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='unit_costprice',
            field=models.PositiveIntegerField(default='0', null=True, validators=[products.models.validate_zero]),
        ),
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='z',
            field=models.DecimalField(blank=True, decimal_places=3, default='0', max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='purchase',
            name='recieved',
            field=models.IntegerField(default='0', null=True),
        ),
        migrations.AddField(
            model_name='purchase',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='demand', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='price',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='demands', to='products.product'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
    ]
