from __future__ import print_function
import unittest
from xmd.parser import command
from xmd.parser import variable_name
import pyparsing as pp


def parse_arg_type(string):
    if string in ('True', 'False'):
        return string == 'True'
    try:
        return int(string)
    except ValueError:
        pass
    try:
        return float(string)
    except ValueError:
        pass
    if string.startswith("'") and string.endswith("'"):
        return string.strip("'")
    if string.startswith('"') and string.endswith('"'):
        return string.strip('"')
    if string.startswith("'''") and string.endswith("'''"):
        return string.strip("'''")
    if string.startswith('"""') and string.endswith('"""'):
        return string.strip('"""')
    raise ValueError('Could not parse: {}'.format(string))


def parse_arg_list(string):
    pass


class ParsingComponents(unittest.TestCase):

    def test_variable_name(self):
        # These are fine.
        variable_name.parseString('abc')
        variable_name.parseString('abc_')
        variable_name.parseString('_abc1')
        variable_name.parseString('Abc')
        # These are not.
        self.assertRaises(pp.ParseException, variable_name.parseString, '1abc')

    def test_arg_type(self):
        assert parse_arg_type('True') is True
        assert parse_arg_type('False') is False
        assert parse_arg_type('1') is 1
        assert parse_arg_type('1.') is not 1
        assert parse_arg_type('1.') == 1.0
        assert parse_arg_type('"1."') == '1.'
        assert parse_arg_type("'1.'") == '1.'
        self.assertRaises(ValueError, parse_arg_type, '1."')

    # def test_kwarg(self):
    #     kwarg.parseString('asdf=a')

    # def test_arg_string(self):
    #     arg_string.parseString("'as5_df'")
    #     arg_string.parseString('"asdf[]"')
    #     arg_string.parseString('"asdf!"')
    #     arg_string.parseString('"asdf.png"')

    # def test_arg_string_quotable(self):
    #     self.assertRaises(pp.ParseException, arg_string.parseString, "asdf'")
    #     self.assertRaises(pp.ParseException, arg_string.parseString, 'asdf"')
    #     self.assertRaises(pp.ParseException, arg_string.parseString, "'asdf")
    #     self.assertRaises(pp.ParseException, arg_string.parseString, '"asdf')

    # def test_arg_int(self):
    #     arg_int.parseString("1")
    #     arg_int.parseString("1567890")
    #     # print(arg_int.parseString("1.0"))
    #     self.assertRaises(pp.ParseException, arg_int.parseString, "01")
    #     # self.assertRaises(pp.ParseException, arg_int.parseString, "1.0")
    #     self.assertRaises(pp.ParseException, arg_int.parseString, "abc")

    # def test_arg_float(self):
    #     print(arg_float.parseString("1.0"))
    #     print(arg_float.parseString("1.0eE02"))
    #     self.assertRaises(pp.ParseException, arg_float.parseString, "abc")



if __name__ == '__main__':
    unittest.main()
    # print(pp.printables)
