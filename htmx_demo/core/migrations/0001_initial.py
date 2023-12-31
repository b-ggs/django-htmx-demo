# Generated by Django 4.2.5 on 2023-09-17 13:48

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("price_cents", models.PositiveIntegerField()),
                ("image_url", models.URLField(default="https://placehold.co/600x400")),
            ],
        ),
    ]
