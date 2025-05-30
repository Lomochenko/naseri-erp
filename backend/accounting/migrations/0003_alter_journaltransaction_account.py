# Generated by Django 5.0.7 on 2025-05-31 16:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journaltransaction',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='journal_transactions', to='accounting.account', verbose_name='account'),
        ),
    ]
