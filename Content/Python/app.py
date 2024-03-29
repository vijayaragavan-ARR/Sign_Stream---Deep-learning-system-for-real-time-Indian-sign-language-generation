from flask import Flask, request, jsonify
from nltk.tokenize import RegexpTokenizer
import nltk
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download("wordnet")
nltk.download("omw-1.4")

# Initialize WordNet lemmatizer
wnl = WordNetLemmatizer()

# Define sets of auxiliary verbs, tags to remove, negative words, and questionary words
auxiliary_verbs = {'be', 'am', 'is', 'are', 'was', 'were', 'been', 'being', 'has', 'had', 'does','did'}
tags_to_remove = {'MD', 'DT', 'TO','IN'}
negative_words = {'not', 'no', "don't", "doesn't", "didn't", "won't", "can't", "couldn't", "isn't", "aren't", "wasn't", "weren't"}
questionary_words = {'where', 'who', 'what', 'when', 'how', 'why'}

# Initialize a tokenizer
tokenizer = RegexpTokenizer(r"\b\w+(?:'\w+)?\b")

def classify_sentence_type(tagged_words):
    """Classify the type of sentence: simple, question, imperative, or negative."""
    first_word_tag = tagged_words[0][1]
    first_word = tagged_words[0][0].casefold()

    if first_word_tag == 'MD' or first_word.casefold() in auxiliary_verbs or any(word[0].casefold() in questionary_words for word in tagged_words):
        return 'question' 
    
    elif first_word_tag.startswith('V') and first_word != 'be' and first_word_tag != 'MD':
        return 'imperative'
    
    elif any(word[0].casefold() in negative_words for word in tagged_words):
        return 'negative'

    else:
        return 'simple'

def reorder_sentence(sentence, sentence_type, tagged_words):
    """Reorder the sentence based on its type."""
    subject = None
    verb = None
    for word, tag in tagged_words:
        if (tag.startswith('N') or tag.startswith('P')) and subject is None:
            subject = word
        elif tag.startswith('V') and verb is None and word not in auxiliary_verbs:
            verb = word
        if subject and verb:
            break

    # Remove subject and verb from the sentence
    if subject and verb:
        sentence = ' '.join([word for word, _ in tagged_words if word not in [subject, verb]])

    if sentence_type == 'simple':
        reordered_sentence = f"{subject} {sentence} {verb}" if verb else sentence

    elif sentence_type == 'question':
        question_word = next((word for word, _ in tagged_words if word in questionary_words), None)
        reordered_sentence = f"{sentence} {verb} {question_word}" if verb and question_word else sentence

    elif sentence_type == 'negative':
        # Add 'not' to the end of the sentence if it contains negative words
        if any(word.casefold() in negative_words for word in sentence.split()):
            reordered_sentence = f"{subject} {' '.join([word for word in sentence.split() if word.casefold() not in negative_words])} not"
        else:
            reordered_sentence = sentence

    else:
        reordered_sentence = sentence

    return reordered_sentence

def filter_and_lemmatize(words, tags):
    """Filter out unnecessary words and lemmatize remaining words."""
    filtered_words = []

    for word, tag in zip(words, tags):
        if tag not in tags_to_remove and word.casefold() not in auxiliary_verbs:
            wn_tag = nltk.corpus.wordnet.NOUN
            if tag.startswith('J'):
                wn_tag = nltk.corpus.wordnet.ADJ
            elif tag.startswith('V'):
                wn_tag = nltk.corpus.wordnet.VERB
            elif tag.startswith('R'):
                wn_tag = nltk.corpus.wordnet.ADV

            # Lemmatize the word based on its part of speech
            lemma = wnl.lemmatize(word, pos=wn_tag)
            filtered_words.append(lemma)

    return filtered_words

@app.route('/', methods=['POST'])
def get_filtered_words():
    """Endpoint to receive input string, process it, and return filtered words."""
    input_string = request.json.get('input_string')

    words = tokenizer.tokenize(input_string)
    tagged_words = nltk.pos_tag(words)

    # Classify the type of sentence
    sentence_type = classify_sentence_type(tagged_words)

    # Reorder the sentence based on its type
    reordered_sentence = reorder_sentence(input_string, sentence_type, tagged_words)

    # Filter and lemmatize the words in the reordered sentence
    filtered_words = filter_and_lemmatize(tokenizer.tokenize(reordered_sentence), [tag for _, tag in nltk.pos_tag(tokenizer.tokenize(reordered_sentence))])

    return jsonify({'filtered_Words': filtered_words})

if __name__ == '__main__':
    app.run(debug=True)
