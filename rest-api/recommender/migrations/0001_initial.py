# Generated by Django 2.1.4 on 2018-12-11 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ModelTraining',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('independent_variables', models.TextField(blank=True, null=True)),
                ('dependent_variable', models.TextField(blank=True, null=True)),
                ('transformation', models.TextField(blank=True, null=True)),
                ('encode_cat_list', models.TextField(blank=True, null=True)),
                ('encode_date_list', models.TextField(blank=True, null=True)),
                ('drop_list', models.TextField(blank=True, null=True)),
                ('dummies', models.TextField(blank=True, null=True)),
                ('model_type', models.TextField(blank=True, null=True)),
                ('user_id', models.CharField(blank=True, max_length=256, null=True)),
                ('trained_date', models.DateTimeField(auto_now=True, null=True)),
                ('accuracy_r2', models.FloatField(blank=True, null=True)),
                ('accuracy_rmse', models.FloatField(blank=True, null=True)),
                ('model_file', models.TextField(blank=True, null=True)),
                ('test_json', models.TextField(blank=True, null=True)),
                ('scatter_plot', models.TextField(blank=True, null=True)),
            ],
        ),
    ]