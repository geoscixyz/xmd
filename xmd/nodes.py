from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future.utils import with_metaclass
import markdown
from . import mdx_math


class Context(object):

    def __init__(self):
        self._things = {}

    def count(self, name):
        if name not in self._things:
            self._things[name] = 0
        self._things[name] += 1
        return self._things[name]


class XmdNode(object):

    def __init__(self, string, location, ppinput):
        self.string = string
        self.location = location
        self.ppinput = ppinput
        self.parse()

    def parse(self):
        self.content = []
        pass

    @property
    def context(self):
        return getattr(self, '_context', None)

    @context.setter
    def context(self, val):
        for n in self.content:
            n.context = val
        self._context = val

    def parseArguments(self):
        # print(self.args)
        inner = self.command.args[0].strip('(').strip(')')
        args = [_.strip() for _ in inner.split(',')]
        # print(args)
        return args


class CommandArguments(object):
    def __init__(self, ppinput):
        # print('here', ppinput)
        self.ppinput = ppinput
        self.name = ppinput[0]
        self.args = ppinput[1]

    def __repr__(self):
        return "<{name} #{n}>".format(name=self.name, n=len(self.args))


class Command(XmdNode):

    def parse(self):
        self.command = self.ppinput[0][0]
        self.content = self.ppinput[1]

    def render(self):
        inner = '\n'.join([x.render() for x in self.content])
        return '<{name}>\n{html}\n</{name}>'.format(name=self.name, html=inner)


class Sidenote(Command):

    dagger = None   # "<sup>&Dagger;</sup>"

    def render(self):
        inner = '\n'.join([x.render() for x in self.content])
        return '<div class="sidenote">\n{html}\n</div>'.format(html=inner)


class Figure(Command):

    def render(self):
        args = self.parseArguments()
        fignum = self.context.count(self.__class__.__name__)
        src = args[0].strip('"').strip("'")
        inner = '    \n'.join([x.render() for x in self.content])
        inner = inner.strip('<p>').strip('</p>')
        html = (
            '<div class="figure">'
            '<img src="{src}">'
            '<div class="caption">'
            '<strong>Figure {num}:</strong> {html}'
            '</div>'
            '</div>'
        )
        return html.format(num=fignum, src=src, html=inner)


class Markdown(XmdNode):

    def render(self):
        return markdown.markdown(self.ppinput[0][0], extensions=[
            mdx_math.makeExtension(enable_dollar_delimiter=True)
        ])


def chooseCommand(string, location, ppinput):
    # ppinput = ppinput[0]
    # print('r: ', ppinput[0][0])
    if ppinput[0][0].name == 'sidenote':
        return Sidenote(string, location, ppinput)
    if ppinput[0][0].name == 'figure':
        return Figure(string, location, ppinput)
    return Command(string, location, ppinput)
