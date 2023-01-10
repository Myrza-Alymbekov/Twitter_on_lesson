# Generated by Django 3.2 on 2023-01-10 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.comment')),
                ('profile', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='accounts.profile')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.statustype')),
            ],
            options={
                'unique_together': {('comment', 'profile')},
            },
        ),
    ]
