# SrtMerger

A command-line tool to merge multiple SRT subtitle files with customizable colors, positions, and encodings.

[![PyPI version](https://img.shields.io/pypi/v/srtmerger.svg)](https://pypi.org/project/srtmerger/)
[![Python versions](https://img.shields.io/pypi/pyversions/srtmerger.svg)](https://pypi.org/project/srtmerger/)
[![License](https://img.shields.io/github/license/iraj-jelo/srtmerger.svg)](https://github.com/iraj-jelo/srtmerger/blob/main/LICENSE)


![s](https://cloud.githubusercontent.com/assets/1775045/11559585/608ac4fa-99cf-11e5-91a2-3ea93ae98a3a.png)

Subtitle merger is a tool for merging two or more subtitles for videos.
SRT Merger allows you to merge subtitle files, no matter what language are the subtitles encoded in. The result of this merge will be a new subtitle file which will display subtitles from each merged file.

## Features

- Merge multiple SRT subtitle files into one
- Customize subtitle colors for each input file
- Set subtitle position (top/bottom) individually
- Support for different file encodings
- Set global defaults for all files
- Simple and intuitive command-line interface

## Installation

```bash
pip install srtmerger
```

## Usage

### Python
Running in your Python script:

```Python
 from srtmerger import Merger


 m = Merger(output_path="new.srt")
 m.add('fa.srt', color="yellow", encoding="windows-1256")
 m.add('en.srt')
 m.merge()
```

### Bash
The basic syntax is:
```bash
srtmerger [global options] file1.srt[:options] file2.srt[:options] ...
```

Each subtitle file can have its own configuration using colon-separated options:
- `e=VALUE`, `encoding=VALUE`: Set the file encoding (e.g., utf-8, utf-16)
- `c=VALUE`, `color=VALUE`: Set the subtitle color
- `top`: Position the subtitles at the top of the screen

##### Global Options

- `-o`, `--output`: Set path for the output file
- `-e`, `--output-encoding`: Set encoding for the output file
- `-E`, `--default-encoding`: Set default encoding for all files
- `-C`, `--default-color`: Set default color for all files
- `-T`, `--default-top`: Set default top position for all files

#### Examples

1. Basic merge of two subtitle files:
```bash
srtmerger sub1.srt sub2.srt -o output.srt
```

2. Set specific options for each file:
```bash
srtmerger sub1.srt:encoding=utf-8:color=yellow:top sub2.srt:color=blue --output output.srt
```
The above command is equivalent to:
```bash
srtmerger sub1.srt:e=utf-8:c=yellow:top sub2.srt:c=blue -o output.srt
```

3. Use global defaults with some overrides:
```bash
srtmerger -o output.srt -E utf-8 -C white sub1.srt sub2.srt:color=blue
```

## Development

### Prerequisites

- Python 3.11 or higher

### Setting up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/iraj-jelo/srtmerger.git
cd srtmerger
```

2. Install in editable mode with test dependencies:
```bash
pip install -e .
```

### Running Tests

Run all tests:
```bash
python -m unittest discover -s tests -v
```

Run a specific test file:
```bash
python -m unittest tests/test_main.py -v
```

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/my-new-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- **iraj-jelo** - *Initial work* - [GitHub](https://github.com/iraj-jelo)

## Changelog

### [0.1.0] - 2025-01-12
- Initial release
- Basic subtitle merging functionality
- Support for custom colors and positioning
- File encoding options
- Command-line interface

### [0.1.1] - 2025-02-12
- Bug fix for importing `Color` and `Merger` classes in Python