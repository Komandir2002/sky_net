# Generated by Django 5.0.2 on 2024-02-28 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cheklist', '0006_alter_applications_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='applications',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
