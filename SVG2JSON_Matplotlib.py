# -*- coding: utf-8 -*-
"""
    Convert different chart svg files created by matplotlib package to json extracted with ground truth annotations
    Combine with data & aesthetic annotation from json files
    @ Yixuan Wei
    @ weiyx16@mails.tsinghua.edu.cn
    Motivated by: https://github.com/Maluuba/bokeh/blob/figureqa-bbox-0.1.0/bokeh/io.py
"""


from subprocess import Popen, PIPE
import os
import io
import Figure_elements_ID as FID
import json
import pandas as pd
import sys
from utils.utils import merge_dict_2 as merge_dict
from utils.utils import mkdir_safe

def detect_phantomjs():
    """ Detect if PhantomJS is avaiable in PATH.
    See: https://bokeh.pydata.org/en/latest/docs/user_guide/export.html#additional-dependencies
    """
    default_PHANTOMJS_PREFIX = '/n/home06/ywei1998/anaconda3/envs/py36/bin/'
    PHANTOMJS_PREFIX = os.environ.get('PHANTOMJS_PREFIX', default_PHANTOMJS_PREFIX)
    phantomjs_path = os.path.join(PHANTOMJS_PREFIX, 'phantomjs')

    try:
        proc = Popen([phantomjs_path, "--version"], stdout=PIPE, stderr=PIPE)
        proc.wait()
    except OSError:
        raise RuntimeError('PhantomJS is not present in PATH. Try "conda install -c conda-forge phantomjs" or \
                           "npm install -g phantomjs-prebuilt"')
    else:
        return phantomjs_path


def detect_chrome():
    web_driver_prefix = './webdrivers'
    chrome_path = os.path.join(web_driver_prefix, 'chromedriver')
    try:
        proc = Popen([chrome_path, "--version"], stdout=PIPE, stderr=PIPE)
        proc.wait()
    except OSError:
        raise RuntimeError('chrome_path is not present in PATH. '
                           'try to download from the website')
    else:
        return chrome_path, os.path.join(web_driver_prefix, "webdriver.log")


def crop_image(image, bbox):
    '''Crop the border from the layout'''
    cropped_image = image.crop((bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]))

    return cropped_image


def export_png_and_bbox(svg_path, png_path, driver=None):
    import selenium.webdriver as webdriver  # "conda install -c bokeh selenium" or "pip install selenium"
    from selenium.webdriver.chrome.options import Options as webdriver_Options
    import PIL.Image as Image  # "conda install pillow" or "pip install pillow"
    # assert that web driver is in path for webdriver

    # phantomjs_path = detect_phantomjs()
    chrome_path, log_path = detect_chrome()

    if driver is None:
        # Use headless chrome version instead of the one in phantomJS..
        options = webdriver_Options()
        options.headless = True
        # options.binary_location = '/Applications/Google Chrome   Canary.app/Contents/MacOS/Google Chrome Canary'

        web_driver = webdriver.Chrome(executable_path=chrome_path, service_log_path=log_path, chrome_options=options)

        # Create a desired capabilities object as a starting point.
        # dcap = webdriver.DesiredCapabilities.PHANTOMJS.copy()
        # dcap["phantomjs.page.settings.userAgent"] = \
        #     'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 ' \
        #     '(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        # (
        #     "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        #     '*/*',
        #     'en-US,en;q=0.8',
        #     'max-age=0',
        #     'keep-alive'
        # )

        # web_driver = webdriver.PhantomJS(desired_capabilities=dcap, executable_path=phantomjs_path,
        #                                  service_log_path="webdriver.log")
    else:
        web_driver = driver

    # Get bboxes for each elements through javascript
    web_driver.get('file:///' + svg_path)
    get_bbox_script = """
        var bboxes = {};
        figure_show_bbox = document.documentElement.getBoundingClientRect();
        bboxes['figure_show'] = [figure_show_bbox['x'], figure_show_bbox['y'], figure_show_bbox['width'], figure_show_bbox['height']];
        var layer_nodes = [];
        var next_layer_nodes = [];
        // document.documentElement == svg
        // document.documentElement.children[1] == ('the_figure')
        layer_nodes.push(document.documentElement.children[1]);
        while (layer_nodes.length != 0) {
            for (var node_idx = 0; node_idx<layer_nodes.length; node_idx++){
                var current_node = layer_nodes[node_idx];
                // console.log('Fetching bbox for %s', current_node.id);
                var cur_SVGRect = current_node.getBBox();
                bboxes[current_node.id] = [cur_SVGRect['x'], cur_SVGRect['y'], 
                    cur_SVGRect['width']+cur_SVGRect['x'], cur_SVGRect['height']+cur_SVGRect['y']];
                for (var next_node_idx = 0;
                    next_node_idx<current_node.childElementCount;
                    next_node_idx++){
                    var next_node = layer_nodes[node_idx].children[next_node_idx];
                    if (next_node.id.startsWith('the')){
                        next_layer_nodes.push(next_node);
                    }
                }
            }
            layer_nodes = next_layer_nodes;
            next_layer_nodes = [];
        }
        // console.log(bboxes);
        return bboxes;  // for use in python through web driver
        """

    bboxes_dict = web_driver.execute_script(get_bbox_script)
    # web_driver.close()

    # get rendered png file
    # way 1: html based
    # png = html_png_render(bboxes_dict["the_figure"], web_driver,svg_path)
    # way 2: set svg viewBox to resize
    figure_show_bbox = bboxes_dict['figure_show']
    web_driver.set_window_size(figure_show_bbox[2], figure_show_bbox[3])
    resize_script = """document.documentElement.setAttribute('viewBox', {})""" .format(figure_show_bbox)
    web_driver.execute_script(resize_script)
    png = web_driver.get_screenshot_as_png()
    # way 3: draw svg to canvas and then save canvas (Elegent way):
    # See this::: https://stackoverflow.com/questions/3975499/convert-svg-to-image-jpeg-png-etc-in-the-browser
    # Or this: https://spin.atomicobject.com/2014/01/21/convert-svg-to-png/ -> SVG_Render_Png.js

    image = Image.open(io.BytesIO(png))
    cropped_image = crop_image(image, bboxes_dict[FID.FIGURE_ID])
    cropped_image.save(png_path)

    if driver is None:  # only quit webdriver if not passed in as arg
        web_driver.quit()

    return bboxes_dict, cropped_image


def html_png_render(bbox_fig, web_driver, svg_path):
    # https://stackoverflow.com/questions/28652648/how-to-use-external-svg-in-html
    html = """<!DOCTYPE html>
    <html lang="en">
    <body>
        <meta charset="UTF-8">
        <object width="{}px" height="{}px" data="{}" type="image/svg+xml"></object>
        <!-- <img width="px" height="px" src=""> -->
    </body>
    </html>""" .format(bbox_fig[2], bbox_fig[3], svg_path.split('/')[-1])

    # # https://bl.ocks.org/mbostock/6466603
    # html = """<!DOCTYPE html>
    # <html lang="en">
    # <body>
    #     <meta charset="utf-8">
    #     <canvas width="%d" height="%d"></canvas>
    #     <script>
    #     var canvas = document.querySelector("canvas"),
    #         context = canvas.getContext("2d");
    #     var image = new Image;
    #     image.src = "%s";
    #     image.onload = function() {
    #         context.drawImage(image, 0, 0);
    #         var a = document.createElement("a");
    #         a.download = "%s";
    #         a.href = canvas.toDataURL("image/png");
    #         a.click();
    #     };
    #     </script>
    # </body>
    # </html>
    # """ % (bboxes_dict["the_figure"][2], bboxes_dict["the_figure"][3], svg_path.split('/')[-1], png_path.split('/')[-1])

    html_path = os.path.join(os.getcwd(), 'tmp.html')
    with open(html_path, 'w') as f_html:
        f_html.write(html)

    web_driver.get('file:///' + html_path)
    web_driver.set_window_size(1.5*bbox_fig[2], 1.5*bbox_fig[3])
    png = web_driver.get_screenshot_as_png()

    return png


def bboxes_postprocess(bboxes):
    '''Add bbox for legend packer/axis line and redefine axis bbox/tick by removing gridline'''

    def bbox_merge(bbox_cur, bbox_add):
        bbox_cur[0] = min(bbox_cur[0], bbox_add[0])
        bbox_cur[1] = min(bbox_cur[1], bbox_add[1])
        bbox_cur[2] = max(bbox_cur[2], bbox_add[2])
        bbox_cur[3] = max(bbox_cur[3], bbox_add[3])
        return bbox_cur

    # def merge_dict(dict1, dict2):
    #     z = dict1.copy()  # start with x's keys and values
    #     z.update(dict2)  # modifies z with y's keys and values & returns None
    #     return z

    bboxes_packer = {}
    for element_type, element_bbox in bboxes.items():
        if FID.LEGEND_SYMBOL_ID in element_type:
            idx = element_type.split('_')[-1]
            bboxes_packer[FID.LEGEND_PACKER_ID + idx] = bbox_merge(element_bbox, bboxes[FID.LEGEND_TEXT_ID + idx])

        if FID.X_AXIS_ID == element_type:
            # use top of tickline as axis bbox
            element_bbox[1] = bboxes[FID.X_AXIS_MAJOR_TICKLINE_ID + str(1)][1]
            if FID.X_AXIS_OFFSET_ID in list(bboxes):
                element_bbox = bbox_merge(element_bbox, bboxes[FID.X_AXIS_OFFSET_ID])
        if FID.Y_AXIS_ID == element_type:
            # use right of tickline as axis bbox
            element_bbox[2] = bboxes[FID.Y_AXIS_MAJOR_TICKLINE_ID + str(1)][2]
            if FID.Y_AXIS_OFFSET_ID in list(bboxes):
                element_bbox = bbox_merge(element_bbox, bboxes[FID.Y_AXIS_OFFSET_ID])
        if FID.X_AXIS_MAJOR_TICK_ID in element_type:
            # use top of tickline as axis bbox
            element_bbox[1] = bboxes[FID.X_AXIS_MAJOR_TICKLINE_ID + element_type.split('_')[-1]][1]
        if FID.X_AXIS_MINOR_TICK_ID in element_type:
            # use top of tickline as axis bbox
            element_bbox[1] = bboxes[FID.X_AXIS_MINOR_TICKLINE_ID + element_type.split('_')[-1]][1]
        if FID.Y_AXIS_MAJOR_TICK_ID in element_type:
            # use right of tickline as axis bbox
            element_bbox[2] = bboxes[FID.Y_AXIS_MAJOR_TICKLINE_ID + element_type.split('_')[-1]][2]
        if FID.Y_AXIS_MINOR_TICK_ID in element_type:
            # use right of tickline as axis bbox
            element_bbox[2] = bboxes[FID.Y_AXIS_MINOR_TICKLINE_ID + element_type.split('_')[-1]][2]

    bboxes[FID.X_AXIS_LINE_ID] = bboxes[FID.X_AXIS_ID]
    bboxes[FID.X_AXIS_LINE_ID][3] = bboxes[FID.X_AXIS_MAJOR_TICKLINE_ID + str(1)][3]
    bboxes[FID.Y_AXIS_LINE_ID] = bboxes[FID.Y_AXIS_ID]
    bboxes[FID.Y_AXIS_LINE_ID][0] = bboxes[FID.Y_AXIS_MAJOR_TICKLINE_ID + str(1)][0]

    return merge_dict(bboxes, bboxes_packer)


def bbox_fetch(bboxes, key):
    try:
        bbox = bboxes[key]
    except KeyError:
        bbox = None
    finally:
        return bbox


def export_annotation_bbox(bboxes, data):
    data['figure_size'] = [bboxes[FID.FIGURE_ID][2], bboxes[FID.FIGURE_ID][3]]

    # # https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
    # # Can't use iterate to change value in dict..
    # def bbox_insert(key_former, value_former, bboxes):
    #     if isinstance(value_former, dict):
    #         for key_latter, value_latter in value_former.items():
    #             if 'bbox' == key_latter:
    #                 value_former['bbox'] = bbox_fetch(bboxes, key_former)
    #                 value_latter = bbox_insert(key_latter, value_latter, bboxes)
    #     return value_former
    #
    # for k, v in data.items():
    #     v = bbox_insert(k, v, bboxes)

    data[FID.AXES_ID]['bbox'] = bbox_fetch(bboxes, FID.AXES_PATCH_ID)
    dict_loop = []
    dict_loop_key = []
    dict_loop.append(data[FID.AXES_ID])
    dict_loop_key.append(FID.AXES_ID)
    while len(dict_loop):
        dict_loop_next = []
        dict_loop_key_next = []
        for dict_point, dict_point_key in zip(dict_loop, dict_loop_key):
            for k_next, v_next in dict_point.items():
                if isinstance(v_next, dict):
                    dict_loop_next.append(v_next)
                    dict_loop_key_next.append(k_next)
                if 'bbox' == k_next:
                    dict_point['bbox'] = bbox_fetch(bboxes, dict_point_key)
        dict_loop = dict_loop_next
        dict_loop_key = dict_loop_key_next
    return data


def create_association(node_list, asso_list, asso_type):
    asso_tabel = pd.DataFrame(data=asso_type['none'], index=node_list, columns=node_list)
    for node in node_list:
        asso_tabel[node][node] = asso_type['self']
    for asso in asso_list:
        asso_tabel[asso[0]][asso[1]] = asso[2]
        asso_tabel[asso[1]][asso[0]] = asso[2]
    return asso_tabel


def export_annotation_association(association_path):
    FID.asso_init()
    # levelone_association
    node_list = [FID.X_AXIS_ID, FID.Y_AXIS_ID, FID.TITLE_ID, FID.LEGEND_ID, FID.DRAWING_OBJECT_ID]
    asso_list = [[FID.X_AXIS_ID, FID.Y_AXIS_ID, FID.ASSO_TYPE['similarity']],
                 [FID.X_AXIS_ID, FID.DRAWING_OBJECT_ID, FID.ASSO_TYPE['measure']],
                 [FID.Y_AXIS_ID, FID.DRAWING_OBJECT_ID, FID.ASSO_TYPE['measure']],
                 [FID.LEGEND_ID, FID.DRAWING_OBJECT_ID, FID.ASSO_TYPE['similarity']],
                 [FID.TITLE_ID, FID.DRAWING_OBJECT_ID, FID.ASSO_TYPE['relation']]]
    levelone_asso = create_association(node_list, asso_list, FID.ASSO_TYPE)

    # leveltwo_association
    node_list = [FID.X_AXIS_LINE_ID, FID.X_AXIS_OFFSET_ID, FID.X_AXIS_MAJOR_TICK_ID, FID.X_AXIS_LABEL_ID]
    asso_list = [[FID.X_AXIS_LINE_ID, FID.X_AXIS_MAJOR_TICK_ID, FID.ASSO_TYPE['relation']],
                 [FID.X_AXIS_OFFSET_ID, FID.X_AXIS_MAJOR_TICK_ID, FID.ASSO_TYPE['measure']],
                 [FID.X_AXIS_LINE_ID, FID.X_AXIS_LABEL_ID, FID.ASSO_TYPE['relation']]]
    leveltwo_asso_x_axis = create_association(node_list, asso_list, FID.ASSO_TYPE)
    node_list = [FID.Y_AXIS_LINE_ID, FID.Y_AXIS_OFFSET_ID, FID.Y_AXIS_MAJOR_TICK_ID, FID.Y_AXIS_LABEL_ID]
    asso_list = [[FID.Y_AXIS_LINE_ID, FID.Y_AXIS_MAJOR_TICK_ID, FID.ASSO_TYPE['relation']],
                 [FID.Y_AXIS_OFFSET_ID, FID.Y_AXIS_MAJOR_TICK_ID, FID.ASSO_TYPE['measure']],
                 [FID.Y_AXIS_LINE_ID, FID.Y_AXIS_LABEL_ID, FID.ASSO_TYPE['relation']]]
    leveltwo_asso_y_axis = create_association(node_list, asso_list, FID.ASSO_TYPE)

    # levelthree_association
    node_list = [FID.LEGEND_TITLE_ID, FID.LEGEND_SYMBOL_ID, FID.LEGEND_TEXT_ID]
    asso_list = [[FID.LEGEND_TITLE_ID, FID.LEGEND_SYMBOL_ID, FID.ASSO_TYPE['relation']],
                 [FID.LEGEND_TITLE_ID, FID.LEGEND_TEXT_ID, FID.ASSO_TYPE['relation']],
                 [FID.LEGEND_SYMBOL_ID, FID.LEGEND_TEXT_ID, FID.ASSO_TYPE['measure']]]
    levelthree_asso_legend = create_association(node_list, asso_list, FID.ASSO_TYPE)
    node_list = [FID.X_AXIS_MAJOR_TICKLABEL_ID, FID.X_AXIS_MAJOR_TICKLINE_ID, FID.X_AXIS_MAJOR_GRID_ID]
    asso_list = [[FID.X_AXIS_MAJOR_TICKLINE_ID, FID.X_AXIS_MAJOR_GRID_ID, FID.ASSO_TYPE['relation']],
                 [FID.X_AXIS_MAJOR_TICKLABEL_ID, FID.X_AXIS_MAJOR_TICKLINE_ID, FID.ASSO_TYPE['measure']]]
    levelthree_asso_x_tick = create_association(node_list, asso_list, FID.ASSO_TYPE)
    node_list = [FID.Y_AXIS_MAJOR_TICKLABEL_ID, FID.Y_AXIS_MAJOR_TICKLINE_ID, FID.Y_AXIS_MAJOR_GRID_ID]
    asso_list = [[FID.Y_AXIS_MAJOR_TICKLINE_ID, FID.Y_AXIS_MAJOR_GRID_ID, FID.ASSO_TYPE['relation']],
                 [FID.Y_AXIS_MAJOR_TICKLABEL_ID, FID.Y_AXIS_MAJOR_TICKLINE_ID, FID.ASSO_TYPE['measure']]]
    levelthree_asso_y_tick = create_association(node_list, asso_list, FID.ASSO_TYPE)

    # levelisomerism_association
    # only node on leaf -> association among different hierarchical level
    node_list = [FID.TITLE_ID, FID.DRAWING_OBJECT_ID,
                 FID.X_AXIS_LINE_ID, FID.X_AXIS_OFFSET_ID, FID.X_AXIS_LABEL_ID,
                 FID.X_AXIS_MAJOR_TICKLABEL_ID, FID.X_AXIS_MAJOR_TICKLINE_ID,
                 FID.Y_AXIS_LINE_ID, FID.Y_AXIS_OFFSET_ID, FID.Y_AXIS_LABEL_ID,
                 FID.Y_AXIS_MAJOR_TICKLABEL_ID, FID.Y_AXIS_MAJOR_TICKLINE_ID,
                 FID.LEGEND_TITLE_ID, FID.LEGEND_SYMBOL_ID, FID.LEGEND_TEXT_ID]
    asso_list = [[FID.TITLE_ID, FID.DRAWING_OBJECT_ID, FID.ASSO_TYPE['relation']],
                 [FID.DRAWING_OBJECT_ID, FID.X_AXIS_LABEL_ID, FID.ASSO_TYPE['relation']],
                 [FID.DRAWING_OBJECT_ID, FID.X_AXIS_LINE_ID, FID.ASSO_TYPE['relation']],
                 [FID.DRAWING_OBJECT_ID, FID.X_AXIS_MAJOR_TICKLABEL_ID, FID.ASSO_TYPE['measure']],
                 [FID.DRAWING_OBJECT_ID, FID.X_AXIS_MAJOR_TICKLINE_ID, FID.ASSO_TYPE['measure']],
                 [FID.DRAWING_OBJECT_ID, FID.X_AXIS_OFFSET_ID, FID.ASSO_TYPE['measure']],
                 [FID.DRAWING_OBJECT_ID, FID.Y_AXIS_LABEL_ID, FID.ASSO_TYPE['relation']],
                 [FID.DRAWING_OBJECT_ID, FID.Y_AXIS_LINE_ID, FID.ASSO_TYPE['relation']],
                 [FID.DRAWING_OBJECT_ID, FID.Y_AXIS_MAJOR_TICKLABEL_ID, FID.ASSO_TYPE['measure']],
                 [FID.DRAWING_OBJECT_ID, FID.Y_AXIS_MAJOR_TICKLINE_ID, FID.ASSO_TYPE['measure']],
                 [FID.DRAWING_OBJECT_ID, FID.Y_AXIS_OFFSET_ID, FID.ASSO_TYPE['measure']],
                 [FID.DRAWING_OBJECT_ID, FID.LEGEND_TITLE_ID, FID.ASSO_TYPE['relation']],
                 [FID.DRAWING_OBJECT_ID, FID.LEGEND_SYMBOL_ID, FID.ASSO_TYPE['similarity']],
                 [FID.DRAWING_OBJECT_ID, FID.LEGEND_SYMBOL_ID, FID.ASSO_TYPE['measure']],

                 [FID.X_AXIS_LINE_ID, FID.X_AXIS_MAJOR_TICKLINE_ID, FID.ASSO_TYPE['relation']],
                 [FID.X_AXIS_LINE_ID, FID.X_AXIS_LABEL_ID, FID.ASSO_TYPE['relation']],
                 [FID.X_AXIS_OFFSET_ID, FID.X_AXIS_MAJOR_TICKLABEL_ID, FID.ASSO_TYPE['measure']],
                 [FID.X_AXIS_MAJOR_TICKLABEL_ID, FID.X_AXIS_MAJOR_TICKLINE_ID, FID.ASSO_TYPE['measure']],
                 [FID.Y_AXIS_LINE_ID, FID.Y_AXIS_MAJOR_TICKLINE_ID, FID.ASSO_TYPE['relation']],
                 [FID.Y_AXIS_LINE_ID, FID.Y_AXIS_LABEL_ID, FID.ASSO_TYPE['relation']],
                 [FID.Y_AXIS_OFFSET_ID, FID.Y_AXIS_MAJOR_TICKLABEL_ID, FID.ASSO_TYPE['measure']],
                 [FID.Y_AXIS_MAJOR_TICKLABEL_ID, FID.Y_AXIS_MAJOR_TICKLINE_ID, FID.ASSO_TYPE['measure']],
                 [FID.X_AXIS_LINE_ID, FID.Y_AXIS_LINE_ID, FID.ASSO_TYPE['similarity']],
                 [FID.LEGEND_TITLE_ID, FID.LEGEND_SYMBOL_ID, FID.ASSO_TYPE['relation']],
                 [FID.LEGEND_TITLE_ID, FID.LEGEND_TEXT_ID, FID.ASSO_TYPE['relation']],
                 [FID.LEGEND_SYMBOL_ID, FID.LEGEND_TEXT_ID, FID.ASSO_TYPE['measure']]]
    leveliso_asso = create_association(node_list, asso_list, FID.ASSO_TYPE)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(association_path, engine='xlsxwriter')

    # Write each dataframe to a different worksheet.
    levelone_asso.to_excel(writer, sheet_name='levelone')
    leveltwo_asso_x_axis.to_excel(writer, sheet_name='leveltwo_x_axis')
    leveltwo_asso_y_axis.to_excel(writer, sheet_name='leveltwo_y_axis')
    levelthree_asso_legend.to_excel(writer, sheet_name='levelthree_legend')
    levelthree_asso_x_tick.to_excel(writer, sheet_name='levelthree_x_tick')
    levelthree_asso_y_tick.to_excel(writer, sheet_name='levelthree_y_tick')
    leveliso_asso.to_excel(writer, sheet_name='leveliso')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()


if __name__ == '__main__':
    cwd = os.getcwd()

    figures_path = os.path.join(cwd, 'figure/matplotlib')
    line_chart_path = os.path.join(figures_path, 'Line_chart')
    svg_path = os.path.join(line_chart_path, 'svg')
    src_data_path = os.path.join(line_chart_path, 'src_data')

    png_path = os.path.join(line_chart_path, 'png')
    bbox_anno_path = os.path.join(line_chart_path, 'bbox_anno')
    asso_anno_path = os.path.join(line_chart_path, 'asso_anno')
    mkdir_safe([png_path, bbox_anno_path, asso_anno_path])

    FID.element_init()

    for idx in range(len(os.listdir(svg_path))):
        print(' >> Reading json and svg from: %s' % os.path.join(svg_path, 'Line_chart_%03d.svg' % idx))
        bboxes_dict, image = export_png_and_bbox(os.path.join(svg_path, 'Line_chart_%03d.svg' % idx),
                                                 os.path.join(png_path, 'Line_chart_%03d.png' % idx), driver=None)

        bboxes_dict = bboxes_postprocess(bboxes_dict)
        # from Show_bbox import show_bbox
        # show_bbox(bboxes_dict, image, bbox_png_path)

        with open(os.path.join(src_data_path, 'Line_chart_%03d.json' % idx), 'r') as infile:
            src_data = json.load(infile)

        annotation_data = export_annotation_bbox(bboxes_dict, src_data)
        with open(os.path.join(bbox_anno_path, 'Line_chart_%03d.json' % idx), 'w') as outfile:
            json.dump(annotation_data, outfile, indent=4)

        export_annotation_association(os.path.join(asso_anno_path, 'Line_chart_%03d.xlsx' % idx))
