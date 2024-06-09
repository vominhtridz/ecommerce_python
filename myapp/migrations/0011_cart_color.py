# Generated by Django 5.0.3 on 2024-06-01 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0010_cart"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="color",
            field=models.CharField(
                choices=[("Xám", "Xám"), ("Xanh", "Xanh"), ("Đen", "Đen")],
                default="",
                max_length=20,
            ),
        ),
    ]
