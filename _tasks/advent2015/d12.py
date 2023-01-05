import json


def sum_json(j, ignore_str_value=None):
    if isinstance(j, list):
        return sum([sum_json(k, ignore_str_value=ignore_str_value) for k in j])
    elif isinstance(j, dict):
        str_values = set([value for value in j.values() if isinstance(value, str)])
        if ignore_str_value in str_values:
            return 0
        return sum([sum_json(k, ignore_str_value=ignore_str_value) for k in j.values()])
    elif isinstance(j, int):
        return j
    elif isinstance(j, str):
        return 0
    else:
        assert False


with open('d12.txt') as f:
    data = json.load(f)

print(sum_json(data))
print(sum_json(data, ignore_str_value='red'))