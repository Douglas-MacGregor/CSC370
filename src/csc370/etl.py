import csv


def read_rows(csv_path):
    with open(csv_path, newline="", encoding="utf-8") as f:
        yield from csv.DictReader(f)


def load_template(path):
    with open(path, encoding="utf-8") as f:
        return f.read().strip()


def sql_value(v):
    if v is None or v == "":
        return "NULL"
    try:
        float(v)
        return str(v)
    except (TypeError, ValueError):
        escaped = str(v).replace("\\", "\\\\").replace("'", "\\'")
        return f"'{escaped}'"


def render_template(template, values):
    parts = template.split("?")
    if len(parts) - 1 != len(values):
        raise ValueError(f"template has {len(parts) - 1} placeholders, got {len(values)} values")
    rendered = parts[0]
    for value, part in zip(values, parts[1:]):
        rendered += sql_value(value) + part
    return rendered
