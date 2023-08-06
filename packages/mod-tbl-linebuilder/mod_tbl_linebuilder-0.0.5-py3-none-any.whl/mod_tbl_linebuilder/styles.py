from utflib.table_chars import Corners, Horizontals, Verticals, Middles


class Style():

    LOCATIONS = {
        'top_left': {
            'thin': Corners.TOP_LEFT_THIN,
            'filled': Corners.TOP_LEFT_FILLED
        },
        'top_right': {
            'thin': Corners.TOP_RIGHT_THIN,
            'filled': Corners.TOP_RIGHT_FILLED
        },
        'bottom_left': {
            'thin': Corners.BOTTOM_LEFT_THIN,
            'filled': Corners.BOTTOM_LEFT_FILLED
        },
        'bottom_right': {
            'thin': Corners.BOTTOM_RIGHT_THIN,
            'filled': Corners.BOTTOM_RIGHT_FILLED            
        },
        'vertical_left': {
            'thin': Verticals.VERT_THIN,
            'filled': Verticals.VERT_LEFT_FILLED
        },
        'vertical_right': {
            'thin': Verticals.VERT_THIN,
            'filled': Verticals.VERT_RIGHT_FILLED
        },
        'vertical_middle': {
            'thin': Verticals.VERT_THIN,
            'filled': Verticals.VERT_MIDDLE_FILLED
        },
        'vertical_notch_right': {
            'thin': Verticals.VERT_DASH_LEFT_THIN,
            'filled': Verticals.VERT_RIGHT_FILLED
        },
        'vertical_notch_left': {
            'thin': Verticals.VERT_DASH_RIGHT_THIN,
            'filled': Verticals.VERT_LEFT_FILLED
        },
        'horizontal_top': {
            'thin': Horizontals.HORIZ_THIN,
            'filled': Horizontals.HORIZ_TOP_FILLED
        },
        'horizontal_bottom': {
            'thin': Horizontals.HORIZ_THIN,
            'filled': Horizontals.HORIZ_BOTTOM_FILLED
        },
        'horizontal_middle': {
            'thin': Horizontals.HORIZ_THIN,
            'filled': Horizontals.HORIZ_MIDDLE_FILLED
        },
        'horizontal_notch_top': {
            'thin': Horizontals.HORIZ_DASH_DOWN_THIN,
            'filled': Horizontals.HORIZ_TOP_FILLED
        },
        'horizontal_notch_bottom': {
            'thin': Horizontals.HORIZ_DASH_UP_THIN,
            'filled': Horizontals.HORIZ_BOTTOM_FILLED
        },
        'middle': {
            'thin': Middles.MIDDLE_THIN,
            'filled': Middles.MIDDLE_FILLED
        }
    }

    @staticmethod
    def char_at(location, style='thin'):
        if location in Style.LOCATIONS and style in Style.LOCATIONS[location]:
            return Style.LOCATIONS[location][style]
        
        print("Not found.")
        return ''