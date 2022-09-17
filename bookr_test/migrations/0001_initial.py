# Generated by Django 4.1 on 2022-09-14 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='name of Publisher.', max_length=50)),
                ('website', models.URLField(help_text="Publisher's website.")),
                ('email', models.EmailField(help_text="Publisher's email address.", max_length=254)),
            ],
        ),
    ]
