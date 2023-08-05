from exex_cli.util import array_dimensions

import json


def to_strings(values):
    outer_dim, inner_dim = array_dimensions(values)

    if outer_dim == 0 and inner_dim == 0:
        return str(values)
    elif inner_dim == 0:
        return list(map(str, values))
    else:
        return [list(map(str, row)) for row in values]


def to_csv(values, delimiter=",", line_separator="\n"):
    outer_dim, inner_dim = array_dimensions(values)

    if outer_dim == 0 and inner_dim == 0:
        return values
    elif inner_dim == 0:
        return line_separator.join(to_strings(values))
    else:
        return line_separator.join(delimiter.join(to_strings(row)) for row in values)


def to_json(values):
    return json.dumps(values, indent=2)
