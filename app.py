import math
from flask import Flask, redirect, url_for, render_template
import re
from flask import jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your-secret-key'
# print


def load_vocab():
    vocab = {}
    with open('vocab.txt', 'r', encoding='latin-1') as f:
        vocab_terms = f.readlines()
    with open('idf-values.txt', 'r', encoding='latin-1') as f:
        idf_values = f.readlines()

    for (term, idf_value) in zip(vocab_terms, idf_values):
        vocab[term.strip()] = int(idf_value.strip())

    return vocab


def load_documents():
    documents = []
    with open('documents.txt', 'r', encoding='latin-1') as f:
        documents = f.readlines()
    documents = [document.strip().split() for document in documents]

    # print('Number of documents: ', len(documents))
    # print('Sample document: ', documents[0])
    return documents


def load_inverted_index():
    inverted_index = {}
    with open('inverted-index.txt', 'r', encoding='latin-1') as f:
        inverted_index_terms = f.readlines()

    for row_num in range(0, len(inverted_index_terms), 2):
        term = inverted_index_terms[row_num].strip()
        documents = inverted_index_terms[row_num+1].strip().split()
        inverted_index[term] = documents

    # print('Size of inverted index: ', len(inverted_index))
    return inverted_index


vocab_idf_values = load_vocab()
documents = load_documents()
inverted_index = load_inverted_index()


def get_tf_dictionary(term):
    tf_values = {}
    if term in inverted_index:
        for document in inverted_index[term]:
            if document not in tf_values:
                tf_values[document] = 1
            else:
                tf_values[document] += 1

    for document in tf_values:
        tf_values[document] /= len(documents[int(document)])

    return tf_values


def get_idf_value(term):
    return math.log(len(documents)/vocab_idf_values[term])


def calculate_sorted_order_of_documents(query_terms):
    potential_documents = {}
    for term in query_terms:
        if term in vocab_idf_values:
            # continue
            tf_values_by_document = get_tf_dictionary(term)
            idf_value = get_idf_value(term)
            # print(term,tf_values_by_document,idf_value)
            for document in tf_values_by_document:
                if document not in potential_documents:
                    potential_documents[document] = tf_values_by_document[document] * idf_value
                potential_documents[document] += tf_values_by_document[document] * idf_value

    # divite by the length of the query terms

    potential_documents = dict(
        sorted(potential_documents.items(), key=lambda item: item[1], reverse=True))
    if (len(potential_documents) == 0):
        results = []
        # results.append({"Question name": ['No','Results','Found',':('], "Score": 10})
        return results
    else:
        # print(potential_documents)
        for document in potential_documents:
            potential_documents[document] /= len(query_terms)

        # cnt=1;
        results = []
        for doc_index in potential_documents:
            # if(cnt>10):
            #     break
            # print('Document: ', documents[int(document_index)], ' Score: ', potential_documents[document_index])
            results.append({"Question name": documents[int(
                doc_index)], "Score": potential_documents[doc_index]})
            # cnt+=1
        return results


# query_string = input('Enter your query: ')
# query_terms = [term.lower() for term in query_string.strip().split()]

# print(query_terms)
# results = {}
# results = calculate_sorted_order_of_documents(query_terms)
# for result in results:
#     print(result['Question name'],result['Score'])



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_value = request.form['input_field']
        # Process the input and generate a list of results
        query_terms = [term.lower() for term in input_value.strip().split()]
        if (len(calculate_sorted_order_of_documents(query_terms)) >= 20):
            results = calculate_sorted_order_of_documents(query_terms)[:20]
        else:
            results = calculate_sorted_order_of_documents(query_terms)

        return render_template('index.html', results=results)
    else:
        return render_template('form.html')


# if __name__ == '__main__':
#     app.run(port=5001)
