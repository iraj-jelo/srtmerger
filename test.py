#!/usr/bin/env python

from main import Merger

## How to use?
m = Merger(output_name="new.srt", output_encoding="utf-16-le")
m.add('./test_srt/en.srt') # utf8 as default codec, white as default color
m.add('./test_srt/fa.srt', color="yellow", codec="cp1256")
m.merge()
