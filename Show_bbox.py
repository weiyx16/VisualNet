# -*- coding: utf-8 -*-
"""
    Show results of bboxes from javascript + svg
    @ Yixuan Wei
    @ weiyx16@mails.tsinghua.edu.cn
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import Figure_elements_ID as FID
import json
import PIL.Image as Image


def bbox_postprocess(bbox, image_size):
    '''For case: the width/height of bbox = 0, e.g. for line(tickline, gridline..) '''
    # See bbox definition of svg.getBBox(): https://developer.mozilla.org/en-US/docs/Web/API/SVGGraphicsElement/getBBox
    # https://developer.mozilla.org/en-US/docs/Web/API/Element/getBoundingClientRect

    # minc, minr, maxc, maxr  =>  bbox
    if bbox[2] == bbox[0]:
        # width = 0
        bbox[0] = max(image_size[0], bbox[0] - 1)
        bbox[2] = min(image_size[0] + image_size[2], bbox[2] + 1)
    if bbox[3] == bbox[1]:
        # height = 0
        bbox[1] = max(image_size[1], bbox[1] - 1)
        bbox[3] = min(image_size[1] + image_size[3], bbox[3] + 1)
    return bbox


def show_bbox(bboxes, image, bbox_png_path):

    plt.cla()
    plt.clf()
    fig = plt.figure(figsize=(18, 10))
    axes = fig.gca()
    axes.imshow(image)
    axes.set_title(' Bbox Recovered from svg file ')

    bbox_types = [
        # FID.FIGURE_ID, FID.FIGURE_PATCH_ID,
        # FID.AXES_ID, FID.AXES_PATCH_ID,
        # FID.TITLE_ID,
        # FID.LEGEND_ID, FID.LEGEND_PATCH_ID, FID.LEGEND_TITLE_ID, FID.LEGEND_SYMBOL_ID, FID.LEGEND_TEXT_ID, FID.LEGEND_PACKER_ID,
        # FID.X_AXIS_ID, FID.X_AXIS_LABEL_ID, FID.X_AXIS_OFFSET_ID,
        # FID.Y_AXIS_ID, FID.Y_AXIS_LABEL_ID, FID.Y_AXIS_OFFSET_ID,
        # FID.X_AXIS_MAJOR_TICK_ID, FID.X_AXIS_MAJOR_TICKLABEL_ID, FID.X_AXIS_MAJOR_TICKLINE_ID, FID.X_AXIS_MAJOR_GRID_ID,
        # FID.Y_AXIS_MAJOR_TICK_ID, FID.Y_AXIS_MAJOR_TICKLABEL_ID, FID.Y_AXIS_MAJOR_TICKLINE_ID, FID.Y_AXIS_MAJOR_GRID_ID,
        # FID.X_AXIS_MINOR_TICK_ID, FID.X_AXIS_MINOR_TICKLABEL_ID, FID.X_AXIS_MINOR_TICKLINE_ID, FID.X_AXIS_MINOR_GRID_ID,
        # FID.Y_AXIS_MINOR_TICK_ID, FID.Y_AXIS_MINOR_TICKLABEL_ID, FID.Y_AXIS_MINOR_TICKLINE_ID, FID.Y_AXIS_MINOR_GRID_ID,
        # FID.DRAWING_OBJECT_ID
    ]

    # TODO: Need to redefine the bbox of parent nodes (like axis tick, mainly for the reason of gridlines)
    for bbox_type, bbox in bboxes.items():
        for bbox_type_show in bbox_types:
            if (bbox_type_show[-1] == '_' and bbox_type_show in bbox_type) or (bbox_type_show[-1] != '_' and bbox_type == bbox_type_show):
                bbox = bbox_postprocess(bbox, bboxes[FID.FIGURE_ID])
                minc, minr, maxc, maxr = bbox
                rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr, fill=False, edgecolor='red', linewidth=1)
                axes.add_patch(rect)

    axes.set_axis_off()
    fig.tight_layout()
    fig.savefig(bbox_png_path)


if __name__ == '__main__':
    cwd = os.getcwd()
    png_path = os.path.join(cwd, 'test_web.png')
    bbox_path = os.path.join(cwd, 'test_bbox.json')
    bbox_png_path = os.path.join(cwd, 'test_bbox_web.png')
    FID.element_init()
    with open(bbox_path, 'r') as infile:
        bboxes = json.load(infile)
    image = Image.open(png_path)
    show_bbox(bboxes, image, bbox_png_path)
