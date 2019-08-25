import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
import pandas as pd
import os
from utils import utils

'''
DIVERSITY: https://plot.ly/python/plotly-fundamentals/
'''

# change renderer here
# See: https://plot.ly/python/renderers/
# png_renderer = pio.renderers["png"]
# png_renderer.width = 500
# png_renderer.height = 500
# pio.renderers.default = "png"

# possible type:
#  waterfall volume violin table surface sunburst splom scatterternary scatterpolar scattermapbox
#  sattergl scattergeo scattercarpet scatter3d scatter sankey pointcloud pie parcoords parcats
#  ohlc mesh3d isosurface indicator histogram2d histogram heatmap funnelarea funnel densitymapbox
#  contourcarpet contour cone choroplethmapbox carpet candlestick box barpolar bar area layout

# create and display plots
# See: https://plot.ly/python/creating-and-updating-figures/
# one way:
fig = go.Figure(
    data=[go.Bar(x=[1, 2, 3], y=[1, 3, 2])],
    layout_title_text="A Figure Displayed with fig.show()"
)
# fig.show()  # fig.show(renderer="png", width=800, height=300)

# another way:
fig = go.Figure({
    "data": [{"type": "bar",
              "x": [1, 2, 3],
              "y": [1, 3, 2]}],
    "layout": {"title": {"text": "A Bar Chart"}}
})
# fig.show()

# another way:
N = 100
x = np.random.rand(N)
y = np.random.rand(N)
colors = np.random.rand(N)
sz = np.random.rand(N) * 30

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=x,
    y=y,
    mode="markers",
    marker=go.scatter.Marker(
        size=sz,
        color=colors,
        opacity=0.6,
        colorscale="Viridis"
    )
))

# fig.show()

# another way:
# fig = {
#     "data": [{"type": "bar",
#               "x": [1, 2, 3],
#               "y": [1, 3, 2]}],
#     "layout": {"title": {"text": "A Bar Chart"}}
# }
# pio.show(fig)


# save to file
# See: https://plot.ly/python/static-image-export/
save_dir = './figure/plotly'
utils.mkdir_save(save_dir)
fig.write_image(os.path.join(save_dir, "fig1.svg"))  # support png,jpeg,webp,svg,pdf,eps

# save as graph objects
img_bytes = fig.to_image(format="png", width=600, height=350, scale=2)
# show in Ipython
# from IPython.display import Image
# Image(img_bytes)
# or pio.write_image / to_image
