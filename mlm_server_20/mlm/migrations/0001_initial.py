# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MLMNode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(verbose_name='ID пользователя в Core')),
                ('referrer_id', models.BigIntegerField(blank=True, null=True, verbose_name='ID реферера')),
                ('position', models.CharField(choices=[('left', 'Слева'), ('center', 'Центр'), ('right', 'Справа')], default='left', max_length=10, verbose_name='Позиция')),
                ('status', models.CharField(default='participant', max_length=20, verbose_name='Статус')),
                ('rank', models.CharField(default='0', max_length=20, verbose_name='Ранг')),
                ('partners_count', models.IntegerField(default=0, verbose_name='Количество партнеров')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
            ],
            options={
                'verbose_name': 'MLM узел',
                'verbose_name_plural': 'MLM узлы',
            },
        ),
        migrations.CreateModel(
            name='Bonus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(verbose_name='ID пользователя')),
                ('referrer_id', models.BigIntegerField(verbose_name='ID реферера')),
                ('bonus_type', models.CharField(choices=[('yellow', 'Желтый бонус'), ('green', 'Зеленый бонус'), ('green_1', 'Зеленый бонус (1-й партнер)'), ('green_2', 'Зеленый бонус (2-й партнер)'), ('red', 'Красный бонус')], max_length=20, verbose_name='Тип бонуса')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма')),
                ('status', models.CharField(choices=[('pending', 'Ожидает'), ('sent', 'Отправлен'), ('failed', 'Ошибка')], default='pending', max_length=20, verbose_name='Статус')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
            ],
            options={
                'verbose_name': 'Бонус',
                'verbose_name_plural': 'Бонусы',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='mlmnode',
            index=models.Index(fields=['referrer_id', 'position'], name='mlm_mlmnode_referre_idx'),
        ),
        migrations.AddIndex(
            model_name='mlmnode',
            index=models.Index(fields=['user_id'], name='mlm_mlmnode_user_id_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='mlmnode',
            unique_together={('user_id', 'referrer_id')},
        ),
    ]

