#imports fitz and nltk
import fitz
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from collections import Counter
from nltk.corpus import wordnet
from nltk.corpus import stopwords
nltk.download('universal_tagset')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')



#defines WordFactory class
class WordFactory:
    def __init__(self, words_list): #receives (word, occurrence) as parameter
        self.word = words_list[0]
        self.category = categorize(words_list[0])
        self.meaning = get_meaning(words_list[0]) 
        self.occurrence = words_list[1]



#reads a pdf and returns an enormous string
def read_pdf(file_path):
    pdf = fitz.open(file_path)
    pdf_content = ""

    for page_num in range(pdf.page_count):
        page = pdf[page_num]
        pdf_content += page.get_text()
        
    pdf.close()
    return pdf_content



#tokenizes a string and returns an array with the words
def tokenize(pdf_content):
    tokenized_words = word_tokenize(pdf_content.lower())
    tokenized_words_filtered = []
    i = 0
    while i < len(tokenized_words):
        word = tokenized_words[i]
        if not any(char.isdigit() for char in word): #doesn't accept numbers
            if word.isalpha(): #only accepts alphabet letter
                tokenized_words_filtered.append(word)
            else:
                if word.endswith('-'): #check if a word ends with hyphen, removing hyphen and join with the next word
                    word_without_hyphen = word.replace('-', '')
                    if not any(char.isdigit() for char in tokenized_words[i+1]): #checks if none of the characters in the subsequent string are numbers
                        word_without_hyphen += tokenized_words[i+1]
                        tokenized_words_filtered.append(word_without_hyphen)
                    else: #if the characters in the subsequent string are numbers, joins with the second string
                        word_without_hyphen += tokenized_words[i+2]
                        tokenized_words_filtered.append(word_without_hyphen)
                    #The chance of the second string in the list containing a number is extremely small, which is why another if was not implemented to check. In any case, this word will be removed later
        i += 1

    tokenized_words_filtered_2 = [token for token in tokenized_words_filtered if not (token.startswith('https') or token.startswith('www'))] #don't show words that starts with "https" or "www"

    stop_words = set(stopwords.words('english'))
    tokenized_words_filtered_3 = []

    for word in tokenized_words_filtered_2:
            if len(word) > 2 and word not in stop_words: #only accepts words with more than two letters and outside English stopwords
                tokenized_words_filtered_3.append(word)

    return tokenized_words_filtered_3



#lemmatizes a tokenized words list and returns an array with dictionary form words
def lemmatize(list):
    lemmatizer = WordNetLemmatizer()
    dictionary_form = [lemmatizer.lemmatize(word, pos='v') for word in list] #puts verbs in dictionary form
    dictionary_form_2 = [lemmatizer.lemmatize(word) for word in dictionary_form] #puts plurals in singular form
    return dictionary_form_2



#returns an array of tuples, with word and occurrence number sorted by frequency
def get_occurrence(list):
    counter = Counter(list)
    word_and_occurrence_tuple_list = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    return word_and_occurrence_tuple_list



#returns an array of tuples, with word and morphologic category
def categorize(words_list):
    tagged_words = pos_tag([words_list], tagset='universal', lang='eng')
    if tagged_words:
        if tagged_words[0][1] == "NOUN":
            return "Noun"
        elif tagged_words[0][1] == "VERB":
            return "Verb"
        elif tagged_words[0][1] == "ADJ":
            return "Adjective"
        elif tagged_words[0][1] == "ADV":
            return "Adverb"
        else:
            return tagged_words[0][1]
    else:
        return "UNKNOWN CATEGORY"



#returns possible meanings of the word
def get_meaning(palavra):
    synsets = wordnet.synsets(palavra)

    if synsets:
        meanings = []

        for synset in synsets:
            meanings.append(synset.definition())

        return meanings
    else:
        return "UNKNOWN MEANING"



#English Reading Assistant
def en_reading_assistant(file_path):
    pdf_content = read_pdf(file_path)
    tokenized_words = tokenize(pdf_content)
    lemmatized_words = lemmatize(tokenized_words)
    word_and_occurrence_tuple_list = get_occurrence(lemmatized_words) #[(word_1, occurrence_1), (word_2, occurrence_2), ...(word_n, occurrence_n)]
    instantiated_words_list = []

    for word_occurrence in word_and_occurrence_tuple_list:
        word_instance = WordFactory(word_occurrence)
        if word_instance.meaning != "UNKNOWN MEANING" and word_instance.category != "UNKNOWN CATEGORY" and (word_instance.category == "Verb" or word_instance.category == "Adverb" or word_instance.category == "Noun" or word_instance.category == "Adjective"): #only accepts verbs, nouns, adjectives and adverbs; Doesn't accept unknown meaning and category
            instantiated_words_list.append(word_instance)
        else:
            del word_instance
    return instantiated_words_list



def generateDownloadList(list):
    i = 1
    with open("Vocabulary List.txt", "w", encoding="utf-8") as f:
        f.write("-------------------------------------------------------------------------------\n")

        for word in list:
            f.write(word.word + " #" + str(word.occurrence) + "\n")

            f.write("Category: " + word.category +"\n")

            #writes the occurrence in a better way
            if word.occurrence == 1:
                f.write("Occurrence: Once\n")
            elif word.occurrence == 2:
                f.write("Occurrence: Twice\n")
            else:
                f.write("Occurrence: " + str(word.occurrence) + " times\n")

            #writes each meaning
            i = 1
            f.write("Meaning:\n" )
            for meaning in word.meaning:
                f.write(str(i) + " - " + meaning)
                f.write(";\n")
                i += 1
            f.write("-------------------------------------------------------------------------------\n")
    f.close()
    print("List Downloaded!")