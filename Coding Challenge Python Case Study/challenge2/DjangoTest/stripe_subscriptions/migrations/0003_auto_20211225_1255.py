# Generated by Django 2.2 on 2021-12-25 12:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_subscriptions', '0002_stripecustomer_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stripecustomer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL),
        ),
    ]
