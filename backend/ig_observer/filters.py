from django.contrib.admin import SimpleListFilter


class JSONFieldFilter(SimpleListFilter):
    """
    """
    def __init__(self, *args, **kwargs):

        super(JSONFieldFilter, self).__init__(*args, **kwargs)

        assert hasattr(self,
                       'title'), ('Class {} missing "title" attribute'.format(
                           self.__class__.__name__))
        assert hasattr(self, 'parameter_name'), (
            'Class {} missing "parameter_name" attribute'.format(
                self.__class__.__name__))
        assert hasattr(self, 'json_field_name'), (
            'Class {} missing "json_field_name" attribute'.format(
                self.__class__.__name__))
        assert hasattr(self, 'json_field_property_name'), (
            'Class {} missing "json_field_property_name" attribute'.format(
                self.__class__.__name__))

    def lookups(self, request, model_admin):
        """
        # Improvemnt needed: if the size of jsonfield is large and there are lakhs of row
        """
        if self.json_field_property_name is None:
            return None
        elif self.field_value_set:
            field_value_set = self.field_value_set
        else:
            if '__' in self.json_field_property_name:  # NOTE: this will cover only one nested level
                keys = self.json_field_property_name.split('__')
                field_value_set = set(
                    data[keys[0]][keys[1]]
                    for data in model_admin.model.objects.values_list(
                        self.json_field_name, flat=True)
                    if keys is not None and data is not None)
            else:
                field_value_set = set(
                    data[self.json_field_property_name]
                    for data in model_admin.model.objects.values_list(
                        self.json_field_name, flat=True) if data is not None
                    and self.json_field_property_name in data)
        return [(v, v) for v in field_value_set]

    def queryset(self, request, queryset):
        if self.value():
            json_field_query = {
                "{}__{}".format(self.json_field_name, self.json_field_property_name):
                self.value()
            }
            return queryset.filter(**json_field_query)
        else:
            return queryset


class RacyFilter(JSONFieldFilter):
    title = 'Racy'  # for admin sidebar (above the filter options)
    parameter_name = 'jsonracy'  # Parameter for the filter that will be used in the URL query
    json_field_name = 'gvisionanalyse__analyse'
    json_field_property_name = 'safeSearchAnnotation__racy'  # property/field in json data
    field_value_set = [
        'VERY_LIKELY',
        'LIKELY',
        'POSSIBLE',
        'UNLIKELY',
        'VERY_UNLIKELY',
    ]
