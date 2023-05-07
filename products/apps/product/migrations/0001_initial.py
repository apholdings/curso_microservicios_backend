# Generated by Django 3.2.16 on 2023-05-05 15:50

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shipping', '0001_initial'),
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('position_id', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('hex', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('stock', models.IntegerField(blank=True, null=True)),
                ('inStock', models.BooleanField(default=True)),
                ('author', models.UUIDField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('position_id', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('body', models.CharField(max_length=1200)),
                ('author', models.UUIDField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('position_id', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=60, null=True)),
                ('file', models.ImageField(upload_to='marketplace/products')),
                ('author', models.UUIDField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('position_id', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='marketplace/materials')),
                ('inStock', models.BooleanField(default=True)),
                ('stock', models.IntegerField(blank=True, null=True)),
                ('author', models.UUIDField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('token_id', models.TextField(unique=True)),
                ('nft_address', models.CharField(blank=True, default=0, max_length=256, null=True)),
                ('author', models.UUIDField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=60, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('short_description', models.TextField(blank=True, max_length=125, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('keywords', models.CharField(blank=True, max_length=255, null=True)),
                ('slug', models.SlugField(default=uuid.uuid4, unique=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('compare_price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('onSale', models.BooleanField(default=False)),
                ('stock', models.IntegerField(default=0)),
                ('best_seller', models.BooleanField(default=False)),
                ('business_activity', models.CharField(default='B2C', max_length=255)),
                ('type', models.CharField(default='Brand Product', max_length=255)),
                ('condition', models.CharField(choices=[('new', 'New'), ('used', 'Used'), ('broken', 'Broken')], default='new', max_length=255)),
                ('warranty', models.CharField(default='0', max_length=255)),
                ('packaging', models.CharField(choices=[('normal', 'Normal'), ('gift', 'Gift')], default='normal', max_length=255)),
                ('views', models.IntegerField(blank=True, default=0)),
                ('clicks', models.IntegerField(blank=True, default=0, null=True)),
                ('impressions', models.IntegerField(blank=True, default=0, null=True)),
                ('clickThroughRate', models.FloatField(blank=True, default=0, null=True)),
                ('purchases', models.IntegerField(blank=True, default=0, null=True)),
                ('conversion_rate', models.FloatField(blank=True, default=0, null=True)),
                ('avg_time_on_page', models.FloatField(blank=True, default=0, null=True)),
                ('sold', models.IntegerField(blank=True, default=0, null=True)),
                ('income_earned', models.PositiveIntegerField(blank=True, default=0)),
                ('rating_no', models.IntegerField(blank=True, default=0, null=True)),
                ('avgRating', models.IntegerField(blank=True, default=0)),
                ('likes', models.IntegerField(blank=True, default=0)),
                ('totalRevenue', models.IntegerField(blank=True, default=0)),
                ('returns', models.IntegerField(blank=True, default=0)),
                ('refunds', models.IntegerField(blank=True, default=0)),
                ('manufacturer', models.CharField(blank=True, max_length=1200, null=True)),
                ('target_audience_bool', models.BooleanField(default=False)),
                ('features_bool', models.BooleanField(default=False)),
                ('supply_chain_bool', models.BooleanField(default=False)),
                ('delivery_bool', models.BooleanField(default=False)),
                ('warehousing_bool', models.BooleanField(default=False)),
                ('value_proposition_bool', models.BooleanField(default=False)),
                ('marketing_strategy_bool', models.BooleanField(default=False)),
                ('product_details_bool', models.BooleanField(default=False)),
                ('accessibility_bool', models.BooleanField(default=False)),
                ('documentation_bool', models.BooleanField(default=False)),
                ('landing_page_bool', models.BooleanField(default=False)),
                ('pricing_bool', models.BooleanField(default=False)),
                ('promotions_bool', models.BooleanField(default=False)),
                ('shipping_bool', models.BooleanField(default=False)),
                ('messages_bool', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='category.category')),
                ('colors', models.ManyToManyField(blank=True, related_name='productColors', to='product.Color')),
                ('details', models.ManyToManyField(blank=True, related_name='productDetails', to='product.Details')),
                ('images', models.ManyToManyField(blank=True, related_name='product_images', to='product.Image')),
                ('materials', models.ManyToManyField(blank=True, related_name='productMaterial', to='product.Material')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('rate_number', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('user', models.UUIDField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WhoIsFor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('position_id', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('user', models.UUIDField(blank=True, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='whoisfor_belongs_to_product', to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='Weight',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('position_id', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('inStock', models.BooleanField(default=True)),
                ('stock', models.IntegerField(blank=True, null=True)),
                ('author', models.UUIDField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='weight_belongs_to_product', to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='ViewCount',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ip_address', models.CharField(max_length=255)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_view_count', to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('position_id', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=60, null=True)),
                ('file', models.FileField(upload_to='marketplace/products')),
                ('author', models.UUIDField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_video_attached', to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('position_id', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('inStock', models.BooleanField(default=True)),
                ('stock', models.IntegerField(blank=True, null=True)),
                ('author', models.UUIDField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='size_belongs_to_product', to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='Sellers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.UUIDField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=256, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productSeller', to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='Requisite',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('position_id', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('user', models.UUIDField(blank=True, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requisite_belongs_to_product', to='product.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.ManyToManyField(blank=True, to='product.Rate'),
        ),
        migrations.AddField(
            model_name='product',
            name='sellers',
            field=models.ManyToManyField(blank=True, related_name='courseSellers', to='product.Sellers'),
        ),
        migrations.AddField(
            model_name='product',
            name='shipping',
            field=models.ManyToManyField(blank=True, to='shipping.Shipping'),
        ),
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(blank=True, related_name='productSizes', to='product.Size'),
        ),
        migrations.AddField(
            model_name='product',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sub_category_products', to='category.category'),
        ),
        migrations.AddField(
            model_name='product',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='topic_products', to='category.category'),
        ),
        migrations.AddField(
            model_name='product',
            name='videos',
            field=models.ManyToManyField(blank=True, related_name='product_videos', to='product.Video'),
        ),
        migrations.AddField(
            model_name='product',
            name='weights',
            field=models.ManyToManyField(blank=True, related_name='productweight', to='product.Weight'),
        ),
        migrations.AddField(
            model_name='material',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='material_belongs_to_product', to='product.product'),
        ),
        migrations.AddField(
            model_name='image',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_image_attached', to='product.product'),
        ),
        migrations.AddField(
            model_name='details',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detail_belongs_to_product', to='product.product'),
        ),
        migrations.AddField(
            model_name='color',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='color_belongs_to_product', to='product.product'),
        ),
        migrations.CreateModel(
            name='Benefits',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('position_id', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('user', models.UUIDField(blank=True, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='benefits_belongs_to_product', to='product.product')),
            ],
        ),
    ]