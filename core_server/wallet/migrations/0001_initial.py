# Generated manually for Railway deployment

from django.conf import settings
from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Баланс')),
                ('total_earned', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Всего заработано')),
                ('total_withdrawn', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Всего выведено')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('user', models.OneToOneField(on_delete=models.CASCADE, related_name='wallet', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Кошелек',
                'verbose_name_plural': 'Кошельки',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма')),
                ('transaction_type', models.CharField(choices=[('deposit', 'Пополнение'), ('withdrawal', 'Вывод'), ('bonus', 'Бонус'), ('referral_bonus', 'Реферальный бонус'), ('mlm_bonus', 'MLM бонус'), ('payment', 'Оплата')], max_length=20, verbose_name='Тип')),
                ('status', models.CharField(choices=[('pending', 'Ожидает'), ('completed', 'Завершена'), ('failed', 'Ошибка'), ('cancelled', 'Отменена')], default='pending', max_length=20, verbose_name='Статус')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('mlm_server_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='MLM сервер')),
                ('reference_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='ID ссылки')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('wallet', models.ForeignKey(on_delete=models.CASCADE, related_name='transactions', to='wallet.wallet', verbose_name='Кошелек')),
            ],
            options={
                'verbose_name': 'Транзакция',
                'verbose_name_plural': 'Транзакции',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='WithdrawalRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Сумма')),
                ('status', models.CharField(choices=[('pending', 'Ожидает'), ('processing', 'Обрабатывается'), ('completed', 'Завершен'), ('rejected', 'Отклонен')], default='pending', max_length=20, verbose_name='Статус')),
                ('payment_method', models.CharField(max_length=50, verbose_name='Способ оплаты')),
                ('payment_details', models.JSONField(default=dict, verbose_name='Детали оплаты')),
                ('admin_notes', models.TextField(blank=True, verbose_name='Заметки администратора')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('wallet', models.ForeignKey(on_delete=models.CASCADE, related_name='withdrawal_requests', to='wallet.wallet', verbose_name='Кошелек')),
            ],
            options={
                'verbose_name': 'Запрос на вывод',
                'verbose_name_plural': 'Запросы на вывод',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['wallet', 'created_at'], name='wallet_tran_wallet__idx'),
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['transaction_type', 'status'], name='wallet_tran_transac_idx'),
        ),
    ]

