#!/usr/bin/env python3

import unittest
from unittest.mock import patch

from srtmerger.main import create_parser, parse_subtitle_spec


class TestSubtitleMerger(unittest.TestCase):
    def setUp(self):
        self.parser = create_parser()

    def test_parse_subtitle_spec_basic(self):
        """Test parsing basic subtitle specification."""
        config = parse_subtitle_spec("file.srt")
        self.assertEqual(config.file_path, "file.srt")
        self.assertIsNone(config.encoding)
        self.assertIsNone(config.color)
        self.assertFalse(config.top)

    def test_parse_subtitle_spec_full(self):
        """Test parsing subtitle specification with all options."""
        config = parse_subtitle_spec("file.srt:encoding=utf-8:color=yellow:top")
        self.assertEqual(config.file_path, "file.srt")
        self.assertEqual(config.encoding, "utf-8")
        self.assertEqual(config.color, "yellow")
        self.assertTrue(config.top)

    def test_parse_subtitle_spec_partial(self):
        """Test parsing subtitle specification with some options."""
        config = parse_subtitle_spec("file.srt:color=blue:top")
        self.assertEqual(config.file_path, "file.srt")
        self.assertIsNone(config.encoding)
        self.assertEqual(config.color, "blue")
        self.assertTrue(config.top)

    def test_cli_basic(self):
        """Test basic CLI usage."""
        test_args = ["file1.srt", "file2.srt:encoding=utf-8:color=yellow"]
        with patch("sys.argv", ["srt-merger"] + test_args):
            args = self.parser.parse_args()
            self.assertEqual(args.subtitles, test_args)
            self.assertIsNone(args.default_encoding)
            self.assertIsNone(args.default_color)

    def test_cli_with_defaults(self):
        """Test CLI with default options."""
        test_args = [
            "-E",
            "utf-8",
            "-C",
            "white",
            "file1.srt:color=yellow",
            "file2.srt:top",
        ]
        with patch("sys.argv", ["srt-merger"] + test_args):
            args = self.parser.parse_args()
            self.assertEqual(len(args.subtitles), 2)
            self.assertEqual(args.default_encoding, "utf-8")
            self.assertEqual(args.default_color, "white")

    @patch("srtmerger.main.Merger")
    def test_main_integration(self, MockMerger):
        """Test main function integration."""
        mock_merger = MockMerger.return_value
        test_args = [
            "-E",
            "utf-8",
            "-C",
            "white",
            "file1.srt:color=yellow",
            "file2.srt:top",
        ]

        with patch("sys.argv", ["srtmerger"] + test_args):
            from srtmerger.main import main

            main()

            # Verify Merger was initialized
            MockMerger.assert_called_once()

            # Verify add() was called for each subtitle
            self.assertEqual(mock_merger.add.call_count, 2)

            # Verify merge() was called
            mock_merger.merge.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)
