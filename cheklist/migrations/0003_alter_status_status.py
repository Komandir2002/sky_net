# Generated by Django 5.0.2 on 2024-02-27 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cheklist', '0002_alter_status_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='status',
            field=models.CharField(choices=[(1, 'Оформлено'), (2, 'В процессе'), (3, 'Выполнено')], max_length=15),
        ),
    ]