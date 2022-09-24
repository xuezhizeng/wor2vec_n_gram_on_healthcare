import spacy
import pandas as pd
import itertools as it
import re
import os
import sys
import string
import random
from classification_binary.configfile import *

nlp = spacy.load('en')



#path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
path = os.getcwd()


dict_uk_us = {} # store the dictionary of uk and us



def replace_all(text, uk_us_dict):
    word_list = text.split()
    for uk, us in uk_us_dict.items():
     for word in word_list:
      if(us == word):
       index = word_list.index(word)
       word_list[index] = uk
    return " ".join(word_list)


#read dictionary_uk_us and build a dictionary object
def buildDictUKtoUS(fileName):
    with open(path + '/input/' + fileName,'r') as f:
        for line in f:
            dict_uk_us[line.strip().split(":")[0]] = line.strip().split(":")[1]
    return dict_uk_us

def readfile(path):
    fp = open(path, "r", encoding='utf-8', errors='ignore')
    content = fp.read()
    fp.close()
    return content


def savefile(savepath, content):
    fp = open(savepath, "w+",encoding='utf-8', errors='ignore')
    fp.write(content)
    fp.close()



#this function is used to clean the raw content of each research plan
def cleanRawText(text,fileName,folder_by_disease,destination):

    dict_uk_us = buildDictUKtoUS('dictionary_uk_us.txt')
    text = replace_all(text,dict_uk_us)
    text = text.strip().lower()   #remove blank and lower all words in the text
    # text = re.sub(r"-", " ", text) #split the two words with "-" connected, for example：Beckwith-Wiedemann ==> Beckwith Wiedemann）
    # text = re.sub(r"\s+[0-9]+$", "", text)  # remove number   #$ means string ending with number
    text = re.sub(r"[\",?,``,–,(,~,:,),\"]", " ", text)  # remove "(", "~",":", ")"
    text = re.sub(r"\/", " ", text)  # remove / in data like gain-of-function/loss-of-function
    text = re.sub(r"^-", " ", text)  # remove "-" in data like -Actinin-3
    text = re.sub(r"[\",\,]", "", text)  # remove , and "
    text = re.sub(r"\s+[0-9]+\s+", " ", text)  # remove number in the following example: 20.2,  will not remove 11p15.5

    text = re.sub(r"\d{n,}$", " ", text)  # remove number   #$ means string ending with number

    text = text.replace('\n', " ")  # remove new line
    text = re.sub(r"[^\x00-\xff]", " ", text)  # remove all double byte strings. for example: "—", "‘"
    text = re.sub(r"[\x91,\x92,\x93,\x94,\x95,\x96,\x97]", " ",text)  # remove all double byte strings. for example: "—", "‘"

    '''
    text = re.sub(r"\x97", " ", text) #remove "—" for example：growth regulators—for example, CDKN1C
    text = re.sub(r"\x91", " ", text) #remove "‘", for example： in germ cells, these ‘reformatting’
    text = re.sub(r"\x92", " ", text) #remove "’", for example： in germ cells, these ‘reformatting’
    text = re.sub(r"\x93", " ", text)
    text = re.sub(r"\x94", " ", text)
    text = re.sub(r"\x96", " ", text)
    '''


    text = re.sub(r"^\d+\.\d+", "", text)  # remove date like 2010.0
    text = re.sub(r"\d+/\d+/\d+", "", text)  # remove date like 2016/09/10
    text = re.sub(r"\d+/\d+", "", text)  # remove date like 2016/09
    text = re.sub(r"\d+\-\d+", "", text)  # remove date like 2007-08
    text = re.sub(r"[0-9]{4}", "", text)  # remove date like 2014, or 2014-2016
    text = re.sub(r"[0-9]{2}\–[0-9]{2}", "", text)  # remove number like aged 16-20
    text = re.sub(r"[0-9]\.[0-9]", "", text)  # remove number like 9.5
    text = re.sub(r"app[0-9]+", "", text)  # remove number app1116352
    text = re.sub(r"page +[0-9]+", "", text)  # remove data like page 9

    text = re.sub(r"[0-9]+\,[0-9]+", "", text)  # remove data 19,737, 19377
    text = re.sub(r"[0-9]+%","", text)  # remove data like 13%
    text = re.sub(r">[0-9]+","", text)  # remove data like >50
    text = re.sub(r"including +references", "", text)  #remove "including references" in some research plans
    text = re.sub(r" +references.*", "", text)  #remove all the references starting from "references" to the end of the research plan


    text = re.sub(r"[0-2]?[0-9]:[0-6][0-9]", "", text)  # remove time
    text = re.sub(r"[\.]\s+", " ", text)  # remove ".", but not remove "." in string like "11lp15.5"

    # text = re.sub(r"[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]", " ", text)

    text = re.sub(r"[\",/\,?,``,–,(,~,:,),\"]", " ", text)  # remove "(", "~",":", ")" again

    text = re.sub(r"\s+", " ", text)  # finally, we remove any extra blank between strings,just keep one blank between them


    pure_text = ''
    # remove them in case there are some special string,number
    for letter in text:
        #if letter.isalpha() or letter==' ':       #Python isalpha() function check if string consists of letter
        #if letter!='—':
        pure_text += letter
    # the remaining are all meaningful words。
    text = ' '.join(word for word in pure_text.split() if len(word)>1)


    #cleaned_text = open(path + '/butac/text_classification/train_clean/' + fileName, 'w')
    savepath = path + '/' + destination + '/' + folder_by_disease + '/'

    if(destination == "train_clean"):
        if(not os.path.exists(savepath)):
            os.makedirs(savepath)

        savefile(savepath + '/' + fileName,text)
    else:
        #savepath = path + '/butac/text_classification/' + destination + '/' + folder_by_disease + '/'
        if (not os.path.exists(savepath)):
            os.makedirs(savepath)

        savefile(savepath + '/' + fileName, text)
    return text


