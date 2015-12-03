#!/usr/bin/env python
import datetime
import re

RED = '#FF003B'
BLUE = '#00ADFF'
GREEN = '#B4FF00'
WHITE = '#FFFFFF'
YELLOW = '#FFEB00'

class Merger():
    """
    SRT Merger allows you to merge subtitle files, no matter what language
    are the subtitles encoded in. The result of this merge will be a new subtitle
    file which will display subtitles from each merged file.
    """

    def __init__(self, path="~", output_file_name='subtitle_name.srt'):
        self.subtitles = []
        self.timestamps = []
        self.path = path
        self.output_file_name  = output_file_name
        self.lines=[]


    def _split_dialogs(self, dialogs, subtitle, color=None):
        for dialog in dialogs:
            if dialog.startswith('\r\n'):
                dialog = dialog.replace('\r\n', '',1)
            if dialog == '':
                continue
            time = dialog.split('\n',2)[1].split('-->')[0].split(',')[0]
            timestamp = datetime.datetime.strptime(time,'%H:%M:%S').timestamp()
            text_and_time = dialog.split('\n',1)[1]
            texts = text_and_time.split('\n')[1:]
            time = text_and_time.split('\n')[0]
            text = ""
            for t in texts:
                text += t+'\n'
            text = text if color == None else '<font color="%s">%s</font>'%(color, text)
            text_and_time = '%s\n%s\n'%(time, text)
            subtitle['dialogs'][timestamp] = text_and_time
            self.timestamps.append(timestamp)


    def encode(self, text, codec="utf-16-le"):
        try:
            return bytes(text, encoding='utf-16-le')
        except Exception as e:
            print(b'Problem in "%s" to encoing by %s. \nError: %s'%(text, codec, e))
            return b'Problem in "%s" to encoing by %s'%(text, codec)


    def add(self, subtitle_address, codec="utf-8", color=WHITE):
        subtitle = {'address':subtitle_address,
                    'codec':codec,
                    'color':color,
                    'dialogs': {}
                    }
        with open(subtitle_address, 'r') as file:
            data = file.buffer.read().decode(codec)
            dialogs = re.split('\n\r\n',data)
            subtitle['data'] = data
            subtitle['raw_dialogs'] = dialogs
            self._split_dialogs(dialogs, subtitle, color)
            self.subtitles.append(subtitle)


    def merge(self):
        self.lines = []
        self.timestamps = list(set(self.timestamps))
        self.timestamps.sort()
        cunt = 1
        for t in self.timestamps:
            for sub in self.subtitles:
                if t in sub['dialogs'].keys():
                    line = self.encode(sub['dialogs'][t].replace('\n\n',''))
                    if cunt == 1:
                        byteOfCunt = b'\xff\xfe'+bytes(str(cunt),encoding="utf-16-le")
                    else:
                        byteOfCunt = '\n'.encode("utf-16-le")+bytes(str(cunt),encoding="utf-16-le")
                    if sub['dialogs'][t].endswith('\n') != True:
                        sub['dialogs'][t] = sub['dialogs'][t]+'\n'
                    dialog = byteOfCunt+'\n'.encode("utf-16-le")+line
                    self.lines.append(dialog)
                    cunt += 1

        if self.lines[-1].endswith(b'\x00\n\x00'):
            self.lines[-1] = self.lines[-1][:-3]+b'\x00'
                        
        with  open(self.output_file_name, 'w', encoding="utf-16-le") as output:
            output.buffer.writelines(self.lines)
            print('"%s/%s"'%(self.path, self.output_file_name) ,'created. successfully.',)



## How to use?
#m = Merger(output_file_name="new.srt")
#m.add('fa.srt', codec="utf-16-le")
#m.add('en.srt')
#m.merge()
