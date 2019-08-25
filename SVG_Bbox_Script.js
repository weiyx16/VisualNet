//
//     Fetch bbox of svg elements using webdriver + javascript
//     @ Yixuan Wei
//     @ weiyx16@mails.tsinghua.edu.cn
//


var bboxes = {};
const figure_show_bbox = document.documentElement.getBoundingClientRect();
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
// return bboxes;  // for use in python through web driver
