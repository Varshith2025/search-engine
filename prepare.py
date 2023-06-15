# read the index.txt and prepare documents, vocab , idf

import chardet

def find_encoding(fname):
    r_file = open(fname, 'rb').read()
    result = chardet.detect(r_file)
    charenc = result['encoding']
    return charenc


filename = 'Leetcode-Questions-Scrapper/index.txt'
my_encoding = find_encoding(filename)

with open(filename, 'r', encoding=my_encoding) as f:
    lines = f.readlines()
    # print(lines)


def preprocess(document_text):
    # remove the leading numbers 
    terms = [term.lower() for term in document_text.strip().split()[1:] ]
    # print(terms)
    return terms
 
vocab = {}
documents = []
for index,line in enumerate(lines):
    # print(index,line)
    tokens = preprocess(line)
    documents.append(preprocess(line))
    for token in tokens:
        if token not in vocab:
            vocab[token] = 1
        else:
            vocab[token] += 1

# print(documents[:5])
#  reverse sort the vocab by values
vocab = dict(sorted(vocab.items(), key=lambda item: item[1], reverse=True))
# print('Number of documents:', len(documents))
# print('Size of vocab:', len(vocab))
# print('sample document:', documents[0])
# print(vocab)


# save the vocab in a text file
with open('tf-idf/vocab.txt', 'w') as f:
    for key in vocab.keys():
        f.write("%s\n" % key)


with open('tf-idf/idf-values.txt', 'w') as f:
    for key in vocab.keys():
        f.write("%s\n" % vocab[key])

with open('tf-idf/documents.txt', 'w') as f:
    for document in documents:
        f.write("%s\n" % ' '.join(document))
    
inverted_index = {}
for index,document in enumerate(documents):
    for token in document:
        if token not in inverted_index:
            inverted_index[token] = [index]
        else:
            inverted_index[token].append(index)

# save the inverted index in a text file
with open('tf-idf/inverted-index.txt', 'w') as f:
    for key in inverted_index.keys():
        f.write("%s\n" % key)
        f.write("%s\n" % ' '.join(str(e) for e in inverted_index[key]))    