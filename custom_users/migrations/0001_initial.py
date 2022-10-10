# Generated by Django 3.2.7 on 2022-10-05 18:43

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('entities', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.CharField(blank=True, max_length=10, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Transgender'), ('Other', 'Other')], default='Male', max_length=20)),
                ('address_line', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('pin_code', models.CharField(max_length=6)),
                ('township', models.CharField(help_text='Taluka/Tehsil', max_length=50)),
                ('district', models.CharField(max_length=50)),
                ('state', models.CharField(choices=[('AP', 'Andhra Pradesh'), ('AR', 'Arunachal Pradesh'), ('AS', 'Assam'), ('BR', 'Bihar'), ('CG', 'Chhattisgarh'), ('GA', 'Goa'), ('GJ', 'Gujarat'), ('HR', 'Haryana'), ('HP', 'Himachal Pradesh'), ('JK', 'Jammu and Kashmir'), ('JH', 'Jharkhand'), ('KA', 'Karnataka'), ('KL', 'Kerala'), ('MP', 'Madhya Pradesh'), ('MH', 'Maharashtra'), ('MN', 'Manipur'), ('ML', 'Meghalaya'), ('MZ', 'Mizoram'), ('NL', 'Nagaland'), ('OR', 'Odisha'), ('PB', 'Punjab'), ('RJ', 'Rajasthan'), ('SK', 'Sikkim'), ('TN', 'Tamil Nadu'), ('TG', 'Telangana'), ('TR', 'Tripura'), ('UK', 'Uttarakhand'), ('UP', 'Uttar Pradesh'), ('WB', 'West Bengal'), ('AN', 'Andaman and Nicobar Islands'), ('CH', 'Chandigarh'), ('DN', 'Dadra and Nagar Haveli'), ('DD', 'Daman and Diu'), ('DL', 'Delhi'), ('LD', 'Lakshadweep'), ('PY', 'Puducherry')], max_length=5)),
                ('phone', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Number should only contains integers.', regex='^[0-9]*$')])),
                ('father_phone', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Number should only contains integers.', regex='^[0-9]*$')])),
                ('mother_phone', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Number should only contains integers.', regex='^[0-9]*$')])),
                ('registered_year', models.IntegerField(validators=[django.core.validators.MinValueValidator(2012, 'Can only add students registered after 2012')])),
                ('date_of_birth', models.DateField()),
                ('aadhaar_id_number', models.CharField(blank=True, max_length=12, null=True)),
                ('mother_tongue', models.CharField(blank=True, max_length=50, null=True)),
                ('father_name', models.CharField(blank=True, max_length=50, null=True)),
                ('mother_name', models.CharField(blank=True, max_length=50, null=True)),
                ('father_aadhaar_id_number', models.CharField(blank=True, max_length=12, null=True)),
                ('mother_aaadhaar_id_number', models.CharField(blank=True, max_length=12, null=True)),
                ('father_occupation', models.CharField(default='Not Specified', max_length=50)),
                ('mother_occuption', models.CharField(default='Housewife', max_length=50)),
                ('age', models.IntegerField(validators=[django.core.validators.MinValueValidator(4, 'Can only add students above 4 years of age')])),
                ('is_age_appropriate', models.BooleanField(default=False)),
                ('age_appropiation_reason', models.TextField(blank=True, null=True)),
                ('address_type', models.CharField(choices=[('Urban', 'Urban'), ('Rural', 'Rural')], default='Rural', max_length=20)),
                ('religion', models.CharField(blank=True, max_length=50, null=True)),
                ('cast', models.CharField(choices=[('General', 'General'), ('OBC', 'OBC'), ('SC', 'SC'), ('ST', 'ST'), ('General-EWS', 'General-EWS')], default='General', max_length=20)),
                ('belong_to_bpl', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='app_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InstituteAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institute_admin', to='entities.institute')),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='institute_admin', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EducationDepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='education_department', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]