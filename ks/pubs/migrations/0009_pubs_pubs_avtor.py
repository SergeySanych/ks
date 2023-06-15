# Generated by Django 4.1.7 on 2023-06-07 06:17

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0007_avtors"),
        ("pubs", "0008_pubsstat"),
    ]

    operations = [
        migrations.AddField(
            model_name="pubs",
            name="pubs_avtor",
            field=modelcluster.fields.ParentalManyToManyField(
                blank=True, to="home.avtors"
            ),
        ),
    ]
