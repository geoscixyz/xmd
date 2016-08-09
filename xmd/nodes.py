import markdown
import mdx_math


class Context(object):

    def __init__(self):
        self._things = {}

    def count(self, name):
        if name not in self._things:
            self._things[name] = 0
        self._things[name] += 1
        return self._things[name]


class XmdNode(object):

    def __init__(self, s, loc, raw):
        self.loc = loc
        self.raw = raw
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


class Command(XmdNode):

    def parse(self):
        self.name = self.raw[0][0]
        self.args = self.raw[0][1]
        self.content = self.raw[0][2]

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
        fignum = self.context.count(self.__class__.__name__)
        src = self.args[0].strip('"')
        inner = '    \n'.join([x.render() for x in self.content])
        inner = inner.strip('<p>').strip('</p>')
        html = (
            '<div class="figure">'
            '<img src="{src}">'
            '<div class="caption">'
            '<strong>Figure {num}:</strong>{html}'
            '</div>'
            '</div>'
        )
        return html.format(num=fignum, src=src, html=inner)


class Markdown(XmdNode):

    def render(self):
        return markdown.markdown(self.raw[0][0], extensions=[
            mdx_math.makeExtension(enable_dollar_delimiter=True)
        ])



def chooseCommand(s, loc, raw):
    if raw[0][0] == 'sidenote':
        return Sidenote(s, loc, raw)
    if raw[0][0] == 'figure':
        return Figure(s, loc, raw)
    return Command(s, loc, raw)
