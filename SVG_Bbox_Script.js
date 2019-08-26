//
//     Fetch bbox of svg elements using webdriver + javascript
//     @ Yixuan Wei
//     @ weiyx16@mails.tsinghua.edu.cn
//


var bboxes = {};
var figure_type = '%s'; // need to assign from outside
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

        // fetch path for line element
        if (current_node.id.startsWith('%s')){  // need to assign from outside
            if (figure_type == 'Line_chart' || figure_type == 'Area_chart'){
                try {
                    bboxes[current_node.id + '_path'] = current_node.getElementsByTagName('path')[0].getAttribute('d');
                } catch(error) {
                    console.error(error);  // expected output: TypeError: Cannot read property 'getAttribute' of undefined
                }
            }
            if (figure_type == 'Scatter_chart') {
                // get path for line
                try {
                    bboxes[current_node.id + '_path'] = current_node.getElementsByTagName('path')[0].getAttribute('d');
                } catch(error) {
                    console.error(error);  // expected output: TypeError: Cannot read property 'getAttribute' of undefined
                }
                // get path for scatter dot
                try {
                    var dots = current_node.getElementsByTagName('g')[0];
                    var tmp_bbox = {};
                    for (var dot_num=0; dot_num<dots.childElementCount; dot_num++){
                        var tmp_SVGRect = dots.children[dot_num].getBBox();
                        tmp_bbox[current_node.id + '_Dot_' + dot_num] = [tmp_SVGRect['x'], tmp_SVGRect['y'],
                            tmp_SVGRect['width']+tmp_SVGRect['x'], tmp_SVGRect['height']+tmp_SVGRect['y']];
                    }
                    bboxes[current_node.id + '_Dot'] = tmp_bbox;
                } catch (error) {
                    console.error(error);  // expected output: TypeError: Cannot read property 'getAttribute' of undefined
                }
            }
        }

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
