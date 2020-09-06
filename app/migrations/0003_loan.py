# Generated by Django 2.2.4 on 2020-09-06 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_borrower'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to='app.Borrower')),
                ('lender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to='app.Lender')),
            ],
        ),
    ]
