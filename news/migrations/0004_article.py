# Generated by Django 5.1.3 on 2024-11-16 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_news_summary_alter_news_image_alter_news_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
            ],
        ),
    ]
