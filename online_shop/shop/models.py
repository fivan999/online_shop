import time

import ckeditor_uploader.fields
import shop.managers
import sorl.thumbnail
import transliterate

import django.core.validators
import django.db.models
import django.urls


def generate_image_path(obj: django.db.models.Model, filename: str) -> str:
    """генерируем файловый пусть к картинке"""
    filename = transliterate.translit(filename, 'ru', reversed=True)
    filename = (
        filename[: filename.rfind('.')]
        + str(int(time.time()))
        + filename[filename.rfind('.') :]
    )
    return f'shop/{obj.pk}/{filename}'


class Category(django.db.models.Model):
    """модель категории"""

    name = django.db.models.CharField(
        max_length=200, verbose_name='имя', help_text='Имя категории'
    )
    slug = django.db.models.SlugField(
        max_length=200,
        verbose_name='слаг',
        help_text='Слаг имени',
        unique=True,
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self) -> str:
        """строковое представление"""
        return self.name[:15]

    def get_absolute_url(self) -> str:
        return django.urls.reverse(
            'shop:products_by_category', kwargs={'category_pk': self.pk}
        )


class Product(django.db.models.Model):
    """модель продукта"""

    objects = shop.managers.ProductManager()

    category = django.db.models.ForeignKey(
        to=Category,
        related_name='products',
        on_delete=django.db.models.CASCADE,
        verbose_name='категория',
        help_text='Категория, к которой относится товар',
    )
    name = django.db.models.CharField(
        max_length=200, verbose_name='имя', help_text='Имя продукта'
    )
    slug = django.db.models.SlugField(
        max_length=200,
        verbose_name='слаг',
        help_text='Слаг для продукта',
        unique=True,
    )
    image = django.db.models.ImageField(
        verbose_name='картинка',
        help_text='Картинка продукта',
        blank=True,
        upload_to=generate_image_path,
    )
    description = ckeditor_uploader.fields.RichTextUploadingField(
        help_text='Описание продукта', verbose_name='описание', blank=True
    )
    price = django.db.models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='цена',
        help_text='Цена продукта',
        validators=[django.core.validators.MinValueValidator(0)],
    )
    available = django.db.models.BooleanField(
        default=True, verbose_name='доступен', help_text='Доступен ли продукт'
    )
    created = django.db.models.DateTimeField(
        auto_now_add=True, verbose_name='создан', help_text='Время создания'
    )
    updated = django.db.models.DateTimeField(
        auto_now=True, verbose_name='обновлен', help_text='Время обновления'
    )

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    def __str__(self) -> str:
        """строковое представление"""
        return self.name[:15]

    def get_absolute_url(self) -> str:
        return django.urls.reverse(
            'shop:product', kwargs={'product_pk': self.pk}
        )

    def get_image_300x300(self):
        """получаем миниатюру изображения"""
        return sorl.thumbnail.get_thumbnail(
            self.image, '300x300', crop='center', quality=70
        )
