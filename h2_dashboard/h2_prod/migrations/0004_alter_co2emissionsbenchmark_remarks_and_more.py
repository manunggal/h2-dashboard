# Generated by Django 4.2.7 on 2023-11-13 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("h2_prod", "0003_co2emissionsbenchmark_remarks_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="co2emissionsbenchmark",
            name="remarks",
            field=models.TextField(
                blank=True,
                help_text="Additional information about the benchmark data",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="electricityproductionbenchmark",
            name="remarks",
            field=models.TextField(
                blank=True,
                help_text="Additional information about the benchmark data",
                null=True,
            ),
        ),
    ]
