from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FunctionLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='name')),
                ('input_values', models.CharField(max_length=50, verbose_name='input_values')),
                ('execution_time', models.TimeField(verbose_name='execution_time')),
            ],
            options={
                'verbose_name': 'functionlog',
                'verbose_name_plural': 'functionlogs',
            },
        ),
    ]
