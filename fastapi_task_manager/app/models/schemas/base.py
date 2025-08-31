import datetime
import pydantic
from pydantic import field_serializer

from app.utils.formatters.datetime_formatter import format_datetime_into_isoformat
from app.utils.formatters.field_formatter import format_dict_key_to_camel_case


class BaseScheameModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        validate_assignment=True,
        alias_generator=format_dict_key_to_camel_case,
    )

    @field_serializer("*", when_used="unless-none")
    def serialize_datetime_fields(self, value, info):
        if isinstance(value, datetime.datetime):
            return format_datetime_into_isoformat(value)
        return value
