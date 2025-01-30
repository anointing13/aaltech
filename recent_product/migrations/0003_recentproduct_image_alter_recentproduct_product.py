# Generated by Django 4.2.16 on 2024-11-07 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_alter_product_is_hidden'),
        ('recent_product', '0002_alter_recentproduct_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='recentproduct',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='special_offer_images/'),
        ),
        migrations.AlterField(
            model_name='recentproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recent_product', to='product.product'),
        ),
    ]
