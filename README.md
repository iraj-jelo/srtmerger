# srtmerger
![s](https://cloud.githubusercontent.com/assets/1775045/11559585/608ac4fa-99cf-11e5-91a2-3ea93ae98a3a.png)
subtitle merger is a tool for merging two or more subtitles for videos.
SRT Merger allows you to merge subtitle files, no matter what language are the subtitles encoded in. The result of this merge will be a new subtitlec file which will display subtitles from each merged file.

## How to works?
    m = Merger(output_file_name="new.srt")
    m.add('fa.srt', codec="utf-16-le")
    m.add('en.srt')
    m.merge()
