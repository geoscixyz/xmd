import pyparsing as pp
import pprint
import nodes

mdObject = pp.Forward()


def createKwarg(z):
    return 'arg[{}, {}]'.format(z[0][0], z[0][1])


def createArg(z):
    return z[0][0]


def isNewLine(s):
    return s


def recurse(s, b, c):
    out = mdObject.parseString(s[c[0]+1: c[2]-1])
    return [out]


def asMarkdown(text):
    return markdown.markdown(text[0][0], extensions=extensions)


varName = pp.Combine(
    pp.Word(pp.alphas + '_', exact=1) +
    pp.ZeroOrMore(pp.Word(pp.alphanums + '_', exact=1))
)

kwarg = pp.Group(varName + pp.Suppress('=') + pp.Word(pp.alphas)).setParseAction(createKwarg)
arg = pp.Group(pp.Word(pp.alphanums + '"/._-')).setParseAction(createArg)

command = (
    pp.Suppress(">") + varName +
    pp.Group(pp.Optional(
        pp.Suppress('(') +
        pp.Optional(pp.delimitedList( arg )) +
        pp.Suppress(')')
    ))
)

Command = pp.Group(
    pp.Suppress('[') + command + pp.Suppress(']') + pp.FollowedBy('{') +
    pp.originalTextFor(pp.nestedExpr(opener='{', closer='}')).setParseAction(recurse)
).setParseAction(nodes.chooseCommand)

injector = pp.Group(pp.Suppress('{{') + pp.Word(pp.alphas) + pp.Suppress('}}'))

text_block = pp.Group(
    pp.OneOrMore(pp.Word("""0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'(){}*+,-./:;<=>?@\^_`|~ \n"""))
).setParseAction(nodes.Markdown)

mdObject << pp.ZeroOrMore(pp.MatchFirst([Command, injector, text_block]))


def parse(text):
    return mdObject.parseString(text)


def parse_file(name):
    with open(name, 'r') as f:
        p = parse(f.read())

    out = ''.join([x.render() for x in p.asList()])

    return out
