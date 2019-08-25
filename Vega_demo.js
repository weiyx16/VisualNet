var vega = require('vega');
var fs = require('fs');
var json_file = require('./Vega.json');

// create a new view instance for a given Vega JSON spec
var view = new vega
  .View(vega.parse(json_file))
  .renderer('none')
  .initialize();

// generate static PNG file from chart
view
  .toCanvas()
  .then(function (canvas) {
    // process node-canvas instance for example, generate a PNG stream to write var
    // stream = canvas.createPNGStream();
    console.log('Writing PNG to file...');
    fs.writeFile('stackedBarChart.png', canvas.toBuffer());
  })
  .catch(function (err) {
    console.log("Error writing PNG to file:");
    console.error(err);
  });

// generate a static SVG image
view.toSVG()
  .then(function(svg) {
    // process svg string
    console.log('Writing SVG to file...')
  })
  .catch(function(err) {
      console.log("Error writing PNG to file:");
      console.error(err);
  });