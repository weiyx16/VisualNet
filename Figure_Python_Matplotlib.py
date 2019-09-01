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


def legend_id_set(axes, annotation_axes, legend_number, force_set=False, none_line_symbol=False):
    if legend_number > 1 or force_set:
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
        if none_line_symbol:
            #                vPacker           textarea&hPacker        vPacker
            hpackers = legend.get_children()[0].get_children()[1].get_children()[0].get_children()
            if len(legend.get_lines()) == len(hpackers):
                # scatter
                symbols = []
                for hpacker, false_line in zip(hpackers, legend.get_lines()):
                    drawarea = hpacker.get_children()[0]
                    assert 'DrawingArea' in str(drawarea.__class__)
                    for child in drawarea.get_children():
                        if false_line == child:
                            pass
                        else:
                            symbols.append(child)
            else:
                # bar / pie
                symbols = []
                for hpacker in hpackers:
                    drawarea = hpacker.get_children()[0]
                    assert 'DrawingArea' in str(drawarea.__class__)
                    symbols.append(drawarea.get_children()[0])  # rectangle
            assert len(symbols) == len(legend.get_texts())
        else:
            symbols = legend.get_lines()
        for packer_idx, (line, text) in enumerate(zip(symbols, legend.get_texts())):
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
    else:
        pass
    return annotation_axes


def get_axises(axes):
    axis_list = axes._get_axis_list()
    for axis in axis_list:
        if 'XAxis' in str(axis.__class__):
            Xaxis = axis
        if 'YAxis' in str(axis.__class__):
            Yaxis = axis
    return Xaxis, Yaxis


def overall_aesthetic(annotation_figure):
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

    return IS_MINOR_TICK, IS_MAJOR_GRIDLINE_X, IS_MINOR_GRIDLINE_X, IS_MAJOR_GRIDLINE_Y, IS_MINOR_GRIDLINE_Y


def line_area_chart(data, csv_dir, csv_file, fig, fig_type, fig_path, data_path):
    # Data
    data_row, data_column = data.shape
    legend_number = min(5, random.randint(1, data_row))
    data_index = random.sample(range(0, data_row), legend_number)
    x = list(data.columns[5:-1])

    # Annotation_data json
    annotation_figure = {'figure_name': fig_path, 'figure_type': fig_type, 'language': 'python', 'module': 'matplotlib',
                         'data_dir': csv_dir, 'data_file': csv_file}

    # Overall aesthetic control
    IS_MINOR_TICK, IS_MAJOR_GRIDLINE_X, IS_MINOR_GRIDLINE_X, IS_MAJOR_GRIDLINE_Y, IS_MINOR_GRIDLINE_Y = \
        overall_aesthetic(annotation_figure)

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

        if fig_type == 'Line_chart':
            line_style = random.sample(FID.ALL_LINE, 1)[0]
            axes.plot(x, data.iloc[data_i, 5:-1], label=data.iloc[data_i, 1],
                      linestyle=line_style,
                        gid=FID.DRAWING_OBJECT_ID + '%d' % idx)
            annotation_objects[FID.DRAWING_OBJECT_ID + '%d' % idx] = \
                {'value': 'dataloc_%d' % data_i, 'style': line_style, 'bbox': None, 'path_bbox': None}

        if fig_type == 'Area_chart':
            axes.fill_between(list(map(int, x)), list(data.iloc[data_i, 5:-1]), label=data.iloc[data_i, 1], alpha=0.3,
                              gid=FID.DRAWING_OBJECT_ID + '%d' % idx)
            annotation_objects[FID.DRAWING_OBJECT_ID + '%d' % idx] = {'value': 'dataloc_%d' % data_i, 'style': 'alpha=0.3', 'bbox': None}

            if bool(random.getrandbits(1)):
                line_style = random.sample(FID.ALL_LINE, 1)[0]
                axes.plot(list(map(int, x)), list(data.iloc[data_i, 5:-1]), label=data.iloc[data_i, 1],
                          linestyle=line_style,
                          gid=FID.DRAWING_OBJECT_ID + '%d' % idx + '_line')
                annotation_objects[FID.DRAWING_OBJECT_ID + '%d' % idx + '_line'] = \
                    {'value': 'dataloc_%d' % data_i, 'style': line_style, 'bbox': None, 'path_bbox': None}

        # marker = 'o', markerfacecolor = 'blue', markersize = 12, color = 'skyblue', linewidth = 4

    annotation_axes['drawing_objects'] = annotation_objects

    fig.canvas.draw()  # use this so the text will be populated

    ### 'axis es'
    Xaxis, Yaxis = get_axises(axes)

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
    annotation_axes = legend_id_set(axes, annotation_axes, legend_number)

    annotation_figure[FID.AXES_ID] = annotation_axes
    fig.tight_layout()
    fig.savefig(fig_path, format="svg", dpi=plt.gcf().dpi)
    with open(data_path, 'w') as outfile:
        json.dump(annotation_figure, outfile, indent=4)

    print(' >>> Writing json and svg: %s' % fig_path)


def bar_pie_chart(data, csv_dir, csv_file, fig, fig_type, fig_path, data_path):
    # Data
    data_row, data_column = data.shape
    legend_number = min(5, random.randint(1, data_row))
    if fig_type == 'Pie_chart':
        legend_number = 1
    data_index = random.sample(range(0, data_row), legend_number)
    x_number = random.randint(3, 8)
    x_index = random.sample(range(5, data_column-1), x_number)  # last column is nothing, first four is title
    x = list(data.columns[x_index])

    bars = []
    for data_i in data_index:
        bars.append(list(data.iloc[data_i, x_index]))

    # Annotation_data json
    annotation_figure = {'figure_name': fig_path, 'figure_type': fig_type, 'language': 'python', 'module': 'matplotlib',
                         'data_dir': csv_dir, 'data_file': csv_file}

    # Overall aesthetic control
    IS_MINOR_TICK, IS_MAJOR_GRIDLINE_X, IS_MINOR_GRIDLINE_X, IS_MAJOR_GRIDLINE_Y, IS_MINOR_GRIDLINE_Y = \
        overall_aesthetic(annotation_figure)

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
    def object_anno_create(annotation_objects, idx, data_index, bar_width):
        annotation_object = {'value': ['dataloc_%d' % data_index[idx], 'dataloc_%s' % x_index], 'style': bar_width}
        for bar_idx in range(x_number):
            annotation_object['bbox_%d' % bar_idx] = None
        annotation_objects[FID.DRAWING_OBJECT_ID + '%d' % idx] = annotation_object
        return annotation_objects

    annotation_objects = {}
    if fig_type == 'Bar_chart':
        # TODO: inline bar pattern https://matplotlib.org/3.1.1/gallery/shapes_and_collections/hatch_demo.html
        x_loc = np.arange(x_number)
        if legend_number == 1:
            bar_width = random.randint(60, 90) / 100
            if bool(random.getrandbits(1)):
                # Create vertical bars
                axes.bar(x_loc, bars[0], width=bar_width, label=data.iloc[data_index[0], 1], gid=FID.DRAWING_OBJECT_ID + '%d' % 0)
                # Create names on the x-axis
                plt.xticks(x_loc, x)
                annotation_figure['sub_figure_type'] = 'Vertical bar chart'
            else:
                # Create horizontal bars
                axes.barh(x_loc, bars[0], height=bar_width, label=data.iloc[data_index[0], 1], gid=FID.DRAWING_OBJECT_ID + '%d' % 0)
                # Create names on the y-axis
                plt.yticks(x_loc, x)
                annotation_figure['sub_figure_type'] = 'Horizontal bar chart'
            annotation_objects = object_anno_create(annotation_objects, 0, data_index, bar_width)

        else:
            if bool(random.getrandbits(1)):
                # Create stacked bars
                bar_width = random.randint(60, 90) / 100
                # Bar proprocess
                bar_bottom = [0.0] * x_number
                for idx, data_i in enumerate(data_index):
                    axes.bar(x_loc, bars[idx], bottom=bar_bottom, width=bar_width, label=data.iloc[data_i, 1], gid=FID.DRAWING_OBJECT_ID + '%d' % idx)
                    bar_bottom = [a + b for a, b in zip(bar_bottom, bars[idx])]
                    annotation_objects = object_anno_create(annotation_objects, idx, data_index, bar_width)
                # Create names on the x-axis
                plt.xticks(x_loc, x)
                annotation_figure['sub_figure_type'] = 'Stacked bar chart'

            else:
                # Create grouped bars
                bar_width = random.randint(60, 90) / 100 / legend_number
                # Bar loc process
                bar_bias = [0.0] * x_number
                for idx, data_i in enumerate(data_index):
                    axes.bar([a + b for a, b in zip(bar_bias, x_loc)], bars[idx],
                            width=bar_width, label=data.iloc[data_i, 1], gid=FID.DRAWING_OBJECT_ID + '%d' % idx)
                    bar_bias = [a + bar_width for a in bar_bias]
                    annotation_objects = object_anno_create(annotation_objects, idx, data_index, bar_width)
                # Create names on the x-axis
                plt.xticks([r + (legend_number-1)/2*bar_width for r in range(x_number)], x)
                annotation_figure['sub_figure_type'] = 'Grouped bar chart'

    if fig_type == 'Pie_chart':
        start_angle = random.randint(75, 105)
        axes.pie(bars[0], labels=x, autopct='%1.1f%%', startangle=start_angle)
        axes.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # set gid in pie chart
        obj_texts = axes.texts[::2]
        pct_texts = axes.texts[1::2]
        assert len(pct_texts) == len(obj_texts)
        annotation_object_texts = {}
        annotation_polar_labels = {}
        for idx, (widge, obj_text, pct_text) in enumerate(zip(axes.patches, obj_texts, pct_texts)):
            widge.set_gid(FID.DRAWING_OBJECT_ID + '%d' % idx)
            annotation_objects[FID.DRAWING_OBJECT_ID + '%d' % idx] = \
                {'value': ['dataloc_%d' % data_index[0], 'dataloc_%s' % x_index[idx]], 'bbox': None}
            obj_text.set_gid(FID.POLAR_AXIS_TICKLABEL_ID + '%d' % idx)
            annotation_polar_labels[FID.POLAR_AXIS_TICKLABEL_ID + '%d' % idx] = {'value': obj_text.get_text(), 'bbox': None}
            pct_text.set_gid(FID.OBJECT_TEXT_ID + '%d' % idx)
            annotation_object_texts[FID.OBJECT_TEXT_ID + '%d' % idx] = {'value': pct_text.get_text(), 'bbox': None}
        annotation_axes['object_texts'] = annotation_object_texts
        annotation_axes['polar_axis_labels'] = annotation_polar_labels

    annotation_axes['drawing_objects'] = annotation_objects

    fig.canvas.draw()  # use this so the text will be populated

    ### 'axis es'
    if fig_type == 'Bar_chart':
        Xaxis, Yaxis = get_axises(axes)

        if IS_MINOR_TICK:
            axes.minorticks_on()

        x_axis_label, y_axis_label = 'Time', data.iloc[0, 3]
        if annotation_figure['sub_figure_type'] == 'Horizontal bar chart':
            x_axis_label, y_axis_label = data.iloc[0, 3], 'Time'
        ### x_axis
        annotation_axes = axis_id_set(Xaxis, x_axis_label, annotation_axes, 'x', IS_MINOR_TICK, IS_MAJOR_GRIDLINE_X,
                                      IS_MINOR_GRIDLINE_X)
        ### y_axis
        annotation_axes = axis_id_set(Yaxis, y_axis_label, annotation_axes, 'y', IS_MINOR_TICK, IS_MAJOR_GRIDLINE_Y,
                                      IS_MINOR_GRIDLINE_Y)

    ### title
    axes.set_title(data.iloc[0, 4], gid=FID.TITLE_ID)
    annotation_axes[FID.TITLE_ID] = {'value': data.iloc[0, 4], 'bbox': None}

    ### legend
    annotation_axes = legend_id_set(axes, annotation_axes, legend_number, force_set=(fig_type == 'Pie_chart'), none_line_symbol=True)

    annotation_figure[FID.AXES_ID] = annotation_axes
    fig.tight_layout()
    fig.savefig(fig_path, format="svg", dpi=plt.gcf().dpi)
    with open(data_path, 'w') as outfile:
        json.dump(annotation_figure, outfile, indent=4)

    print(' >>> Writing json and svg: %s' % fig_path)


def scatter_chart(data_1, data_2, data_inter, csv_dir, csv_file_2, fig, fig_type, fig_path, data_path):
    # Data
    legend_number = min(5, random.randint(1, len(data_inter)))
    legend_list = random.sample(data_inter, legend_number)

    # Annotation_data json
    annotation_figure = {'figure_name': fig_path, 'figure_type': fig_type, 'language': 'python', 'module': 'matplotlib',
                         'data_dir': csv_dir, 'data_file': csv_file_2}

    # Overall aesthetic control
    IS_MINOR_TICK, IS_MAJOR_GRIDLINE_X, IS_MINOR_GRIDLINE_X, IS_MAJOR_GRIDLINE_Y, IS_MINOR_GRIDLINE_Y = \
        overall_aesthetic(annotation_figure)

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
    marker_list = random.sample(FID.ALL_MARKER, legend_number)
    color_list = random.sample(FID.ALL_COLOR, legend_number)
    for idx, data_i in enumerate(legend_list):
        x = data_1[data_1['Country Code'] == data_i]
        y = data_2[data_2['Country Code'] == data_i]
        # axes.scatter(list(x.iloc[0, 5:-1]), list(y.iloc[0, 5:-1]), label=x.iloc[0, 1],
        #           marker=marker_list[idx], c=color_list[idx],
        #           gid=FID.DRAWING_OBJECT_ID + '%d' % idx)
        axes.plot(list(x.iloc[0, 5:-1]), list(y.iloc[0, 5:-1]), label=x.iloc[0, 1],
                    marker=marker_list[idx], markerfacecolor=color_list[idx],
                    linestyle='None',  # random.sample(FID.ALL_LINE, 1)[0],
                    gid=FID.DRAWING_OBJECT_ID + '%d' % idx)

        annotation_objects[FID.DRAWING_OBJECT_ID + '%d' % idx] = \
            {'value': 'datafrom_%s' % data_i, 'style': marker_list[idx]+' & '+color_list[idx], 'bbox': None, 'path_bbox': None}


    annotation_axes['drawing_objects'] = annotation_objects

    fig.canvas.draw()  # use this so the text will be populated

    ### 'axis es'
    Xaxis, Yaxis = get_axises(axes)

    if IS_MINOR_TICK:
        axes.minorticks_on()

    ### x_axis
    annotation_axes = axis_id_set(Xaxis, data_1.iloc[0, 3], annotation_axes, 'x', IS_MINOR_TICK, IS_MAJOR_GRIDLINE_X,
                                  IS_MINOR_GRIDLINE_X)
    ### y_axis
    annotation_axes = axis_id_set(Yaxis, data_2.iloc[0, 3], annotation_axes, 'y', IS_MINOR_TICK, IS_MAJOR_GRIDLINE_Y,
                                  IS_MINOR_GRIDLINE_Y)

    ### title
    axes.set_title(data_1.iloc[0, 4] + ' & ' + data_2.iloc[0, 4], gid=FID.TITLE_ID)
    annotation_axes[FID.TITLE_ID] = {'value': data_1.iloc[0, 4] + ' & ' + data_2.iloc[0, 4], 'bbox': None}

    ### legend
    annotation_axes = legend_id_set(axes, annotation_axes, legend_number, none_line_symbol=True)

    annotation_figure[FID.AXES_ID] = annotation_axes
    fig.tight_layout()
    fig.savefig(fig_path, format="svg", dpi=plt.gcf().dpi)
    with open(data_path, 'w') as outfile:
        json.dump(annotation_figure, outfile, indent=4)

    print(' >>> Writing json and svg: %s' % fig_path)


def chart_batch_create(fig_type, csv_dir, chart_number=50):
    csv_files = os.listdir(csv_dir)
    chart_path = os.path.join(figures_path, fig_type)
    svg_path = os.path.join(chart_path, 'svg')
    src_data_path = os.path.join(chart_path, 'src_data')
    utils.mkdir_safe([chart_path, svg_path, src_data_path])

    print(' >> Creating %s with number %d' % (fig_type, chart_number))
    fig = plt.figure(figsize=(15, 9))
    for idx in range(chart_number):
        if fig_type in ['Line_chart', 'Area_chart', 'Bar_chart', 'Pie_chart']:
            # data postprocess
            csv_file = csv_files[random.randint(0, len(csv_files) - 1)]
            data_csv_path = os.path.join(csv_dir, csv_file)
            print(' >>> Pick file named: {}'.format(data_csv_path))
            data = statistic_data_load(data_csv_path)
            if fig_type in ['Line_chart', 'Area_chart']:
                line_area_chart(data, csv_dir, csv_file, fig, fig_type, fig_path=os.path.join(svg_path, '%s_%03d.svg' % (fig_type, idx)),
                           data_path=os.path.join(src_data_path, '%s_%03d.json' % (fig_type, idx)))
            if fig_type in ['Bar_chart', 'Pie_chart']:
                bar_pie_chart(data, csv_dir, csv_file, fig, fig_type, fig_path=os.path.join(svg_path, '%s_%03d.svg' % (fig_type, idx)),
                           data_path=os.path.join(src_data_path, '%s_%03d.json' % (fig_type, idx)))
        if fig_type in ['Scatter_chart']:
            # data postprocess
            country_num = 0
            while country_num == 0:
                csv_file_2 = random.sample(csv_files, 2)
                data_file_0 = statistic_data_load(os.path.join(csv_dir, csv_file_2[0]))
                data_file_1 = statistic_data_load(os.path.join(csv_dir, csv_file_2[1]))
                country_list_0 = list(data_file_0.iloc[:, 2])
                country_list_1 = list(data_file_1.iloc[:, 2])
                country_inter = list(set(country_list_0) & set(country_list_1))
                country_num = len(country_inter)

            print(' >>> Pick file: {}, {} with country intersected: {}'
                  .format(os.path.join(csv_dir, csv_file_2[0]), os.path.join(csv_dir, csv_file_2[1]), country_num))
            scatter_chart(data_file_0, data_file_1, country_inter, csv_dir, csv_file_2, fig, fig_type,
                          fig_path=os.path.join(svg_path, '%s_%03d.svg' % (fig_type, idx)),
                          data_path=os.path.join(src_data_path, '%s_%03d.json' % (fig_type, idx)))


if __name__ == '__main__':
    csv_dir = r'./data/postprocess/WDI/Indicator'

    FID.element_init()
    FID.aesthetic_init()
    figures_path = r'./figure/matplotlib'
    utils.mkdir_safe(figures_path)

    # # Line Chart
    # fig_type = 'Line_chart'
    # chart_batch_create(fig_type, csv_dir, chart_number=50)

    # # Area Chart
    # fig_type = 'Area_chart'
    # chart_batch_create(fig_type, csv_dir, chart_number=50)

    # # Scatter Chart
    # fig_type = 'Scatter_chart'
    # chart_batch_create(fig_type, csv_dir, chart_number=50)

    # # bar chart
    # fig_type = 'Bar_chart'
    # chart_batch_create(fig_type, csv_dir, chart_number=50)

    # pie chart
    fig_type = 'Pie_chart'
    chart_batch_create(fig_type, csv_dir, chart_number=50)
