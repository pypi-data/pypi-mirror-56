#!/usr/bin/env python

import numbers


def convert_as_table_format(column_names, contents, is_headless=False, line_separator='\n', separator='|'):
    accumulation = []

    if not is_headless:
        table_header = convert_as_row_format(column_names)
        divider = prepare_divider(separator, len(column_names))
        accumulation.extend([table_header, divider])

    rows = [convert_as_row_format(row_items, separator) for row_items in contents]
    accumulation.extend(rows)
    return line_separator.join(accumulation)


def prepare_divider(separator, times):
    divider_tail = ' :----: {0}'.format(separator) * times
    return '{0}{1}'.format(separator, divider_tail)


def convert_as_row_format(items, separator='|'):
    margin_separator = ' {0} '.format(separator)
    body = margin_separator.join(beautify_text(item, separator) for item in items)
    return "{0} {1} {2}".format(separator, body, separator)


def beautify_text(text, separator):
    escaped_separator = '\{0}'.format(separator)
    return "{:,}".format(text) if isinstance(text, numbers.Number) else text.replace(separator, escaped_separator)
