import markdown
import mdx_math

extensions = [mdx_math.makeExtension(enable_dollar_delimiter=True)]


class XmdNode(object):

    def __init__(self, s, loc, raw):
        self.loc = loc
        self.raw = raw
        self.parse()

    def parse(self):
        pass


class Command(XmdNode):

    def parse(self):
        self.name = self.raw[0][0]
        self.args = self.raw[0][1]
        self.content = self.raw[0][2]

    def render(self):
        inner = '    \n'.join([x.render() for x in self.content])

        return '<{name}>\n    {html}\n</{name}>'.format(name=self.name, html=inner)


class Sidenote(Command):

    dagger = None # "<sup>&Dagger;</sup>"

    def render(self):
        inner = '    \n'.join([x.render() for x in self.content])
        return '<div class="sidenote">\n    {html}\n</div>'.format(html=inner)


class Figure(Command):

    def render(self):
        src = self.args[0].strip('"')
        inner = '    \n'.join([x.render() for x in self.content])
        inner = inner.strip('<p>').strip('</p>')
        o = '<div class="figure"><img src="{src}"><div class="caption"><strong>Figure:</strong> {html}</div></div>'.format(src=src, html=inner)
        return o


def chooseCommand(s, loc, raw):
    if raw[0][0] == 'sidenote':
        return Sidenote(s, loc, raw)
    if raw[0][0] == 'figure':
        return Figure(s, loc, raw)
    return Command(s, loc, raw)


class Markdown(XmdNode):

    def render(self):
        return markdown.markdown(self.raw[0][0], extensions=extensions)
