# Generated by Django 3.2.7 on 2022-10-13 17:13

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('custom_users', '0006_auto_20221008_0109'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='current_enrolled_type',
            field=models.CharField(choices=[('School', 'School'), ('College', 'College')], default='School', max_length=20),
        ),
        migrations.CreateModel(
            name='StudentChangeRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, default='', max_length=50)),
                ('last_name', models.CharField(blank=True, default='', max_length=50)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Transgender'), ('Other', 'Other')], default='Male', max_length=20)),
                ('address_line', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('pin_code', models.CharField(max_length=6)),
                ('township', models.CharField(help_text='Taluka/Tehsil', max_length=50)),
                ('district', models.CharField(max_length=50)),
                ('state', models.CharField(choices=[('AP', 'Andhra Pradesh'), ('AR', 'Arunachal Pradesh'), ('AS', 'Assam'), ('BR', 'Bihar'), ('CG', 'Chhattisgarh'), ('GA', 'Goa'), ('GJ', 'Gujarat'), ('HR', 'Haryana'), ('HP', 'Himachal Pradesh'), ('JK', 'Jammu and Kashmir'), ('JH', 'Jharkhand'), ('KA', 'Karnataka'), ('KL', 'Kerala'), ('MP', 'Madhya Pradesh'), ('MH', 'Maharashtra'), ('MN', 'Manipur'), ('ML', 'Meghalaya'), ('MZ', 'Mizoram'), ('NL', 'Nagaland'), ('OR', 'Odisha'), ('PB', 'Punjab'), ('RJ', 'Rajasthan'), ('SK', 'Sikkim'), ('TN', 'Tamil Nadu'), ('TG', 'Telangana'), ('TR', 'Tripura'), ('UK', 'Uttarakhand'), ('UP', 'Uttar Pradesh'), ('WB', 'West Bengal'), ('AN', 'Andaman and Nicobar Islands'), ('CH', 'Chandigarh'), ('DN', 'Dadra and Nagar Haveli'), ('DD', 'Daman and Diu'), ('DL', 'Delhi'), ('LD', 'Lakshadweep'), ('PY', 'Puducherry')], max_length=5)),
                ('phone', models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(message='Number should only contains integers.', regex='^[0-9]*$')])),
                ('father_phone', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Number should only contains integers.', regex='^[0-9]*$')])),
                ('mother_phone', models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(message='Number should only contains integers.', regex='^[0-9]*$')])),
                ('email', models.EmailField(max_length=254, null=True)),
                ('date_of_birth', models.DateField()),
                ('aadhaar_id_number', models.CharField(blank=True, max_length=12, null=True)),
                ('mother_tongue', models.CharField(blank=True, max_length=50, null=True)),
                ('father_name', models.CharField(blank=True, max_length=50, null=True)),
                ('mother_name', models.CharField(blank=True, max_length=50, null=True)),
                ('father_aadhaar_id_number', models.CharField(blank=True, max_length=12, null=True)),
                ('mother_aadhaar_id_number', models.CharField(blank=True, max_length=12, null=True)),
                ('father_occupation', models.CharField(default='Not Specified', max_length=50)),
                ('mother_occuption', models.CharField(default='Housewife', max_length=50)),
                ('address_type', models.CharField(choices=[('Urban', 'Urban'), ('Rural', 'Rural')], default='Rural', max_length=20)),
                ('religion', models.CharField(blank=True, max_length=50, null=True)),
                ('caste', models.CharField(choices=[('General', 'General'), ('OBC', 'OBC'), ('SC', 'SC'), ('ST', 'ST'), ('General-EWS', 'General-EWS')], default='General', max_length=20)),
                ('belong_to_bpl', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='custom_users.student')),
            ],
        ),
    ]
