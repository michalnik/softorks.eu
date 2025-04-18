# Generated by Django 5.1.7 on 2025-04-01 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='description_cs',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='reference',
            name='description_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='reference',
            name='name_cs',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='reference',
            name='name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='reference',
            name='url_cs',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='reference',
            name='url_en',
            field=models.URLField(null=True),
        ),
    ]
