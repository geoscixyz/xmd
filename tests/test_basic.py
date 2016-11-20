from __future__ import print_function
import unittest
import xmd


sidenote = """
[>sidenote]{This is a sidenote}
"""

sidenote_math = """
[>sidenote]{Math inside a sidenote!! $m^{a}_{th}$}
"""

paragraph = """
Simple paragraph.

* point the first
"""

figures = """

[>figure('a_figure.png', numbered=True)]{the figure caption}

"""

weird = "\r\n## DC resistivity \r\n  [>sidenote]{\r\n[>figure(https://raw.githubusercontent.com/simpeg/tle-finitevolume/master/images/DCSurvey.png)]{\r\n        Setup of a DC resistivity survey.\r\n    }\r\n}\r\n\r\n\r\nDC resistivity surveys obtain"


class Basic(unittest.TestCase):

    def test_sidenote(self):
        nodes = xmd.transform(sidenote)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].__class__.__name__, 'Sidenote')
        render = xmd.render(nodes)
        assert 'class="sidenote"' in render
        assert 'This is a sidenote' in render

    def test_sidenote_math(self):
        nodes = xmd.transform(sidenote_math)
        render = xmd.render(nodes)
        assert 'class="sidenote"' in render
        assert 'script type="math/tex"' in render
        assert 'm^{a}_{th}' in render

    def test_paragraph(self):
        render = xmd.render(paragraph)
        for tag in ('p', 'ul', 'li'):
            assert '<{}>'.format(tag) in render
            assert '</{}>'.format(tag) in render

    # def test_figures(self):
    #     render = xmd.render(figures)
    #     print(render)


    def test_returns(self):
        render = xmd.render(weird)
        print(render)




if __name__ == '__main__':
    unittest.main()
