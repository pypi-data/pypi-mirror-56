We know nothing about Github OH MY!


```python
import pandas, requests, requests_cache, operator, hvplot.pandas
requests_cache.install_cache('resident-demo')
s = pandas.Series({
    project: F"https://api.github.com/repos/{project}"
    for project in "ipython/ipython jupyter/notebook seatgeek/fuzzywuzzy".split()
})
```





<link rel="stylesheet" href="https://code.jquery.com/ui/1.10.4/themes/smoothness/jquery-ui.css">
<style>div.bk-hbox {
    display: flex;
    justify-content: center;
}

div.bk-hbox div.bk-plot {
    padding: 8px;
}

div.bk-hbox div.bk-data-table {
    padding: 20px;
}

div.hololayout {
  display: flex;
  align-items: center;
  margin: 0;
}

div.holoframe {
  width: 75%;
}

div.holowell {
  display: flex;
  align-items: center;
}

form.holoform {
  background-color: #fafafa;
  border-radius: 5px;
  overflow: hidden;
  padding-left: 0.8em;
  padding-right: 0.8em;
  padding-top: 0.4em;
  padding-bottom: 0.4em;
  box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
  border: 1px solid #e3e3e3;
}

div.holowidgets {
  padding-right: 0;
  width: 25%;
}

div.holoslider {
  min-height: 0 !important;
  height: 0.8em;
  width: 100%;
}

div.holoformgroup {
  padding-top: 0.5em;
  margin-bottom: 0.5em;
}

div.hologroup {
  padding-left: 0;
  padding-right: 0.8em;
  width: 100%;
}

.holoselect {
  width: 92%;
  margin-left: 0;
  margin-right: 0;
}

.holotext {
  padding-left:  0.5em;
  padding-right: 0;
  width: 100%;
}

.holowidgets .ui-resizable-se {
  visibility: hidden
}

.holoframe > .ui-resizable-se {
  visibility: hidden
}

.holowidgets .ui-resizable-s {
  visibility: hidden
}


/* CSS rules for noUISlider based slider used by JupyterLab extension  */

.noUi-handle {
  width: 20px !important;
  height: 20px !important;
  left: -5px !important;
  top: -5px !important;
}

.noUi-handle:before, .noUi-handle:after {
  visibility: hidden;
  height: 0px;
}

.noUi-target {
  margin-left: 0.5em;
  margin-right: 0.5em;
}
</style>







```python
g = s.apply(requests.get).apply(operator.methodcaller('json'))
g = g.apply(pandas.Series).set_index('id')
times = [x for x in g.columns if x.endswith('_at')]
g[times] = g[times].apply(pandas.to_datetime)
g = g.set_index(times, append=True)
g
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th>node_id</th>
      <th>name</th>
      <th>full_name</th>
      <th>private</th>
      <th>owner</th>
      <th>html_url</th>
      <th>description</th>
      <th>fork</th>
      <th>url</th>
      <th>forks_url</th>
      <th>...</th>
      <th>disabled</th>
      <th>open_issues_count</th>
      <th>license</th>
      <th>forks</th>
      <th>open_issues</th>
      <th>watchers</th>
      <th>default_branch</th>
      <th>organization</th>
      <th>network_count</th>
      <th>subscribers_count</th>
    </tr>
    <tr>
      <th>id</th>
      <th>created_at</th>
      <th>updated_at</th>
      <th>pushed_at</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>658518</td>
      <td>2010-05-10 04:46:06+00:00</td>
      <td>2019-10-30 14:51:26+00:00</td>
      <td>2019-10-30 05:08:44+00:00</td>
      <td>MDEwOlJlcG9zaXRvcnk2NTg1MTg=</td>
      <td>ipython</td>
      <td>ipython/ipython</td>
      <td>False</td>
      <td>{'login': 'ipython', 'id': 230453, 'node_id': ...</td>
      <td>https://github.com/ipython/ipython</td>
      <td>Official repository for IPython itself. Other ...</td>
      <td>False</td>
      <td>https://api.github.com/repos/ipython/ipython</td>
      <td>https://api.github.com/repos/ipython/ipython/f...</td>
      <td>...</td>
      <td>False</td>
      <td>1238</td>
      <td>{'key': 'other', 'name': 'Other', 'spdx_id': '...</td>
      <td>3900</td>
      <td>1238</td>
      <td>13837</td>
      <td>master</td>
      <td>{'login': 'ipython', 'id': 230453, 'node_id': ...</td>
      <td>3900</td>
      <td>830</td>
    </tr>
    <tr>
      <td>33653601</td>
      <td>2015-04-09 06:58:03+00:00</td>
      <td>2019-10-30 14:13:09+00:00</td>
      <td>2019-10-29 22:48:39+00:00</td>
      <td>MDEwOlJlcG9zaXRvcnkzMzY1MzYwMQ==</td>
      <td>notebook</td>
      <td>jupyter/notebook</td>
      <td>False</td>
      <td>{'login': 'jupyter', 'id': 7388996, 'node_id':...</td>
      <td>https://github.com/jupyter/notebook</td>
      <td>Jupyter Interactive Notebook</td>
      <td>False</td>
      <td>https://api.github.com/repos/jupyter/notebook</td>
      <td>https://api.github.com/repos/jupyter/notebook/...</td>
      <td>...</td>
      <td>False</td>
      <td>1672</td>
      <td>{'key': 'other', 'name': 'Other', 'spdx_id': '...</td>
      <td>2687</td>
      <td>1672</td>
      <td>6422</td>
      <td>master</td>
      <td>{'login': 'jupyter', 'id': 7388996, 'node_id':...</td>
      <td>2687</td>
      <td>317</td>
    </tr>
    <tr>
      <td>2019626</td>
      <td>2011-07-08 19:32:34+00:00</td>
      <td>2019-10-30 11:47:08+00:00</td>
      <td>2019-09-17 15:35:29+00:00</td>
      <td>MDEwOlJlcG9zaXRvcnkyMDE5NjI2</td>
      <td>fuzzywuzzy</td>
      <td>seatgeek/fuzzywuzzy</td>
      <td>False</td>
      <td>{'login': 'seatgeek', 'id': 447527, 'node_id':...</td>
      <td>https://github.com/seatgeek/fuzzywuzzy</td>
      <td>Fuzzy String Matching in Python</td>
      <td>False</td>
      <td>https://api.github.com/repos/seatgeek/fuzzywuzzy</td>
      <td>https://api.github.com/repos/seatgeek/fuzzywuz...</td>
      <td>...</td>
      <td>False</td>
      <td>62</td>
      <td>{'key': 'gpl-2.0', 'name': 'GNU General Public...</td>
      <td>668</td>
      <td>62</td>
      <td>6170</td>
      <td>master</td>
      <td>{'login': 'seatgeek', 'id': 447527, 'node_id':...</td>
      <td>668</td>
      <td>224</td>
    </tr>
  </tbody>
</table>
<p>3 rows × 72 columns</p>
</div>




```python
g.license.apply(pandas.Series).join(g, rsuffix='_').hvplot.bar('full_name', 'open_issues', invert=True, grid=True)
```




<div id='1443' style='display: table; margin: 0 auto;'>





  <div class="bk-root" id="4802f6ce-ee89-4dc9-ae1c-3754a5ecfb14" data-root-id="1443"></div>
</div>
<script type="application/javascript">(function(root) {
  function embed_document(root) {

  var docs_json = {"e296305f-59f5-4034-936e-1f73940cd58e":{"roots":{"references":[{"attributes":{"align":null,"below":[{"id":"1452","type":"LinearAxis"}],"center":[{"id":"1456","type":"Grid"},{"id":"1460","type":"Grid"}],"left":[{"id":"1457","type":"CategoricalAxis"}],"margin":null,"min_border_bottom":10,"min_border_left":10,"min_border_right":10,"min_border_top":10,"plot_height":300,"plot_width":700,"renderers":[{"id":"1479","type":"GlyphRenderer"}],"sizing_mode":"fixed","title":{"id":"1444","type":"Title"},"toolbar":{"id":"1466","type":"Toolbar"},"x_range":{"id":"1440","type":"Range1d"},"x_scale":{"id":"1448","type":"LinearScale"},"y_range":{"id":"1441","type":"FactorRange"},"y_scale":{"id":"1450","type":"CategoricalScale"}},"id":"1443","subtype":"Figure","type":"Plot"},{"attributes":{"text":"","text_color":{"value":"black"},"text_font_size":{"value":"12pt"}},"id":"1444","type":"Title"},{"attributes":{"active_drag":"auto","active_inspect":"auto","active_multi":null,"active_scroll":"auto","active_tap":"auto","tools":[{"id":"1442","type":"HoverTool"},{"id":"1461","type":"SaveTool"},{"id":"1462","type":"PanTool"},{"id":"1463","type":"WheelZoomTool"},{"id":"1464","type":"BoxZoomTool"},{"id":"1465","type":"ResetTool"}]},"id":"1466","type":"Toolbar"},{"attributes":{"callback":null,"renderers":[{"id":"1479","type":"GlyphRenderer"}],"tags":["hv_created"],"tooltips":[["full_name","@{full_name}"],["open_issues","@{open_issues}"]]},"id":"1442","type":"HoverTool"},{"attributes":{},"id":"1448","type":"LinearScale"},{"attributes":{},"id":"1450","type":"CategoricalScale"},{"attributes":{"bottom_units":"screen","fill_alpha":{"value":0.5},"fill_color":{"value":"lightgrey"},"left_units":"screen","level":"overlay","line_alpha":{"value":1.0},"line_color":{"value":"black"},"line_dash":[4,4],"line_width":{"value":2},"render_mode":"css","right_units":"screen","top_units":"screen"},"id":"1492","type":"BoxAnnotation"},{"attributes":{"fill_alpha":{"value":0.2},"fill_color":{"value":"#1f77b3"},"height":{"value":0.8},"line_alpha":{"value":0.2},"line_color":{"value":"black"},"right":{"field":"open_issues"},"y":{"field":"full_name"}},"id":"1478","type":"HBar"},{"attributes":{},"id":"1465","type":"ResetTool"},{"attributes":{"fill_alpha":{"value":0.1},"fill_color":{"value":"#1f77b3"},"height":{"value":0.8},"line_alpha":{"value":0.1},"line_color":{"value":"black"},"right":{"field":"open_issues"},"y":{"field":"full_name"}},"id":"1477","type":"HBar"},{"attributes":{},"id":"1453","type":"BasicTicker"},{"attributes":{},"id":"1493","type":"UnionRenderers"},{"attributes":{"fill_color":{"value":"#1f77b3"},"height":{"value":0.8},"right":{"field":"open_issues"},"y":{"field":"full_name"}},"id":"1476","type":"HBar"},{"attributes":{},"id":"1484","type":"CategoricalTickFormatter"},{"attributes":{"axis_label":"full_name","bounds":"auto","formatter":{"id":"1484","type":"CategoricalTickFormatter"},"major_label_orientation":"horizontal","ticker":{"id":"1458","type":"CategoricalTicker"}},"id":"1457","type":"CategoricalAxis"},{"attributes":{},"id":"1461","type":"SaveTool"},{"attributes":{"axis_label":"open_issues","bounds":"auto","formatter":{"id":"1482","type":"BasicTickFormatter"},"major_label_orientation":"horizontal","ticker":{"id":"1453","type":"BasicTicker"}},"id":"1452","type":"LinearAxis"},{"attributes":{"data_source":{"id":"1473","type":"ColumnDataSource"},"glyph":{"id":"1476","type":"HBar"},"hover_glyph":null,"muted_glyph":{"id":"1478","type":"HBar"},"nonselection_glyph":{"id":"1477","type":"HBar"},"selection_glyph":null,"view":{"id":"1480","type":"CDSView"}},"id":"1479","type":"GlyphRenderer"},{"attributes":{},"id":"1463","type":"WheelZoomTool"},{"attributes":{"dimension":1,"ticker":{"id":"1458","type":"CategoricalTicker"}},"id":"1460","type":"Grid"},{"attributes":{"callback":null,"data":{"full_name":["ipython/ipython","jupyter/notebook","seatgeek/fuzzywuzzy"],"open_issues":[1238,1672,62]},"selected":{"id":"1474","type":"Selection"},"selection_policy":{"id":"1493","type":"UnionRenderers"}},"id":"1473","type":"ColumnDataSource"},{"attributes":{"overlay":{"id":"1492","type":"BoxAnnotation"}},"id":"1464","type":"BoxZoomTool"},{"attributes":{},"id":"1482","type":"BasicTickFormatter"},{"attributes":{},"id":"1458","type":"CategoricalTicker"},{"attributes":{"callback":null,"factors":["ipython/ipython","jupyter/notebook","seatgeek/fuzzywuzzy"],"tags":[[["full_name","full_name",null]]]},"id":"1441","type":"FactorRange"},{"attributes":{},"id":"1474","type":"Selection"},{"attributes":{},"id":"1462","type":"PanTool"},{"attributes":{"source":{"id":"1473","type":"ColumnDataSource"}},"id":"1480","type":"CDSView"},{"attributes":{"callback":null,"end":1672.0,"reset_end":1672.0,"reset_start":0.0,"tags":[[["open_issues","open_issues",null]]]},"id":"1440","type":"Range1d"},{"attributes":{"ticker":{"id":"1453","type":"BasicTicker"}},"id":"1456","type":"Grid"}],"root_ids":["1443"]},"title":"Bokeh Application","version":"1.3.4"}};
  var render_items = [{"docid":"e296305f-59f5-4034-936e-1f73940cd58e","roots":{"1443":"4802f6ce-ee89-4dc9-ae1c-3754a5ecfb14"}}];
  root.Bokeh.embed.embed_items_notebook(docs_json, render_items);

  }
  if (root.Bokeh !== undefined) {
    embed_document(root);
  } else {
    var attempts = 0;
    var timer = setInterval(function(root) {
      if (root.Bokeh !== undefined) {
        embed_document(root);
        clearInterval(timer);
      }
      attempts++;
      if (attempts > 100) {
        console.log("Bokeh: ERROR: Unable to run BokehJS code because BokehJS library is missing");
        clearInterval(timer);
      }
    }, 10, root)
  }
})(window);</script>




```python
g
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th>node_id</th>
      <th>name</th>
      <th>full_name</th>
      <th>private</th>
      <th>owner</th>
      <th>html_url</th>
      <th>description</th>
      <th>fork</th>
      <th>url</th>
      <th>forks_url</th>
      <th>...</th>
      <th>disabled</th>
      <th>open_issues_count</th>
      <th>license</th>
      <th>forks</th>
      <th>open_issues</th>
      <th>watchers</th>
      <th>default_branch</th>
      <th>organization</th>
      <th>network_count</th>
      <th>subscribers_count</th>
    </tr>
    <tr>
      <th>id</th>
      <th>created_at</th>
      <th>updated_at</th>
      <th>pushed_at</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>658518</td>
      <td>2010-05-10 04:46:06+00:00</td>
      <td>2019-10-30 14:51:26+00:00</td>
      <td>2019-10-30 05:08:44+00:00</td>
      <td>MDEwOlJlcG9zaXRvcnk2NTg1MTg=</td>
      <td>ipython</td>
      <td>ipython/ipython</td>
      <td>False</td>
      <td>{'login': 'ipython', 'id': 230453, 'node_id': ...</td>
      <td>https://github.com/ipython/ipython</td>
      <td>Official repository for IPython itself. Other ...</td>
      <td>False</td>
      <td>https://api.github.com/repos/ipython/ipython</td>
      <td>https://api.github.com/repos/ipython/ipython/f...</td>
      <td>...</td>
      <td>False</td>
      <td>1238</td>
      <td>{'key': 'other', 'name': 'Other', 'spdx_id': '...</td>
      <td>3900</td>
      <td>1238</td>
      <td>13837</td>
      <td>master</td>
      <td>{'login': 'ipython', 'id': 230453, 'node_id': ...</td>
      <td>3900</td>
      <td>830</td>
    </tr>
    <tr>
      <td>33653601</td>
      <td>2015-04-09 06:58:03+00:00</td>
      <td>2019-10-30 14:13:09+00:00</td>
      <td>2019-10-29 22:48:39+00:00</td>
      <td>MDEwOlJlcG9zaXRvcnkzMzY1MzYwMQ==</td>
      <td>notebook</td>
      <td>jupyter/notebook</td>
      <td>False</td>
      <td>{'login': 'jupyter', 'id': 7388996, 'node_id':...</td>
      <td>https://github.com/jupyter/notebook</td>
      <td>Jupyter Interactive Notebook</td>
      <td>False</td>
      <td>https://api.github.com/repos/jupyter/notebook</td>
      <td>https://api.github.com/repos/jupyter/notebook/...</td>
      <td>...</td>
      <td>False</td>
      <td>1672</td>
      <td>{'key': 'other', 'name': 'Other', 'spdx_id': '...</td>
      <td>2687</td>
      <td>1672</td>
      <td>6422</td>
      <td>master</td>
      <td>{'login': 'jupyter', 'id': 7388996, 'node_id':...</td>
      <td>2687</td>
      <td>317</td>
    </tr>
    <tr>
      <td>2019626</td>
      <td>2011-07-08 19:32:34+00:00</td>
      <td>2019-10-30 11:47:08+00:00</td>
      <td>2019-09-17 15:35:29+00:00</td>
      <td>MDEwOlJlcG9zaXRvcnkyMDE5NjI2</td>
      <td>fuzzywuzzy</td>
      <td>seatgeek/fuzzywuzzy</td>
      <td>False</td>
      <td>{'login': 'seatgeek', 'id': 447527, 'node_id':...</td>
      <td>https://github.com/seatgeek/fuzzywuzzy</td>
      <td>Fuzzy String Matching in Python</td>
      <td>False</td>
      <td>https://api.github.com/repos/seatgeek/fuzzywuzzy</td>
      <td>https://api.github.com/repos/seatgeek/fuzzywuz...</td>
      <td>...</td>
      <td>False</td>
      <td>62</td>
      <td>{'key': 'gpl-2.0', 'name': 'GNU General Public...</td>
      <td>668</td>
      <td>62</td>
      <td>6170</td>
      <td>master</td>
      <td>{'login': 'seatgeek', 'id': 447527, 'node_id':...</td>
      <td>668</td>
      <td>224</td>
    </tr>
  </tbody>
</table>
<p>3 rows × 72 columns</p>
</div>




```python
g.unstack('id').stack('id')
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th>node_id</th>
      <th>name</th>
      <th>full_name</th>
      <th>private</th>
      <th>owner</th>
      <th>html_url</th>
      <th>description</th>
      <th>fork</th>
      <th>url</th>
      <th>forks_url</th>
      <th>...</th>
      <th>disabled</th>
      <th>open_issues_count</th>
      <th>license</th>
      <th>forks</th>
      <th>open_issues</th>
      <th>watchers</th>
      <th>default_branch</th>
      <th>organization</th>
      <th>network_count</th>
      <th>subscribers_count</th>
    </tr>
    <tr>
      <th>created_at</th>
      <th>updated_at</th>
      <th>pushed_at</th>
      <th>id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2010-05-10 04:46:06+00:00</td>
      <td>2019-10-30 14:51:26+00:00</td>
      <td>2019-10-30 05:08:44+00:00</td>
      <td>658518</td>
      <td>MDEwOlJlcG9zaXRvcnk2NTg1MTg=</td>
      <td>ipython</td>
      <td>ipython/ipython</td>
      <td>False</td>
      <td>{'login': 'ipython', 'id': 230453, 'node_id': ...</td>
      <td>https://github.com/ipython/ipython</td>
      <td>Official repository for IPython itself. Other ...</td>
      <td>False</td>
      <td>https://api.github.com/repos/ipython/ipython</td>
      <td>https://api.github.com/repos/ipython/ipython/f...</td>
      <td>...</td>
      <td>False</td>
      <td>1238.0</td>
      <td>{'key': 'other', 'name': 'Other', 'spdx_id': '...</td>
      <td>3900.0</td>
      <td>1238.0</td>
      <td>13837.0</td>
      <td>master</td>
      <td>{'login': 'ipython', 'id': 230453, 'node_id': ...</td>
      <td>3900.0</td>
      <td>830.0</td>
    </tr>
    <tr>
      <td>2011-07-08 19:32:34+00:00</td>
      <td>2019-10-30 11:47:08+00:00</td>
      <td>2019-09-17 15:35:29+00:00</td>
      <td>2019626</td>
      <td>MDEwOlJlcG9zaXRvcnkyMDE5NjI2</td>
      <td>fuzzywuzzy</td>
      <td>seatgeek/fuzzywuzzy</td>
      <td>False</td>
      <td>{'login': 'seatgeek', 'id': 447527, 'node_id':...</td>
      <td>https://github.com/seatgeek/fuzzywuzzy</td>
      <td>Fuzzy String Matching in Python</td>
      <td>False</td>
      <td>https://api.github.com/repos/seatgeek/fuzzywuzzy</td>
      <td>https://api.github.com/repos/seatgeek/fuzzywuz...</td>
      <td>...</td>
      <td>False</td>
      <td>62.0</td>
      <td>{'key': 'gpl-2.0', 'name': 'GNU General Public...</td>
      <td>668.0</td>
      <td>62.0</td>
      <td>6170.0</td>
      <td>master</td>
      <td>{'login': 'seatgeek', 'id': 447527, 'node_id':...</td>
      <td>668.0</td>
      <td>224.0</td>
    </tr>
    <tr>
      <td>2015-04-09 06:58:03+00:00</td>
      <td>2019-10-30 14:13:09+00:00</td>
      <td>2019-10-29 22:48:39+00:00</td>
      <td>33653601</td>
      <td>MDEwOlJlcG9zaXRvcnkzMzY1MzYwMQ==</td>
      <td>notebook</td>
      <td>jupyter/notebook</td>
      <td>False</td>
      <td>{'login': 'jupyter', 'id': 7388996, 'node_id':...</td>
      <td>https://github.com/jupyter/notebook</td>
      <td>Jupyter Interactive Notebook</td>
      <td>False</td>
      <td>https://api.github.com/repos/jupyter/notebook</td>
      <td>https://api.github.com/repos/jupyter/notebook/...</td>
      <td>...</td>
      <td>False</td>
      <td>1672.0</td>
      <td>{'key': 'other', 'name': 'Other', 'spdx_id': '...</td>
      <td>2687.0</td>
      <td>1672.0</td>
      <td>6422.0</td>
      <td>master</td>
      <td>{'login': 'jupyter', 'id': 7388996, 'node_id':...</td>
      <td>2687.0</td>
      <td>317.0</td>
    </tr>
  </tbody>
</table>
<p>3 rows × 72 columns</p>
</div>




```python
pandas.Series(range(10)).apply(range).apply(list).apply(pandas.Series).stack().unstack()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
      <th>8</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>2</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>3</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>4</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>3.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>5</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>3.0</td>
      <td>4.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>6</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>3.0</td>
      <td>4.0</td>
      <td>5.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>7</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>3.0</td>
      <td>4.0</td>
      <td>5.0</td>
      <td>6.0</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>8</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>3.0</td>
      <td>4.0</td>
      <td>5.0</td>
      <td>6.0</td>
      <td>7.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>9</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>3.0</td>
      <td>4.0</td>
      <td>5.0</td>
      <td>6.0</td>
      <td>7.0</td>
      <td>8.0</td>
    </tr>
  </tbody>
</table>
</div>


