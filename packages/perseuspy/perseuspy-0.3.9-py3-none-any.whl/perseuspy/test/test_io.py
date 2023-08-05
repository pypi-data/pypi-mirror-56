from unittest import TestCase, main
from os import path
from io import StringIO
from perseuspy import pd
import numpy as np

TEST_DIR = path.dirname(__file__)

def to_string(df, **kwargs):
    out = StringIO()
    df.to_perseus(out, **kwargs)
    out.seek(0)
    return ''.join(out.readlines())

def type_row(df, **kwargs):
    lines = to_string(df, **kwargs).splitlines()
    for line in lines:
        if line.startswith('#!{Type}'):
            return line.strip()
    return ''

class TestReading(TestCase):
    def test_reading_example1(self):
        df = pd.read_perseus(path.join(TEST_DIR, 'matrix.txt'))
        self.assertIsNot(df, None)
        self.assertIsNot(to_string(df), '')
        self.assertEqual('#!{Type}' + (15 * 'E\t') + 'T', type_row(df))

    def test_reading_example2(self):
        df = pd.read_perseus(path.join(TEST_DIR, 'matrix2.txt'))
        self.assertIsNot(df, None)
        self.assertIsNot(to_string(df), '')

    def test_reading_example3(self):
        df = pd.read_perseus(path.join(TEST_DIR, 'matrix3.txt'))
        self.assertIsNot(df, None)
        self.assertIsNot(to_string(df), '')
        self.assertEqual('#!{Type}' + (3 * 'E\t') + 'C',
                '\t'.join(type_row(df).split('\t')[:4]))

    def test_reading_numerical_annotation_row(self):
        df = pd.read_perseus(path.join(TEST_DIR, 'matrix5.txt'))
        self.assertIsNot(df, None)
        self.assertIsNot(to_string(df), '')
        self.assertEqual('#!{C:Quantity1}1.0\t2.0\t3.0\tnan\tnan\tnan\tnan\tnan\tnan\tnan\tnan\tnan\tnan\tnan',
                to_string(df).splitlines()[2])
    
    def test_reading_multi_numeric_columns(self):
        df = pd.read_perseus(path.join(TEST_DIR, 'matrix4.txt'))
        self.assertIsNot(df, None)
        self.assertEqual([1,2,3], df.values[0][0])
        self.assertEqual('1.0;2.0;3.0', to_string(df).splitlines()[-1])
        self.assertEqual("#!{Type}M", type_row(df))

    def test_inferring_and_setting_main_columns(self):
        df = pd.DataFrame({'a' : [2,3], 'b': [1,2], 'c': ['a','b'], 'd': [3,4]})
        self.assertEqual('#!{Type}E\tE\tT\tN', type_row(df))
        self.assertEqual('#!{Type}N\tE\tT\tE', type_row(df, main_columns={'b','d'}))

    def test_writing_empty_table_should_have_all_columns(self):
        df = pd.DataFrame(columns=pd.Index(['Node'], name='Column Name'))
        self.assertEqual(1, len(df.columns))
        self.assertEqual('Column Name', df.columns.name)
        df_str = to_string(df)
        self.assertEqual('Node\n#!{Type}T\n', df_str, df_str)

    def test_write_bool_column_as_categorical(self):
        df = pd.DataFrame(columns=pd.Index(['Significant'], name='Column Name'))
        df['Significant'] = [True, False, True, True]
        self.assertEqual(df.dtypes[0], np.dtype('bool'))
        df_str = to_string(df)
        self.assertEqual('Significant\n#!{Type}C\n+\n""\n+\n+\n', df_str, df_str)
        df_str = to_string(df, convert_bool_to_category=False)
        self.assertEqual('Significant\n#!{Type}C\nTrue\nFalse\nTrue\nTrue\n', df_str, df_str)

if __name__ == '__main__':
    main()
