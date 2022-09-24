import  os

path = os.getcwd()

dict_uk_us = {}  # store the dictionary of uk and us


def replace_all(text, uk_us_dict):

    word_list = text.lower().split()  #here must lower() the text firstly
    print("word_list:",word_list)
    for uk, us in uk_us_dict.items():
     for word in word_list:
          if(us == word):
                index = word_list.index(word)
                word_list[index] = uk
    return " ".join(word_list)

def buildDictUKtoUS(fileName):
    with open(path + '/input/' + fileName,'r') as f:
        for line in f:
            dict_uk_us[line.strip().split(":")[0]] = line.strip().split(":")[1]
    return dict_uk_us

import re
text = 'tumor tumors.Finally 5.61 2017.dd2'
new = re.sub(r"[.]", " ", text)
print("new:",new)


dict_uk_us = buildDictUKtoUS('dictionary_uk_us.txt')
result = replace_all(new,dict_uk_us)

print("result:",result)