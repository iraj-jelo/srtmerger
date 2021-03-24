#!/usr/bin/env python
import unittest
import os

from main import Merger


class TestSrtMerger(unittest.TestCase):
    filename = '_test.srt'

    def test_merge(self):
        merger = Merger(output_name=self.filename, output_encoding="utf-16-le")
        merger.add('./test_assets/en.srt') # utf8 as default codec, white as default color
        merger.add('./test_assets/fa.srt', color="yellow", codec="cp1256", top=True)
        merger.merge()
        self.assertTrue(os.path.isfile(self.filename))

    def test_output_content(self):
        with open(self.filename, encoding='utf-16-le') as f:
            lines = f.readlines()
            self.assertTrue(os.path.isfile(self.filename))
            self.assertEqual(len(lines), 7819)
            self.assertEqual(lines[3091], "You can't cheat them.\n")
            self.assertEqual(lines[7764], '<font color="#FFFFFF">You want to stay here\n')

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.filename):
            os.remove(cls.filename)


if __name__ == '__main__':
    unittest.main()