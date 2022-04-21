# Generated by Django 4.0.2 on 2022-03-22 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_project_date_ending_project_date_start_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='project',
            name='category',
            field=models.ForeignKey(default='Uncategorised', on_delete=django.db.models.deletion.CASCADE, to='projects.category'),
        ),
    ]
