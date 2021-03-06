# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-18 16:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0001_initial'),
        ('accordance', '0004_auto_20170418_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_code', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Quantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='suppliercode',
            name='acc_code',
        ),
        migrations.RemoveField(
            model_name='product',
            name='base_code',
        ),
        migrations.AddField(
            model_name='product',
            name='code',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='SupplierCode',
        ),
        migrations.AddField(
            model_name='quantity',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accordance.Product'),
        ),
        migrations.AddField(
            model_name='quantity',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.Warehouse'),
        ),
        migrations.AddField(
            model_name='match',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accordance.Product'),
        ),
        migrations.AddField(
            model_name='match',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.Supplier'),
        ),
    ]
