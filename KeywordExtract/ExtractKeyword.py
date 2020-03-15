# courtesy of https://github.com/minimaxir/gpt-2-keyword-generation
import spacy
import re

PRONOUN_LIST = ['I', 'Me', 'We', 'You', 'He', 'She',
                'It', 'Him', 'Her', 'Them', 'They']

PRONOUNS = set(PRONOUN_LIST + [x.lower() for x in PRONOUN_LIST])

KEYWORD_MAX_LENGTH = 20

def extractKeyword(inputString):
    nlp = spacy.load('en_core_web_sm')
    pattern = re.compile('\W+')

    text = re.sub(u'[\u2018\u2019]', "'",
                  (re.sub(u'[\u201c\u201d]', '"', inputString)))
    doc = nlp(text)
    keywords_pos = [chunk.text if chunk.pos_ == 'NOUN'
                    else chunk.lemma_ if chunk.pos_ in ['VERB', 'ADJ', 'ADV']
                    else 'I'
                    for chunk in doc
                    if not chunk.is_stop
                    ]
    keywords_ents = [re.sub(' ', '-', chunk.text)
                     for chunk in doc.ents]
    keywords_compounds = [re.sub(' ', '-', chunk.text)
                          for chunk in doc.noun_chunks
                          if len(chunk.text) < KEYWORD_MAX_LENGTH]

    keywords = list(set(keywords_pos +
                        keywords_ents +
                        keywords_compounds) - PRONOUNS)  # dedupe
    return keywords
