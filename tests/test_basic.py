import unittest
import xmd


sidenote = """
[>sidenote]{This is a sidenote}
"""

sidenote_math = """
[>sidenote]{Math inside a sidenote!! $m^{a}_{th}$}
"""


class Basic(unittest.TestCase):

    def test_sidenote(self):
        nodes = xmd.transform(sidenote)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].__class__.__name__, 'Sidenote')
        render = nodes[0].render()
        assert 'class="sidenote"' in render
        assert 'This is a sidenote' in render

    def test_sidenote_math(self):
        nodes = xmd.transform(sidenote_math)
        render = nodes[0].render()
        assert 'class="sidenote"' in render
        assert 'script type="math/tex"' in render
        assert 'm^{a}_{th}' in render


if __name__ == '__main__':
    unittest.main()
