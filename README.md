# Usage to create visualization chart with bbox annotation in matplotlib

## Files

+ data_process.py: convert src data into drawable data (for current data: divided by country or indicator)  
  + [data source](http://datatopics.worldbank.org/world-develepment-indicators/)
  + data dir structure:  

```
.  
├── data   
│   ├── raw  
│   │    ├── WDI  
│   ├── Postprocess  
│   │    ├── WDI  
│   │    │    ├── Country  
│   │    │    ├── Indicator  
└──  
```

+ Figure_Python_Matplotlib.py: create svg file of visualization chart through Matplotlib and assign each element with a gid.  

```python
# usage example
fig_type = 'Pie_chart'
chart_batch_create(fig_type, csv_dir, chart_number=50)
```

+ SVG2JSON_Matplotlib.py: according to gid, use javascript+webdriver (chrome for now) to fetch bboxes from svg files.  

```python
# usage example
fig_type = 'Pie_chart'
export_annotation_png_batch(figures_path, fig_type)
```

+ Figure_elements_ID.py: global parameters for gid assignment  
+ SVG_Bbox_Script.js: javascript used to fetch bboxes and covert path of lines to bboxes for svg files.  
+ Show_bbox.py: test if bboxes are correct.