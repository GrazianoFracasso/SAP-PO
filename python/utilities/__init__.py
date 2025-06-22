import inspect
myself = lambda: inspect.stack()[1][3]

# Convert XML to JSON using BeautifulSoup and a helper function
def xml_to_dict(element):
    # Recursively convert BeautifulSoup XML element to dict
    if not element.contents or all(isinstance(child, str) and not child.strip() for child in element.contents):
        return element.get_text(strip=True)
    result = {}
    for child in element.find_all(recursive=False):
        key = child.name
        value = xml_to_dict(child)
        if key in result:
            # If key already exists, convert to list
            if not isinstance(result[key], list):
                result[key] = [result[key]]
                result[key].append(value)
        else:
            result[key] = value
    return result