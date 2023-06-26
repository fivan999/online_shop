import csv
import datetime

import django.contrib.admin
import django.db.models
import django.http


def export_data_to_csv(
    model_admin: django.contrib.admin.ModelAdmin,
    request: django.http.HttpRequest,
    queryset: django.db.models.QuerySet,
) -> django.http.HttpResponse:
    """экспортируем данные модели в формат csv"""
    options = model_admin.model._meta
    content_disposition = f'attachment; filename="{options.verbose_name}.csv"'
    response = django.http.HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [
        field
        for field in options.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%Y.%m.%d')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_data_to_csv.short_description = 'Экспорт в csv'
