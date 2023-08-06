from utflib.table_chars import Corners, Horizontals, Verticals, Middles
from styles import Style
from sty import fg, bg, ef, rs


# Width is defined as the width INSIDE the borders. Padding will take away from available width.

##################################
# Table line wrappers
##################################
def table_top_line(*, width, style='thin', column_widths=None, column_notches=True):

    if column_widths is not None and column_notches:
        subline = table_top_subline_notched(width=width, style=style, column_widths=column_widths)
    else:
        subline = table_top_subline_flat(width=width, style=style)

    line = f"{Style.char_at('top_left', style)}{subline}{Style.char_at('top_right', style)}"
    return line

def table_middle_line(*, width, style='thin', column_widths=None, column_notches_top=True, column_notches_bottom=True):

    if column_widths is not None and (column_notches_top or column_notches_bottom):
        subline = table_middle_subline_notched(
            width=width, 
            style=style, 
            column_widths=column_widths, 
            column_notches_top=column_notches_top, 
            column_notches_bottom=column_notches_bottom
        )
    else:
        subline = table_middle_subline_flat(width=width, style=style)

    line = f"{Style.char_at('vertical_notch_left', style)}{subline}{Style.char_at('vertical_notch_right', style)}"
    return line

def table_bottom_line(*, width, style='thin', column_widths=None, column_notches=True):

    if column_widths is not None and column_notches:
        subline = table_bottom_subline_notched(width=width, style=style, column_widths=column_widths)
    else:
        subline = table_bottom_subline_flat(width=width, style=style)

    line = f"{Style.char_at('bottom_left', style)}{subline}{Style.char_at('bottom_right', style)}"
    return line

def table_value_line(*, width, style='thin', column_widths, column_vals, column_styles=[], outer_borders=True, inner_borders=True, align='left', line_padding_left=0, line_padding_right=0, cell_padding_left=0, cell_padding_right=0, indent_str='', indent_padding=0):
    left_border_char = Style.char_at('vertical_left', style) if outer_borders else ' '
    right_border_char = Style.char_at('vertical_right', style) if outer_borders else ' '
    inner_border_char = Style.char_at('vertical_middle', style) if inner_borders else ' '

    line_padding_total = line_padding_left + line_padding_right + indent_padding + len(indent_str)

    subline = inner_line_values_notched_subbed(
        width=width - line_padding_total, 
        style=style, 
        column_widths=column_widths, 
        column_vals=column_vals,
        column_styles=column_styles,
        fill_char=' ', 
        col_divider=inner_border_char,
        align=align
    )

    line = f"{left_border_char}{' ' * line_padding_left}{indent_str}{' ' * indent_padding}{subline}{' ' * line_padding_right}{right_border_char}"
    return line

def table_filler_line(*, width, style='thin', outer_borders=True):
    left_border_char = Style.char_at('vertical_left', style) if outer_borders else ' '
    right_border_char = Style.char_at('vertical_right', style) if outer_borders else ' '

    subline = inner_line_filled_notched_subbed(
        width=width, 
        style=style, 
        column_widths=[], 
        fill_char=' ', 
        col_divider=None
    )

    line = f"{left_border_char}{subline}{right_border_char}"
    return line

##################################
# Table top builders
##################################
def table_top_subline_flat(*, width, style):
    return inner_line_filled_notched_subbed(
        width=width, 
        style=style, 
        column_widths=[], 
        fill_char=Style.char_at('horizontal_top', style), 
        col_divider=None
    )

def table_top_subline_notched(*, width, style, column_widths):
    return inner_line_filled_notched_subbed(
        width=width, 
        style=style, 
        column_widths=column_widths, 
        fill_char=Style.char_at('horizontal_top', style), 
        col_divider=Style.char_at('horizontal_notch_top', style)
    )

##################################
# Table middle builders
##################################
def table_middle_subline_flat(*, width, style):
    return inner_line_filled_notched_subbed(
        width=width, 
        style=style, 
        column_widths=[], 
        fill_char=Style.char_at('horizontal_middle', style), 
        col_divider=None
    )

def table_middle_subline_notched(*, width, style, column_widths, column_notches_top, column_notches_bottom):
    divider_char = Middles.MIDDLE_THIN

    if column_notches_top and column_notches_bottom:
        divider_char = Style.char_at('middle', style)
    elif column_notches_top and not column_notches_bottom:
        divider_char = Style.char_at('horizontal_notch_bottom', style)
    elif not column_notches_top and column_notches_bottom:
        divider_char = Style.char_at('horizontal_notch_top', style)
    elif not column_notches_top and not column_notches_bottom:
        divider_char = Style.char_at('horizontal_middle', style)


    return inner_line_filled_notched_subbed(
        width=width, 
        style=style, 
        column_widths=column_widths, 
        fill_char=Style.char_at('horizontal_middle', style),
        col_divider=divider_char
    )

##################################
# Table bottom builders
##################################
def table_bottom_subline_flat(*, width, style):
    return inner_line_filled_notched_subbed(
        width=width, 
        style=style, 
        column_widths=[], 
        fill_char=Style.char_at('horizontal_bottom', style), 
        col_divider=None
    )

def table_bottom_subline_notched(*, width, style, column_widths):
    return inner_line_filled_notched_subbed(
        width=width, 
        style=style, 
        column_widths=column_widths, 
        fill_char=Style.char_at('horizontal_bottom', style), 
        col_divider=Style.char_at('horizontal_notch_bottom', style)
    )

##################################
# Utilities
##################################
def inner_line_filled_notched_subbed(*, width, style, column_widths, fill_char, col_divider):
    # Little safety here in case col_divider is none, but col_widths are passed. Basically we 
    # do nothing special in the header if there are no dividers.
    if col_divider is None:
        column_widths = []

    line = ""

    for column in column_widths:

        # If a column width would cause us to go over the allowed length we stop adding notches.
        # I wouldn't expect a table to ever get into this situation - maybe we use a ... or squiggle
        if len(line) + column + 1 > width:
            break

        line += (fill_char * column) + col_divider

    if len(line) < width:
        line += fill_char * (width - len(line))

    return line

def inner_line_values_notched_subbed(*, width, style, column_widths, column_vals, column_styles=[], col_divider, fill_char=' ', align='left'):
    num_columns = len(column_widths)
    num_vals = len(column_vals)

    if not num_columns >= num_vals - 1:
        raise ValueError()

    if num_columns == num_vals - 1:
        column_widths.append(max(width - sum(column_widths) - num_vals + 1, 0))

    line = ""

    for index, column_width in enumerate(column_widths):
        column_val = column_vals[index] if index < num_vals else ''
        column_style = column_styles[index] if index < len(column_styles) else 'default'

        # THIS IS A BUG
        # - Doing styling before this counts those characters as values. So doing 0:column_width will
        # - cut off "invisible" characters
        column_text = column_val if len(column_val) <= column_width else column_val[0:column_width]

        if align == 'center':
            column_text = column_text.center(column_width)
        elif align == 'right':
            column_text = column_text.rjust(column_width)
        else:
            column_text = column_text.ljust(column_width)

        if column_style == 'invert':
            line += bg.white + fg.black + column_text + rs.all
        else:
            line += column_text

        if index != num_columns:
            line += col_divider

    if len(line) < width:
        line += ''.ljust(width - len(line))

    return line

if __name__ == '__main__':
    print("\n----- Outer Border (only) Table -----")
    print(table_top_line(width=75, column_notches=False, style='filled'))
    print(table_value_line(width=75, column_widths=[8, 15], column_vals=['ID', 'TITLE', 'DESCRIPTION'], align='left', inner_borders=False, style='filled'))
    # print(table_middle_line(width=75, column_notches_top=False, column_notches_bottom=False))
    print(table_value_line(width=75, column_widths=[8, 15], column_vals=['00001', 'value title', 'This is a large description of something that'], align='left', inner_borders=False))
    print(table_value_line(width=75, column_widths=[5, 15], column_vals=['', '', 'might continue to spill over onto the next line.'], align='left', inner_borders=False, indent_str=f"{Verticals.VERT_THIN}", indent_padding=1, line_padding_left=1))
    print(table_value_line(width=75, column_widths=[5, 15], column_vals=['', '', ''], align='left', inner_borders=False, indent_str=f"{Verticals.VERT_THIN}", indent_padding=1, line_padding_left=1))
    print(table_value_line(width=75, column_widths=[], column_vals=['This is a sub-value with a padding/indent character.'], align='left', inner_borders=False, indent_str=f"{Verticals.VERT_DASH_RIGHT_THIN}{Horizontals.HORIZ_THIN}", indent_padding=1, line_padding_left=1))
    print(table_value_line(width=75, column_widths=[6], column_vals=['TAG', 'This is another sub-value with a padding/indent character.'], align='left', inner_borders=False, indent_str=f"{Corners.BOTTOM_LEFT_THIN}{Horizontals.HORIZ_THIN}", indent_padding=1, line_padding_left=1))
    print(table_value_line(width=75, column_widths=[], column_vals=['Can also indent the indent.'], align='left', inner_borders=False, line_padding_left=5, indent_str=f"{Corners.BOTTOM_LEFT_THIN}{Horizontals.HORIZ_THIN}", indent_padding=1))
    print(table_bottom_line(width=75, column_notches=False))

    # print("\n----- Row Border Table -----")
    # print(table_top_line(width=75))
    # print(table_value_line(width=75, column_widths=[15, 25], column_vals=['TITLE', 'ID', 'DESCRIPTION'], align='left', inner_borders=False))
    # print(table_middle_line(width=75, column_notches_top=False, column_notches_bottom=False))
    # print(table_bottom_line(width=75))

    print("\n----- Full Border Table -----")
    full_border_widths = [15, 25, 15, 5, 10]
    print(table_top_line(width=75, column_widths=full_border_widths, style='filled'))
    print(table_value_line(width=75, column_widths=full_border_widths, column_vals=['TITLE', 'ID', 'DESCRIPTION'], style='filled'))
    print(table_middle_line(width=75, column_widths=full_border_widths, style='filled'))

    print(table_value_line(width=75, column_widths=full_border_widths, column_vals=['TITLE', 'ID', 'DESCRIPTION'], align='center', style='filled'))
    print(table_middle_line(width=75, column_widths=full_border_widths, style='filled'))

    print(table_value_line(width=75, column_widths=full_border_widths, column_vals=['TITLE', 'ID', 'DESCRIPTION'], align='right', style='filled'))
    print(table_middle_line(width=75, column_widths=full_border_widths, style='filled'))
    print(table_bottom_line(width=75, column_widths=full_border_widths, style='filled'))

    print()
    print(table_top_line(width=75, column_widths=full_border_widths))
    print(table_value_line(width=75, column_widths=full_border_widths, column_vals=['TITLE', 'ID', 'DESCRIPTION']))
    print(table_middle_line(width=75, column_widths=full_border_widths))
    print(table_bottom_line(width=75, column_widths=full_border_widths))

    # print("\n----- Header Border (only) Table -----")
    # print(table_top_line(width=75, column_widths=[15, 25, 40]))
    # print(table_value_line(width=75, column_widths=[15, 25], column_vals=['TITLE', 'ID', 'DESCRIPTION'], align='left'))
    # print(table_middle_line(width=75, column_widths=[15, 25, 40], column_notches_bottom=False))
    # print(table_bottom_line(width=75, column_widths=[15, 25, 40], column_notches=False))