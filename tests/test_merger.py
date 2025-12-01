#!/usr/bin/env python
import unittest
import os
from pathlib import Path

from srtmerger.merger import Merger


class TestSrtMerger(unittest.TestCase):
    test_assets_dir = Path(__file__).parent / "test_assets"
    filename = test_assets_dir / "test_ok.srt"

    def test_merge(self):
        merger = Merger(output_path=self.filename, output_encoding="utf-16-le")
        merger.add(
            self.test_assets_dir / "en.srt"
        )  # utf8 as default codec, white as default color
        merger.add(
            self.test_assets_dir / "fa.srt", color="yellow", encoding="cp1256", top=True
        )
        merger.merge()
        self.assertTrue(os.path.isfile(self.filename))

    def test_output_content(self):
        with open(self.filename, encoding="utf-16-le") as f:
            lines = f.readlines()
            self.assertTrue(os.path.isfile(self.filename))
            self.assertEqual(len(lines), 4232)
            self.assertEqual(lines[3091], "00:33:43,828 --> 00:33:46,796\n")
            self.assertEqual(lines[4228], "00:51:49,381 --> 00:51:59,286\n")

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.filename):
            os.remove(cls.filename)
            print(f'\n"{cls.filename}" was removed successfully.')


if __name__ == "__main__":
    unittest.main()
