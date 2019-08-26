# -*- coding: utf-8 -*-
"""
    Global variable name for each element in figures to fetch elements in svg files
    @ Yixuan Wei
    @ weiyx16@mails.tsinghua.edu.cn
"""


def element_init():
    global FIGURE_ID, FIGURE_PATCH_ID
    global AXES_ID, AXES_PATCH_ID
    global TITLE_ID
    global LEGEND_ID, LEGEND_PATCH_ID, LEGEND_TITLE_ID, LEGEND_SYMBOL_ID, LEGEND_TEXT_ID, LEGEND_PACKER_ID
    global X_AXIS_ID, X_AXIS_LABEL_ID, X_AXIS_OFFSET_ID, X_AXIS_LINE_ID
    global Y_AXIS_ID, Y_AXIS_LABEL_ID, Y_AXIS_OFFSET_ID, Y_AXIS_LINE_ID
    global X_AXIS_MAJOR_TICK_ID, X_AXIS_MAJOR_TICKLABEL_ID, X_AXIS_MAJOR_TICKLINE_ID, X_AXIS_MAJOR_GRID_ID
    global Y_AXIS_MAJOR_TICK_ID, Y_AXIS_MAJOR_TICKLABEL_ID, Y_AXIS_MAJOR_TICKLINE_ID, Y_AXIS_MAJOR_GRID_ID
    global X_AXIS_MINOR_TICK_ID, X_AXIS_MINOR_TICKLABEL_ID, X_AXIS_MINOR_TICKLINE_ID, X_AXIS_MINOR_GRID_ID
    global Y_AXIS_MINOR_TICK_ID, Y_AXIS_MINOR_TICKLABEL_ID, Y_AXIS_MINOR_TICKLINE_ID, Y_AXIS_MINOR_GRID_ID
    global DRAWING_OBJECT_ID

    FIGURE_ID, FIGURE_PATCH_ID = "the_figure", "the_figure_patch"
    AXES_ID, AXES_PATCH_ID = "the_axes", "the_axes_patch"
    TITLE_ID = "the_title"
    LEGEND_ID, LEGEND_PATCH_ID, LEGEND_TITLE_ID, LEGEND_SYMBOL_ID, LEGEND_TEXT_ID, LEGEND_PACKER_ID = \
        "the_legend", "the_legend_patch", "the_legend_title", "the_legend_symbol_", "the_legend_text_", "the_legend_packer_"
    X_AXIS_ID, X_AXIS_LABEL_ID, X_AXIS_OFFSET_ID, X_AXIS_LINE_ID = \
        "the_x_axis", "the_x_axis_label", "the_x_axis_offset", "the_x_axis_line"
    Y_AXIS_ID, Y_AXIS_LABEL_ID, Y_AXIS_OFFSET_ID, Y_AXIS_LINE_ID = \
        "the_y_axis", "the_y_axis_label", "the_y_axis_offset", "the_y_axis_line"
    X_AXIS_MAJOR_TICK_ID, X_AXIS_MAJOR_TICKLABEL_ID, X_AXIS_MAJOR_TICKLINE_ID, X_AXIS_MAJOR_GRID_ID = \
        "the_x_axis_major_tick_", "the_x_axis_major_ticklabel_", "the_x_axis_major_tickline_", "the_x_axis_major_gridline_"
    Y_AXIS_MAJOR_TICK_ID, Y_AXIS_MAJOR_TICKLABEL_ID, Y_AXIS_MAJOR_TICKLINE_ID, Y_AXIS_MAJOR_GRID_ID = \
        "the_y_axis_major_tick_", "the_y_axis_major_ticklabel_", "the_y_axis_major_tickline_", "the_y_axis_major_gridline_"
    X_AXIS_MINOR_TICK_ID, X_AXIS_MINOR_TICKLABEL_ID, X_AXIS_MINOR_TICKLINE_ID, X_AXIS_MINOR_GRID_ID = \
        "the_x_axis_minor_tick_", "the_x_axis_minor_ticklabel_", "the_x_axis_minor_tickline_", "the_x_axis_minor_gridline_"
    Y_AXIS_MINOR_TICK_ID, Y_AXIS_MINOR_TICKLABEL_ID, Y_AXIS_MINOR_TICKLINE_ID, Y_AXIS_MINOR_GRID_ID = \
        "the_y_axis_minor_tick_", "the_y_axis_minor_ticklabel_", "the_y_axis_minor_tickline_", "the_y_axis_minor_gridline_"
    DRAWING_OBJECT_ID = "the_drawing_object_"

def asso_init():
    global ASSO_TYPE
    ASSO_TYPE = {
        'self': -1,
        'none': 0,
        'relation': 1,
        'measure': 2,
        'similarity': 3
    }

def aesthetic_init():
    global ALL_LINE, ALL_MARKER, ALL_COLOR
    ALL_LINE = ['-', '--', '-.', ':']
    ALL_MARKER = ['.', ',', 'o', 'v', '^', '>', '<', 's', 'p', '*', 'h', 'H', 'D', 'd', '1', '2', '3', '4', 'x']
    ALL_COLOR = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']