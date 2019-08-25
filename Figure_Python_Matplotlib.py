# -*- coding: utf-8 -*-
"""
    Create different chart types in python and using matplotlib package
    To get ground truth annotation,
        - Set each element with a specific ID and pass it to svg (render+layout information)
        - Save it company with a json file which (data+aesthetic information)
        - Finally, use javascript+svg -> bbox annotation, use json -> aesthetic annotation.
    @ Yixuan Wei
    @ weiyx16@mails.tsinghua.edu.cn
"""

import numpy as np
import pandas as pd
import os
import random
from utils import utils
import Figure_elements_ID as FID
import matplotlib.pyplot as plt
import json


def statistic_data_load(csv_path):
    assert os.path.isfile(csv_path), " No such csv file! "
    data = pd.read_csv(csv_path)
    return data


def axis_id_set(axis, axis_label, annotation_axes, axis_type, IS_MINOR_TICK, IS_MAJOR_GRIDLINE, IS_MINOR_GRIDLINE = False):
    if axis_type == 'x':
        AXIS_ID, AXIS_LABEL_ID, AXIS_OFFSET_ID = FID.X_AXIS_ID, FID.X_AXIS_LABEL_ID, FID.X_AXIS_OFFSET_ID
        AXIS_MAJOR_TICK_ID, AXIS_MAJOR_TICKLABEL_ID, AXIS_MAJOR_TICKLINE_ID, AXIS_MAJOR_GRID_ID = \
            FID.X_AXIS_MAJOR_TICK_ID, FID.X_AXIS_MAJOR_TICKLABEL_ID, FID.X_AXIS_MAJOR_TICKLINE_ID, FID.X_AXIS_MAJOR_GRID_ID
        AXIS_MINOR_TICK_ID, AXIS_MINOR_TICKLINE_ID, AXIS_MINOR_GRID_ID = \
            FID.X_AXIS_MINOR_TICK_ID, FID.X_AXIS_MINOR_TICKLINE_ID, FID.X_AXIS_MINOR_GRID_ID
    if axis_type == 'y':
        AXIS_ID, AXIS_LABEL_ID, AXIS_OFFSET_ID = FID.Y_AXIS_ID, FID.Y_AXIS_LABEL_ID, FID.Y_AXIS_OFFSET_ID
        AXIS_MAJOR_TICK_ID, AXIS_MAJOR_TICKLABEL_ID, AXIS_MAJOR_TICKLINE_ID, AXIS_MAJOR_GRID_ID = \
            FID.Y_AXIS_MAJOR_TICK_ID, FID.Y_AXIS_MAJOR_TICKLABEL_ID, FID.Y_AXIS_MAJOR_TICKLINE_ID, FID.Y_AXIS_MAJOR_GRID_ID
        AXIS_MINOR_TICK_ID, AXIS_MINOR_TICKLINE_ID, AXIS_MINOR_GRID_ID = \
            FID.Y_AXIS_MINOR_TICK_ID, FID.Y_AXIS_MINOR_TICKLINE_ID, FID.Y_AXIS_MINOR_GRID_ID

    ### axis
    annotation_axis = {'bbox': None}
    axis.set_gid(AXIS_ID)
    #### axis_label
    axis.set_label_text(axis_label, gid=AXIS_LABEL_ID)
    annotation_axis[AXIS_LABEL_ID] = {'value': axis_label, 'bbox': None}

    #### axis_gridlines
    if IS_MAJOR_GRIDLINE:
        # Show the major grid lines with dark grey lines
        axis.grid(b=True, which='major')  # , color='#666666', linestyle='-')
    if IS_MINOR_GRIDLINE:
        # Show the minor grid lines with very faint and almost transparent grey lines
        axis.grid(b=True, which='minor')  #, color='#999999', linestyle='-', alpha=0.2)

    #### axis_offset
    try:
        axis.get_offset_text().set_gid(AXIS_OFFSET_ID)
        annotation_axis[AXIS_OFFSET_ID] = {'value': axis.get_offset_text().get_text(), 'bbox': None}
    except AttributeError:
        pass

    #### axis_tick_major
    annotation_major_ticks = {}
    for idx, tick in enumerate(axis.get_major_ticks()):
        tick.set_gid(AXIS_MAJOR_TICK_ID + '%d' % idx)
        annotation_major_ticks[AXIS_MAJOR_TICK_ID + '%d' % idx] = {'bbox': None}

    ##### axis_ticklabel_major
    tickslabels = axis.get_majorticklabels()
    for idx, tickslabel in enumerate(tickslabels):
        tickslabel.set_gid(AXIS_MAJOR_TICKLABEL_ID + '%d' % idx)
        annotation_major_ticks[AXIS_MAJOR_TICK_ID + '%d' % idx][
            AXIS_MAJOR_TICKLABEL_ID + '%d' % idx] = {'value': tickslabel.get_text(), 'bbox': None}
    if axis_type == 'x':
        plt.setp(tickslabels, rotation=45, ha="right", rotation_mode="anchor")

    ##### axis_tickline_major
    tickslines = axis.get_majorticklines()
    ticks_idx = 0
    for ticksline in tickslines:
        if ticksline.get_visible():
            ticksline.set_gid(AXIS_MAJOR_TICKLINE_ID + '%d' % ticks_idx)
            annotation_major_ticks[AXIS_MAJOR_TICK_ID + '%d' % ticks_idx][
                AXIS_MAJOR_TICKLINE_ID + '%d' % ticks_idx] = {'style': ticks_idx, 'bbox': None}
            # replace with aesthetic cue
            ticks_idx += 1

    if IS_MAJOR_GRIDLINE:
        ##### axis_gridline_major
        for idx, gridline in enumerate(axis.get_gridlines(which='major')):
            gridline.set_gid(AXIS_MAJOR_GRID_ID + '%d' % idx)
            annotation_major_ticks[AXIS_MAJOR_TICK_ID + '%d' % idx][
                AXIS_MAJOR_GRID_ID + '%d' % idx] = {'style': idx, 'bbox': None}

    if IS_MINOR_TICK:
        #### axis_tick_minor
        annotation_minor_ticks = {}
        for idx, tick in enumerate(axis.get_minor_ticks()):
            tick.set_gid(AXIS_MINOR_TICK_ID + '%d' % idx)
            annotation_minor_ticks[AXIS_MINOR_TICK_ID + '%d' % idx] = {'bbox': None}

        ##### axis_tickline_minor
        tickslines = axis.get_minorticklines()
        ticks_idx = 0
        for ticksline in tickslines:
            if ticksline.get_visible():
                ticksline.set_gid(AXIS_MINOR_TICKLINE_ID + '%d' % ticks_idx)
                annotation_minor_ticks[AXIS_MINOR_TICK_ID + '%d' % ticks_idx][
                    AXIS_MINOR_TICKLINE_ID + '%d' % ticks_idx] = {'style': ticks_idx, 'bbox': None}
                # replace with aesthetic cue
                ticks_idx += 1

        if IS_MINOR_GRIDLINE:
            ##### axis_gridline_minor
            for idx, gridline in enumerate(axis.get_gridlines(which='minor')):
                gridline.set_gid(AXIS_MINOR_GRID_ID + '%d' % idx)
                annotation_minor_ticks[AXIS_MINOR_TICK_ID + '%d' % idx][
                    AXIS_MINOR_GRID_ID + '%d' % idx] = {'style': idx, 'bbox': None}

        annotation_axis['%c_axis_minor_ticks' % axis_type] = annotation_minor_ticks
    annotation_axis['%c_axis_major_ticks' % axis_type] = annotation_major_ticks
    annotation_axes[AXIS_ID] = annotation_axis
    return annotation_axes


def line_chart(data, fig, fig_path, data_path):
    # Chart type
    chart_type = 'Line chart'
    # Data

    data_row, data_column = data.shape
    line_number = min(5, random.randint(1, data_row))
    data_index = random.sample(range(0, data_row), line_number)
    x = list(data.columns[5:-1])

    # Annotation_data json
    annotation_figure = {'figure_name': 'test', 'figure_type': chart_type, 'language': 'python', 'module': 'matplotlib',
                         'data_dir': csv_dir, 'data_file': csv_file}

    # Overall aesthetic control
    IS_MINOR_TICK = bool(random.getrandbits(1))
    IS_MAJOR_GRIDLINE_X = bool(random.getrandbits(1))
    IS_MINOR_GRIDLINE_X = False
    IS_MAJOR_GRIDLINE_Y = bool(random.getrandbits(1))
    IS_MINOR_GRIDLINE_Y = False
    annotation_figure['overall_aesthetic'] = {'minor tick on': IS_MINOR_TICK,
                                              'x axis major gridline on': IS_MAJOR_GRIDLINE_X,
                                              'x axis minor gridline on': IS_MINOR_GRIDLINE_X,
                                              'y axis major gridline on': IS_MAJOR_GRIDLINE_Y,
                                              'y axis minor gridline on': IS_MINOR_GRIDLINE_Y}
    # Figure
    # figure
    fig.clf()
    fig.set_gid(FID.FIGURE_ID)
    fig.patch.set_gid(FID.FIGURE_PATCH_ID)

    ## axes
    annotation_axes = {'bbox': None}
    axes = fig.gca(gid=FID.AXES_ID)
    axes.patch.set_gid(FID.AXES_PATCH_ID)
    # axes.set_position([0, 0, 1, 1])

    ### objects
    annotation_objects = {}
    for idx, data_i in enumerate(data_index):
        axes.plot(x, data.iloc[data_i, 5:-1], label=data.iloc[data_i, 1],
                  gid=FID.DRAWING_OBJECT_ID + '%d' % idx)

        # marker = 'o', markerfacecolor = 'blue', markersize = 12, color = 'skyblue', linewidth = 4, linestyle = 'dashed'

        annotation_objects[FID.DRAWING_OBJECT_ID + '%d' % idx] = {'value': 'dataloc_%d' % data_i, 'bbox': None}
    annotation_axes['drawing_objects'] = annotation_objects

    fig.canvas.draw()  # use this so the text will be populated

    ### 'axis es'
    axis_list = axes._get_axis_list()
    for axis in axis_list:
        if 'XAxis' in str(axis.__class__):
            Xaxis = axis
        if 'YAxis' in str(axis.__class__):
            Yaxis = axis

    if IS_MINOR_TICK:
        axes.minorticks_on()

    ### x_axis
    annotation_axes = axis_id_set(Xaxis, 'Time', annotation_axes, 'x', IS_MINOR_TICK, IS_MAJOR_GRIDLINE_X,
                                  IS_MINOR_GRIDLINE_X)
    ### y_axis
    annotation_axes = axis_id_set(Yaxis, data.iloc[0, 3], annotation_axes, 'y', IS_MINOR_TICK, IS_MAJOR_GRIDLINE_Y,
                                  IS_MINOR_GRIDLINE_Y)

    ### title
    axes.set_title(data.iloc[0, 4], gid=FID.TITLE_ID)
    annotation_axes[FID.TITLE_ID] = {'value': data.iloc[0, 4], 'bbox': None}

    ### legend
    legend = axes.legend()
    annotation_legend = {}
    legend.set_gid(FID.LEGEND_ID)
    legend.legendPatch.set_gid(FID.LEGEND_PATCH_ID)
    #### legend_title
    legend.set_title('Legend')
    legend.get_title().set_gid(FID.LEGEND_TITLE_ID)
    annotation_legend[FID.LEGEND_TITLE_ID] = {'value': 'Legend', 'bbox': None}

    #### legend packer
    annotation_packers = {}
    for packer_idx, (line, text) in enumerate(zip(legend.get_lines(), legend.get_texts())):
        ##### legend_line
        line.set_gid(FID.LEGEND_SYMBOL_ID + '%d' % packer_idx)
        ##### legend_text
        text.set_gid(FID.LEGEND_TEXT_ID + '%d' % packer_idx)
        annotation_packers[FID.LEGEND_PACKER_ID + '%d' % packer_idx] = {
                                FID.LEGEND_SYMBOL_ID + '%d' % packer_idx: {'value': text.get_text(), 'bbox': None},
                                FID.LEGEND_TEXT_ID + '%d' % packer_idx: {'value': text.get_text(), 'bbox': None},
                                'bbox': None}
    annotation_legend['legend_packers'] = annotation_packers
    annotation_axes[FID.LEGEND_ID] = annotation_legend

    annotation_figure[FID.AXES_ID] = annotation_axes
    fig.tight_layout()
    fig.savefig(fig_path, format="svg", dpi=plt.gcf().dpi)
    with open(data_path, 'w') as outfile:
        json.dump(annotation_figure, outfile, indent=4)

    print(' >>> Writing json and svg: %s' % fig_path)


if __name__ == '__main__':
    csv_dir = r'./data/postprocess/WDI/Indicator'
    csv_files = os.listdir(csv_dir)

    FID.element_init()
    figures_path = r'./figure/matplotlib'
    utils.mkdir_safe(figures_path)

    line_chart_path = os.path.join(figures_path, 'Line_chart')
    svg_path = os.path.join(line_chart_path, 'svg')
    src_data_path = os.path.join(line_chart_path, 'src_data')
    utils.mkdir_safe([line_chart_path, svg_path, src_data_path])

    line_chart_number = 50
    print(' >> Creating Line Chart with number %d' % line_chart_number)
    fig = plt.figure(figsize=(15, 9))
    for idx in range(line_chart_number):
        csv_file = csv_files[random.randint(0, len(csv_files) - 1)]
        data_csv_path = os.path.join(csv_dir, csv_file)
        print(' >>> Pick file named: {}'.format(data_csv_path))
        data = statistic_data_load(data_csv_path)
        line_chart(data, fig, fig_path=os.path.join(svg_path, 'Line_chart_%03d.svg' % idx),
                   data_path=os.path.join(src_data_path, 'Line_chart_%03d.json' % idx))