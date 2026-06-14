from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("places", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="place",
            name="source",
            field=models.CharField(default="internal", db_index=True, max_length=20),
        ),
        migrations.AddField(
            model_name="place",
            name="external_id",
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="place",
            name="last_synced_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
