#!/usr/bin/env python3

import argparse
from typing import Optional
from dataclasses import dataclass
from .merger import Merger


version = "0.1.0"


@dataclass
class SubtitleConfig:
    """Configuration for a single subtitle file."""

    file_path: str
    encoding: Optional[str] = None
    e: Optional[str] = None
    color: Optional[str] = None
    c: Optional[str] = None
    top: bool = False


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="SrtMerger",
        description="Merge multiple subtitle files with custom configurations.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("-o", "--output", help="Output path")
    parser.add_argument(
        "-e", "--output-encoding", default="UTF8", help="Output encoding"
    )
    parser.add_argument(
        "-E",
        "--default-encoding",
        # default="UTF8",
        help="Default encoding for all files",
    )
    parser.add_argument("-C", "--default-color", help="Default color for all files")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {version}",
        help="Print the version",
    )

    parser.add_argument(
        "subtitles",
        nargs="+",
        metavar="FILE[:OPTS]",
        help="""Subtitle files with optional parameters.
                       Format: file.srt[:e|encoding=value][:c|color=value][:top].
                       Example: sub.srt:encoding=utf-8:color=yellow:top""",
    )

    return parser


def parse_subtitle_spec(spec: str) -> SubtitleConfig:
    """Parse a subtitle specification string into a SubtitleConfig.

    Format: filename.srt[:e|encoding=value][:c|color=value][:top]
    """
    parts = spec.split(":")
    file_path = parts[0]

    config = {"file_path": file_path}

    for part in parts[1:]:
        if part == "top":
            config["top"] = True
        elif "=" in part:
            key, value = part.split("=", 1)
            if key in ("encoding", "e", "color", "c"):
                config[key] = value

    return SubtitleConfig(**config)


def main():
    parser = create_parser()
    args = parser.parse_args()

    try:
        configs = [parse_subtitle_spec(spec) for spec in args.subtitles]
        merger = Merger(output_path=args.output, output_encoding=args.output_encoding)

        for config in configs:
            merger.add(
                config.file_path,
                encoding=config.encoding or config.e or args.default_encoding,
                color=config.color or config.c or args.default_color,
                top=config.top,
            )

        merger.merge()

    except Exception as e:
        parser.error(str(e))


if __name__ == "__main__":
    main()
