import sys
import pyparsing as pp
import nodes

xmdObject = pp.Forward()


def createKwarg(z):
    return 'arg[{}, {}]'.format(z[0][0], z[0][1])


def createArg(z):
    return z[0][0]


def recurse(s, b, c):
    out = xmdObject.parseString(s[c[0]+1: c[2]-1])
    return [out]


variable_name = pp.Combine(
    pp.Word(pp.alphas + '_', exact=1) +
    pp.ZeroOrMore(pp.Word(pp.alphanums + '_', exact=1))
)

arg_string = pp.Group(
    pp.Suppress(pp.Word("'") | pp.Word('"')) +
    pp.Word("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&()*+,-./:;<=>?@[\]^_`{|}~ ") +
    pp.Suppress(pp.Word("'") | pp.Word('"'))
)

arg = pp.Group(
    pp.Word(pp.alphanums + '"\'/._-')
).setParseAction(createArg)

kwarg = pp.Group(
    variable_name + pp.Suppress('=') + pp.Word(pp.alphas)
).setParseAction(createKwarg)

command = (
    variable_name +
    pp.Group(pp.Optional(
        pp.originalTextFor(
            pp.nestedExpr(opener='(', closer=')')
        )
    ))
).setParseAction(nodes.CommandArguments)

Command = (
    pp.nestedExpr(opener='[>', closer=']', content=command) +
    pp.FollowedBy('{') +
    pp.originalTextFor(
        pp.nestedExpr(opener='{', closer='}')
    ).setParseAction(recurse)
).setParseAction(nodes.chooseCommand)

injector = pp.Group(
    pp.Suppress('{{') + pp.Word(pp.alphas) + pp.Suppress('}}')
)

unicodePrintables = u''.join(
    unichr(c) for c in xrange(sys.maxunicode)
    if not (
        unichr(c).isspace() or
        unichr(c) == '[' or
        unichr(c) == ']'
    )
)

chars = (
    "0123456789"
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "!\"#$%&'(){}*+,-./:;<=>?@\^_`|~ \r\n" +
    unicodePrintables
)

text_block = pp.Group(
    pp.OneOrMore(pp.Word(chars))
).setParseAction(nodes.Markdown)

xmdObject << pp.ZeroOrMore(Command | injector | text_block)


def transform(text):
    return xmdObject.parseString(text)


def render(text):

    if isinstance(text, pp.ParseResults):
        T = text   # already transformed
    else:
        T = transform(text)

    context = nodes.Context()
    for t in T:
        t.context = context
    out = '\n'.join([x.render() for x in T.asList()])
    return u"""<div class="xmd-container">\n{}\n</div>""".format(out)


def parse_file(name):
    with open(name, 'r') as f:
        T = transform(f.read())
    return render(T)
