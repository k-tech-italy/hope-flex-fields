# Generated by Django 3.2.25 on 2024-07-13 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('hope_flex_fields', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldset',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
    ]
