import secrets
import time

import ckeditor_uploader.fields
import shop.managers
import sorl.thumbnail
import transliterate

import django.core.validators
import django.db.models
import django.urls
from django.utils.translation import gettext_lazy as _


def generate_image_path(obj: django.db.models.Model, filename: str) -> str:
    """генерируем файловый пусть к картинке"""
    filename = transliterate.translit(filename, 'ru', reversed=True)
    filename = (
        str(int(time.time()))
        + secrets.token_hex(nbytes=6)
        + filename[filename.rfind('.') :]
    )
    return f'shop/{obj.pk}/{filename}'


class Category(django.db.models.Model):
    """модель категории"""

    objects = shop.managers.CategoryManager()

    name = django.db.models.CharField(
        max_length=200, verbose_name=_('name'), help_text=_("Category's name")
    )
    slug = django.db.models.SlugField(
        max_length=200,
        verbose_name=_('slug'),
        help_text=_("Name's slug"),
        unique=True,
    )

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

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
        verbose_name=_('category'),
        help_text=_('Category to which product relates to'),
    )
    name = django.db.models.CharField(
        max_length=200, verbose_name=_('name'), help_text=_("Product's name")
    )
    slug = django.db.models.SlugField(
        max_length=200,
        verbose_name=_('slug'),
        help_text=_("Product's slug"),
        unique=True,
    )
    image = django.db.models.ImageField(
        verbose_name=_('image'),
        help_text=_("Product's image"),
        blank=True,
        upload_to=generate_image_path,
    )
    description = ckeditor_uploader.fields.RichTextUploadingField(
        help_text=_("Product's description"),
        verbose_name=_('description'),
        blank=True,
    )
    price = django.db.models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('price'),
        help_text=_("Product's price"),
        validators=[django.core.validators.MinValueValidator(0)],
    )
    available = django.db.models.BooleanField(
        default=True,
        verbose_name=_('available'),
        help_text=_('Whether product is available or not'),
    )
    created = django.db.models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created'),
        help_text=_('Creation time'),
    )
    updated = django.db.models.DateTimeField(
        auto_now=True,
        verbose_name=_('updated'),
        help_text=_('Update time'),
    )

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

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
