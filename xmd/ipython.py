import os


def in_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False


def set_style():
    if not in_ipython():
        return

    from IPython.display import HTML, display

    with open(os.sep.join(__file__.split(os.sep)[:-1] + ['xmd.css'])) as f:
        style = (
            '<style type="text/css">'
            '{}'
            '</style>'.format(f.read())
        )

    display(HTML(style))
