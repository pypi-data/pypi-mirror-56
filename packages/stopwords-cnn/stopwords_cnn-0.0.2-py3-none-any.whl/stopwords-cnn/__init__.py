name = 'stopwords-cnn'

stopwords = set()
with open('stopwords-cn.txt') as f:
    for line in f:
        stopwords.add(line[:-1])

def filter(input_list):
    return [i for i in input_list if i not in stopwords]

