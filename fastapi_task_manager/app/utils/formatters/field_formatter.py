def format_dict_key_to_camel_case(field_name: str):
    snake_format = field_name.lower().split("_")
    res = snake_format[0]
    for word in snake_format[1:]:
        res += word.capitalize()
    return res
