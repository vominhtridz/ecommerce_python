# Generated by Django 5.0.3 on 2024-05-23 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0002_image_delete_carausel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="image",
            field=models.ImageField(upload_to="images"),
        ),
    ]
