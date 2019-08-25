//
//     Open svg in browser and save to image
//     @ Yixuan Wei
//     @ weiyx16@mails.tsinghua.edu.cn
//

const xml = '/home/weiyx/visualnet/test.svg';
// const {x, y, svg_width, svg_height} = document.documentElement.children[1].getBBox();
const image = new Image(1080, 648);
image.src = 'data:image/svg+xml;base64,' + window.btoa(xml);
image.onload = function() {
    var canvas = document.createElement('canvas');
    canvas.width = image.width;
    canvas.height = image.height;
    var context = canvas.getContext('2d');
    context.drawImage(image, 0, 0);

    var a = document.createElement('a');
    a.download = "image.png";
    a.href = canvas.toDataURL('image/png');
    document.body.appendChild(a);
    a.click();
}