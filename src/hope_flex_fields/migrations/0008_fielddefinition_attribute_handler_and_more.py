# Generated by Django 5.1.2 on 2024-10-22 16:06

import strategy_field.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hope_flex_fields", "0007_create_default_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="fielddefinition",
            name="attribute_handler",
            field=strategy_field.fields.StrategyField(
                default="hope_flex_fields.attributes.registry.BaseAttributeHandler"
            ),
        ),
        migrations.AlterField(
            model_name="datachecker",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="datacheckerfieldset",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="fielddefinition",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="fieldset",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="flexfield",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
