from django.db.models.fields import FieldDoesNotExist
from django.http import HttpResponse
import unicodecsv as csv


def export_to_csv(description='Export do pliku CSV ', filename='somefilename', fields=None, header=True):
    def action(modeladmin, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{filename}.csv"'.format(
            filename=filename,
        )
        list_display = fields or modeladmin.get_list_display(request)
        model = modeladmin.model
        lookup_opts = model._meta
        writer = csv.writer(response, encoding='utf-8')
        if header:
            row = []
            for field_name in list_display:
                try:
                    field = lookup_opts.get_field(field_name)
                    row.append(field.name)
                except FieldDoesNotExist:
                    if hasattr(modeladmin, field_name):
                        method = getattr(modeladmin, field_name)
                    else:
                        method = getattr(model, field_name)
                    row.append(getattr(method, 'short_description', None))
            writer.writerow(row)
        for user in queryset.all():
            row = []
            for field_name in list_display:
                try:
                    row.append(getattr(user, field_name))
                except AttributeError:
                    if hasattr(modeladmin, field_name):
                        method = getattr(modeladmin, field_name)
                    else:
                        method = getattr(model, field_name)
                    row.append(method(user))
            writer.writerow(row)
        return response
    action.short_description = description
    return action