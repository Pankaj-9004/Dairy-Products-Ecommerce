# Generated by Django 5.0.4 on 2024-06-01 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_payment_orderplaced'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='rezorpay_payment_id',
            new_name='razorpay_payment_id',
        ),
    ]