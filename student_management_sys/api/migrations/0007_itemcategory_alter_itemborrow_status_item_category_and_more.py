# Generated by Django 5.0.1 on 2024-01-24 17:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_item_status_student_email_itemborrow'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='itemborrow',
            name='status',
            field=models.CharField(default='borrowed', max_length=20),
        ),
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='api.itemcategory'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='items',
            field=models.ManyToManyField(blank=True, to='api.itemcategory'),
        ),
    ]
