#!/usr/bin/env python
from main import Merger

## How to use?
m = Merger(output_file_name="new.srt")
m.add('./test_srt/en.srt')
m.add('./test_srt/fa.srt', color="yellow", codec="cp1256")
m.merge()
