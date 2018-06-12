import logging
import jieba
import os, sys
import json

from utils import iter_files

BOS_TOKEN = '<BOS>'
EOS_TOKEN = '<EOS>'
UNK_TOKEN = '<UNK>'

class Dictionary(object):

    def __init__(self):
        self.word2ix = {}
        self.word2count = {}
        self.ix2word = {}
        self.size = 0
        self.addWord(BOS_TOKEN)
        self.addWord(EOS_TOKEN)
        self.addWord(UNK_TOKEN)

    def addWord(self, word):
        if word not in self.word2ix:
            self.word2ix[word] = self.size
            self.ix2word[self.size] = word
            self.word2count[word] = 1
            self.size += 1

        else:
            self.word2count[word] += 1

    def addWords(self, words):
        for w in words:
            self.addWord(w)


    def __len__(self):
        return self.size

    def __repr__(self):
        return self.ix2word.__repr__()

    def saveToFile(self, filename):
        pass

    def loadFromFile(self, filename):
        pass



def _parseDoc(doc, dictionary):
    tokens = jieba.cut(doc)
    dictionary.addWords(tokens)

def parse(dir_name='交运物流'):
    generator = iter_files(dir_name)
    for f in generator:
        try:
            with open(f,'r') as o:
                doc = json.read(o)
                _parseDoc(doc)
                print ('succeed to parse file {}'.format(f))
        except:
            print ('fail to parse file {}'.format(f))



# def removeDupFiles(dir_name='hyyb'):
#     generator = iter_files(dir_name)
#     for f in generator:
#         bn = os.path.basename(f)
#         if bn[-8:] == '(1).json':
#             os.remove(f)
#             print ('remove file {}'.format(f))
