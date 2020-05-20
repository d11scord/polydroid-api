def list_equals(first, second):
    is_equals = True
    if len(first) != len(second):
        return False
    else:
        for element_first, element_second in zip(first, second):
            if not element_first.equals(element_second):
                is_equals = False
    return is_equals


def list_to_json(objects):
    json = '['
    for obj in objects:
        json = json+obj.to_json()
    json = json+']'
    return json
