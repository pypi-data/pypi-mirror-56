def find_item(root_item, field_spec):
    tokens = field_spec.split(".")
    cursor = root_item
    for tokenName in tokens:
        if tokenName[0] == "[":
            assert isinstance(cursor, list)
            tokenName = tokenName.strip("[]]")
            search_key, search_value = tokenName.split("=")
            match_item = [x for x in cursor if getattr(x, search_key) == search_value]
            if match_item:
                cursor = match_item[0]
            else:
                return None
        else:
            cursor = getattr(cursor, tokenName)
    return cursor


def table_from_list(data, fields):
    input_data = data.items
    response_data = []
    response_data.append(fields.keys())
    for list_item in input_data:
        row = []
        for field_mame, field_spec in fields.items():
            value = find_item(list_item, field_spec)
            row.append(value)
        response_data.append(row)
    return response_data
