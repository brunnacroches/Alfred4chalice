from marshmallow import fields


class FilterFieldMixin:
    filter_type = "sqlalchemy.and_"

    def _deserialize(self, value, attr, data, **kwargs):
        value = super()._deserialize(value, attr, data, **kwargs)
        field_name = self.field_name or attr

        return {
            "model": self.model,
            "field_name": field_name,
            "op": self.op,
            "value": value,
            "filter_type": self.filter_type,
        }

    def __init__(self, model, op, field_name=None, *args, **kwargs):
        self.model = model
        self.op = op
        self.field_name = field_name
        super().__init__(*args, **kwargs)


class StringFilterField(FilterFieldMixin, fields.String):
    pass


class DateFilterField(FilterFieldMixin, fields.Date):
    pass


class ListFilterField(FilterFieldMixin, fields.List):
    def _deserialize(self, value, attr, data, **kwargs):
        if value == []:
            return None
        return super()._deserialize(value, attr, data, **kwargs)


class LogicalFilterField(ListFilterField):
    filter_type = "sqlalchemy.or_"
