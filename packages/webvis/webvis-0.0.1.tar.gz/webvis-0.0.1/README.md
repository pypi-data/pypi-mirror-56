# Data visualization made easier

This is a project for interactive data visualization

It uses a dedicated web app with cards that display python variables.

Check out the notebooks folder for examples

## Quick start


```python
from webvis import Vis

vis = Vis(vis_port=7007)

vis.vars.test = "Hello World!"

# Open the browser on 7007 port 
vis.show()
```

Then change the name in card to "test" viola!

The values are updated dynamically, a separate thread is created that checks the changes.


values can be matplotlib figures, 1-d and 2-d arrays,
and even bokeh is supported!
