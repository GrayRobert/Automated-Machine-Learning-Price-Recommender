from bokeh.plotting import figure, show, output_file
from bokeh.models import Line, ColumnDataSource, LinearAxis
from bokeh.embed import components, json_item
import json

class ScatterPlotService():

    # CONSTRUCTOR
    def __init__(self, testing_target, predictions):
        self.x = testing_target
        self.y = predictions

    def getScatterPlot(self):
        x = self.x
        y = self.y

        TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,"

        p = figure(tools=TOOLS, plot_width=500, 
                plot_height=300)

        p.scatter(x, y,
                fill_color='#6666ff', fill_alpha=0.3,
                line_color="#333399")

        p.line([x.min(), x.max()], [x.min(), x.max()],line_color="#666699", line_width=4, line_dash='dashed')

        p.toolbar.logo = None

        jsonified = json.dumps(json_item(p, "scatter-plot"))

        return jsonified