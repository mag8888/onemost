# Generated manually for Railway deployment

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('telegram_id', models.BigIntegerField(blank=True, null=True, unique=True, verbose_name='Telegram ID')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Телефон')),
                ('is_partner', models.BooleanField(default=False, verbose_name='Партнер')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('mlm_statuses', models.JSONField(blank=True, default=dict, verbose_name='MLM статусы')),
                ('mlm_ranks', models.JSONField(blank=True, default=dict, verbose_name='MLM ранги')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ['-created_at'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ReferralLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mlm_server_id', models.CharField(max_length=100, verbose_name='MLM сервер')),
                ('referral_code', models.CharField(max_length=50, unique=True, verbose_name='Реферальный код')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('user', models.ForeignKey(on_delete=models.CASCADE, related_name='referral_links', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Реферальная ссылка',
                'verbose_name_plural': 'Реферальные ссылки',
                'unique_together': {('user', 'mlm_server_id')},
            },
        ),
        migrations.CreateModel(
            name='ReferralRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mlm_server_id', models.CharField(max_length=100, verbose_name='MLM сервер')),
                ('level', models.IntegerField(default=1, verbose_name='Уровень')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('referrer', models.ForeignKey(on_delete=models.CASCADE, related_name='referrals_made', to=settings.AUTH_USER_MODEL, verbose_name='Реферер')),
                ('user', models.ForeignKey(on_delete=models.CASCADE, related_name='referrals', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Реферальная связь',
                'verbose_name_plural': 'Реферальные связи',
                'unique_together': {('user', 'mlm_server_id')},
            },
        ),
        migrations.AddIndex(
            model_name='referralrelation',
            index=models.Index(fields=['referrer', 'mlm_server_id'], name='users_refer_referre_idx'),
        ),
        migrations.AddIndex(
            model_name='referralrelation',
            index=models.Index(fields=['user', 'mlm_server_id'], name='users_refer_user_id_idx'),
        ),
    ]
