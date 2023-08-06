import random

class Unk:
    def __init__(self, magic):
        self.unkList = ['https://www.youtube.com/watch?v=QObAroqCA7o', 'https://www.youtube.com/watch?v=0iPjfuzhtwE', 'https://www.youtube.com/watch?v=nucwKV2e10I', 'https://www.youtube.com/watch?v=_zLF_bRtRnk', 'https://www.youtube.com/watch?v=rzgWw4qavoY', 'https://www.youtube.com/watch?v=FClZzTPSt1E', 'https://www.youtube.com/watch?v=uObtQJu5OBY', 'https://www.youtube.com/watch?v=h6hrnMCxVcY']
        self.msg = 'ミス！うんこうんこ！'
        self.magic = magic

    def luvunk(self):
        if self.magic == 'I love unk.':
            return random.choice(self.unkList)
        else:
            return self.msg
