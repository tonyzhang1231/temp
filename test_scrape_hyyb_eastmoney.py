import unittest
# from scrape_hyyb_eastmoney import *
from utils import *
import os, sys


""" unittest doc
https://docs.python.org/3/library/unittest.html
"""

# class TestStringMethods(unittest.TestCase):

#     def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')

#     def test_isupper(self):
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.isupper())

#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)

url = 'http://data.eastmoney.com/report/hyyb.html'
# 


class TestBasicMethods(unittest.TestCase):

    # def test_get_html_text(self):
    #     html = get_html_text(url, "GB2312")
    #     self.assertIsNotNone(html)
    #     soup = BeautifulSoup(html, 'html.parser')
    #     self.assertIsNotNone(soup)

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_maybe_download_file(self):
        pass

    def test_create_remove_dir_file_if_not_exists(self):
        create_file_if_not_exists("./tmp_file.txt")
        self.assertTrue(os.path.exists("./tmp_file.txt"))
        remove_file_if_exists("./tmp_file.txt")
        self.assertFalse(os.path.exists("./tmp_file.txt"))

        create_dir_if_not_exists("./abc")
        self.assertTrue(os.path.exists("./abc"))
        create_file_if_not_exists("./abc/tmp_file.txt")

        with self.assertRaises(OSError):
            remove_dir_if_exists("./abc", force=False)

        remove_dir_if_exists("./abc", force=True)
        self.assertFalse(os.path.exists("./abc"))

        # self.assertFalse(os.path.exists("./abc"))

if __name__ == '__main__':
    unittest.main()



# command line
# python -m unittest -v test_scrape_hyyb_eastmoney.py

# python 3 unittest module document
# https://docs.python.org/3/library/unittest.html#classes-and-functions
