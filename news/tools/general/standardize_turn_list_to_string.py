def list_to_string(item_element):
    if item_element:
        if isinstance(item_element, list):
            item_element = item_element[0]
    else:
        item_element = ""
    return item_element
