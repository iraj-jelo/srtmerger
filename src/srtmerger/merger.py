#!/usr/bin/env python
# Author: Iraj Jelodari

import logging
import codecs
import re
import enum
from pathlib import Path

from .utils import time_to_timestamp

# \r (Carriage Return) → moves the cursor to the beginning of the line without advancing to the next line
CR = "\r"

# \n (Line Feed) → moves the cursor down to the next line without returning to the beginning of the line
# — In a *nix environment \n moves to the beginning of the line.
LF = "\n"

LF_AS_BYTE = b"\n"

EOL = "\r\n"  # \r\n (End Of Line) → a combination of \r and \n

TIMECODES_PATTERN = (
    r"\d{1,2}:\d{1,2}:\d{1,2},\d{1,5} --> \d{1,2}:\d{1,2}:\d{1,2},\d{1,5}[\r\n]*"
)

logging.basicConfig(format="")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Color(enum.StrEnum):
    RED = "#FF0000"
    DARK_RED = "#8B0000"
    CRIMSON = "#DC143C"
    ORANGE = "#FFA500"
    DARK_ORANGE = "#FF8C00"
    ORANGE_RED = "#FF4500"
    YELLOW = "#FFFF00"
    GOLD = "#FFD700"
    LIGHT_YELLOW = "#FFFFE0"
    GREEN = "#008000"
    LIME = "#00FF00"
    LIGHT_GREEN = "#90EE90"
    CYAN = "#00FFFF"
    DARK_CYAN = "#008B8B"
    LIGHT_CYAN = "#E0FFFF"
    BLUE = "#0000FF"
    DARK_BLUE = "#00008B"
    LIGHT_BLUE = "#ADD8E6"
    WHITE = "#FFFFFF"
    GRAY = "#808080"
    BLACK = "#000000"


class SrtParser:
    """
    A parser for SRT (SubRip) subtitle files.

    This class provides utilities to parse and manipulate SRT subtitle files.
    SRT files contain subtitle entries with the following structure:
    - Sequential Number: An integer indicating the subtitle's order
    - Timecodes: Start and end times in format HH:MM:SS,mmm --> HH:MM:SS,mmm
    - Subtitle Text: The actual text content (can span multiple lines)
    - Blank Line: Separates individual subtitle entries

    Methods:
        parse_timecodes: Extracts and returns the beginning and ending times from a timecode line
        parse_subtitle_entry: Parses a complete subtitle entry into its components (number, timecodes, and text)
        split_subtitle: Splits raw subtitle content by separating sequential numbers and timecode lines
    """

    def parse_timecodes(self, content):
        """Parse timecodes lines into begining time and end time"""
        PATTERN = r"(?P<begin>\d{1,2}:\d{1,2}:\d{1,2},\d{1,5})\s-->\s(?P<end>\d{1,2}:\d{1,2}:\d{1,2},\d{1,5})"
        match = re.search(PATTERN, content, re.MULTILINE | re.DOTALL | re.VERBOSE)
        return match.group("begin"), match.group("end")

    def parse_subtitle_entry(self, content):
        """Parse a subtitle entry (containing sequential number, timecodes and text) into sequential number, timecodes and text"""
        PATTERN = (
            r"(\d{1,2}:\d{1,2}:\d{1,2},\d{1,5}\s-->\s\d{1,2}:\d{1,2}:\d{1,2},\d{1,5})"
        )
        return re.split(PATTERN, content, flags=re.MULTILINE | re.DOTALL | re.VERBOSE)

    def split_subtitle(self, content):
        """Split a subtitle content by its sequential number and timecodes lines"""
        PATTERN = r"(\d*[\r\n]*\d{1,2}:\d{1,2}:\d{1,2},\d{1,5}\s-->\s\d{1,2}:\d{1,2}:\d{1,2},\d{1,5})"
        return re.split(PATTERN, content, flags=re.MULTILINE | re.DOTALL | re.VERBOSE)


class Merger:
    """
    SRT Merger allows you to merge subtitle files, no matter what language
    are the subtitles encoded in. The result of this merge will be a new subtitle
    file which will display subtitles from each merged file.

    Example:
    ```
    m = Merger(output_path="en-fa.srt")
    m.add(Path('./en.srt'), color=Color.BLUE)
    m.add(Path('./fa.srt'), color="yellow", encoding="cp1256")
    m.merge()
    ```
    """

    def __init__(
        self,
        output_path: str | Path = None,
        output_encoding: str = "utf-8",
    ):
        self.output_path = (
            Path(output_path) if type(output_path) is str else output_path
        )
        self.output_encoding = output_encoding
        self.parser = SrtParser()
        self.merged_subtitles = []
        self.timestamps = []
        self.subtitles = []

    def _insert_bom(self, content, encoding):
        encoding = encoding.replace("-", "").replace("_", "").replace(" ", "").upper()
        if encoding in ["UTF64LE", "UTF16", "UTF16LE"]:
            return codecs.BOM + content
        if encoding in ["UTF8"]:
            return codecs.BOM_UTF8 + content
        if encoding in ["UTF32LE"]:
            return codecs.BOM_UTF32_LE + content
        if encoding in ["UTF64BE"]:
            return codecs.BOM_UTF64_BE + content
        if encoding in ["UTF16BE"]:
            return codecs.BOM_UTF32_BE + content
        if encoding in ["UTF32BE"]:
            return codecs.BOM_UTF32_BE + content
        if encoding in ["UTF32"]:
            return codecs.BOM_UTF32 + content
        return content

    def _set_subtitle_color(self, text, color):
        """
        Set a color for subtitle
        """
        return f'<font color="{color}">{text}</font>' if color else text

    def _put_subtitle_top(self, subtitle):
        """
        Put the subtitle at the top of the screen
        """
        return "{\\an8}" + subtitle

    def _extract_subtitle_entries(self, data, color=None, top=False):
        subtitle_entries = dict()
        subtitle_list = self.parser.split_subtitle(data)[1:]

        # Items with even index represent sequential number and timecodes lines and
        # Items with odd index represent subtitle texts
        for seq_number_and_timecodes_idx in range(0, len(subtitle_list), 2):
            subtitle_entry = (
                subtitle_list[seq_number_and_timecodes_idx]
                + LF
                + subtitle_list[seq_number_and_timecodes_idx + 1].strip()
            )
            seq_number, timecodes, text = self.parser.parse_subtitle_entry(
                subtitle_entry
            )
            begin_time, end_time = self.parser.parse_timecodes(timecodes)

            logger.debug(f"index      = {seq_number_and_timecodes_idx}")
            logger.debug(f"seq_number = {seq_number.strip()}")
            logger.debug(f"timecodes  = {timecodes.strip()}")
            logger.debug(f"begin_time = {begin_time.strip()}")
            logger.debug(f"end_time   = {end_time.strip()}")
            logger.debug(f"text       = \n{text.strip()}")
            logger.debug(self.parser.parse_subtitle_entry(subtitle_entry))
            logger.debug("=" * 30)

            timestamp = time_to_timestamp(begin_time.strip())
            subtitle_text = self._set_subtitle_color(text.strip(), color)
            if top is True:
                subtitle_text = self._put_subtitle_top(subtitle_text)

            subtitle_entries[timestamp] = f"{timecodes.strip()}\n{subtitle_text}\n"

            self.timestamps.append(timestamp)
        return subtitle_entries

    def add(
        self,
        path: str | Path,
        encoding: str = "utf-8",
        color: str | Color = Color.WHITE,
        top: bool = False,
    ):
        """Add subtitle file into merger instance to merge them."""
        with open(path if type(path) is Path else Path(path), "r") as file:
            data = file.buffer.read().decode(encoding)
            subtitle = self._extract_subtitle_entries(data, color, top)
            self.subtitles.append(subtitle)

    def merge(self):
        """Merge subtitles and save output."""
        self.merged_subtitles = []
        self.timestamps = sorted(list(set(self.timestamps)))
        count = 1
        for timestamp in self.timestamps:
            for subtitle_order, subtitle in enumerate(self.subtitles, start=1):
                if timestamp in subtitle.keys():
                    # Remove \n characters at end of first subtitle texts to allow join the other subtitle
                    text = re.sub(r"[\r\n]*$", "", subtitle[timestamp])

                    # Remove Timecodes from subtitles with orders greater than 1
                    if subtitle_order > 1:
                        text = re.sub(TIMECODES_PATTERN, "", text)

                    logger.debug(f"{subtitle_order = }, text = {repr(text)}")

                    try:
                        encoded_subtitle_entry = bytes(
                            text, encoding=self.output_encoding
                        )
                    except Exception as e:
                        logger.error(
                            (
                                f'Encoding problem in "{repr(text)}" with {self.output_encoding}.'
                                f"\nError: {e}"
                            )
                        )
                        encoded_subtitle_entry = b"An error has been occurred in encoding by specified `output_encoding`"

                    if count == 1:
                        encoded_sequential_number = self._insert_bom(
                            bytes(f"{LF}{str(count)}", encoding=self.output_encoding),
                            self.output_encoding,
                        )
                    else:
                        encoded_sequential_number = LF.encode(
                            self.output_encoding
                        ) + bytes(f"{LF}{str(count)}", encoding=self.output_encoding)

                    encoded_subtitle = (
                        # sequential_number is required just before first subtitle text
                        (encoded_sequential_number if subtitle_order == 1 else b"")
                        + LF.encode(self.output_encoding)
                        + encoded_subtitle_entry
                    )
                    self.merged_subtitles.append(encoded_subtitle)
            count += 1

        if self.merged_subtitles[-1].endswith(b"\x00\n\x00"):
            self.merged_subtitles[-1] = self.merged_subtitles[-1][:-3] + b"\x00"
        if self.merged_subtitles[-1].endswith(LF_AS_BYTE):
            self.merged_subtitles[-1] = self.merged_subtitles[-1][:-1] + b""

        with open(self.output_path, "w", encoding=self.output_encoding) as output:
            output.buffer.writelines(self.merged_subtitles)
            logger.info(f'"{output.name}" created successfully.')


# How to use?

# m = Merger(output_path="en-fa.srt")
# m.add(Path('./tests/test_assets/en.srt'), color=Color.BLUE)
# m.add(Path('./tests/test_assets/fa.srt'), color=Color.YELLOW3, encoding="cp1256")
# m.merge()
