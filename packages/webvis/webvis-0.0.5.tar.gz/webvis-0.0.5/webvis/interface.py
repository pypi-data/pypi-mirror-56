import json
import numpy as np
#from . import helpers as h
import matplotlib
import mpld3
try:
    import matplotlib
    import mpld3
    #mpld3 hack
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            import numpy as np
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return json.JSONEncoder.default(self, obj)
    from mpld3 import _display
    _display.NumpyEncoder = NumpyEncoder
    import bokeh
except Exception as e:
    print(e)

def is_mpl(val):
    try:
        return isinstance(val, matplotlib.figure.Figure)
    except Exception as e:
        return False
def is_bokeh(val):
    try:
        return isinstance(val,bokeh.model.Model) or isinstance(val,bokeh.document.document.Document)
    except Exception as e:
        return False


def get_var(val, params):
    """
    Val: some value from user
    params: dict of params from frontend
    """
    if is_bokeh(val):
        ret = bokeh.embed.file_html(val, bokeh.resources.Resources('cdn'))
        type_ = 'mpl'
    elif is_mpl(val):
        ret = mpld3.fig_to_html(val)
        type_ = 'mpl'
    elif type(val)==np.ndarray:
        sh = val.shape
        if len(sh) >= 2:
            if sh[0]>10 and sh[1]>10:
                alpha = np.ones(list(sh[:2])+[1])*255
                if len(sh)==2:
                    val = val.reshape(sh[0],-1,1)
                    val = np.concatenate((val,val,val,alpha),axis = -1)
                if len(sh)==3:
                    val = np.concatenate((val,alpha), axis=-1)
                val = val.flatten()
                ret = list(sh[:2]) + val.tolist()
                type_='img'

        else:
            val = val.tolist()
            ret = val
            type_ = 'raw'
    else:
        ret = val
        type_ = 'raw'

    msg = {'args':params['varname'],
           'value':ret,
           'type':type_
          }
    return json.dumps(msg)
