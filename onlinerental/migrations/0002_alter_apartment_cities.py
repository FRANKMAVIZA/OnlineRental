# Generated by Django 3.2.2 on 2021-05-18 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onlinerental', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='Cities',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apartments', to='onlinerental.cities'),
        ),
    ]
