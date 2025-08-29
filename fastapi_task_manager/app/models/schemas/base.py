import datetime
import pydantic

from app.utils.formatters.datetime_formatter import format_datetime_into_isoformat
from app.utils.formatters.field_formatter import format_dict_key_to_camel_case


class BaseScheameModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        validate_assignment=True,
        json_encoders={datetime.datetime: format_datetime_into_isoformat},
        alias_generator=format_dict_key_to_camel_case,
    )
