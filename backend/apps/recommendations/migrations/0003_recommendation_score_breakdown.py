from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recommendations", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="recommendation",
            name="score_breakdown",
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
