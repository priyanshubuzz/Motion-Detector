from bokeh.plotting import figure
from bokeh.io import output_file, show
from motiondetector import df
from bokeh.models import HoverTool, ColumnDataSource
from datetime import datetime as dt

#Note - scale_mode in figure represents responsive=True in new bokeh.
f = figure(height=100, width=500, sizing_mode="scale_width", x_axis_type="datetime")
f.yaxis.minor_tick_line_color = None
f.xgrid.grid_line_color = None
f.ygrid.grid_line_color = None
f.title.text = "Motion Graph"
f.title.text_font_size = "25px"
f.title.align = "center"

#Adding String version of Start and End column which is datetime object
#Bcoz our HoverTool can't read datetime data
df["Start_String"] = df["Start"].dt.strftime(r"%d-%m-%Y %H:%M:%S")
df["End_String"] = df["End"].dt.strftime(r"%d-%m-%Y %H:%M:%S")

#Converting DF Series to CDS object 
#Since hovertool can't access series datatype.
cds = ColumnDataSource(df)

#drawing quadrant in figure object
f.quad(left="Start", right="End", bottom=0, top=1, source=cds, color="#ffae42", alpha=0.5)
#Note - Giving CDS data to plotting bcoz hovertool takes its data source
#And again it wants Cds so....

hover = HoverTool(tooltips = [("Start" , "@Start_String"), ("End", "@End_String")])
f.add_tools(hover)

output_file("Graph.html")
show(f)