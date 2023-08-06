import re
import warnings
import os
import operator
from nltk.corpus import stopwords
from ..symspellpy.symspellpy import SymSpell


class TextPreprocessing:
    initial_capacity = 83000
    max_edit_distance_dictionary = 3
    prefix_length = 7
    dictionary_path = os.path.join(os.path.dirname(__file__), "symspellpy",
                                   "frequency_dictionary_en_82_765.txt")
    sym_spell = SymSpell(initial_capacity, max_edit_distance_dictionary,
                         prefix_length, compact_level=0)
    max_edit_distance_lookup = 2

    def __init__(self, acronyms):
        self.text = str
        self.acronym_dict = acronyms
        self.min_char = 2
        self.max_char = 13
        self.separator = [' ', '•', ',', '.', ' .', ' ,', '. ', ', ', '-', ':',
                          "\\n", '\\t', "[", "]", "_", "/", ">", "*"]

    def transform(self, text):
        text = self.split(text)
        text = self.replace_acronyms(text)
        text = self.remove_numbers(text)
        text = self.remove_stopwords(text)
        text = self.symspell(text)
        text = self.remove_chars(text)

        return text

    def split(self, text):

        if text:
            default_sep = self.separator[0]
            text = text.replace("\n", default_sep)
            for sep in self.separator[1:]:
                text = text.replace(sep, default_sep)

            text = re.sub(' +', ' ', text)
            return ' '.join(
                [i.strip().lower() for i in text.split(default_sep)])

        else:
            warnings.warn("found empty text", Warning)

    def replace_acronyms(self, text):
        text_temp = []
        for word in text.split(' '):
            if word in self.acronym_dict.keys():
                text_temp.extend(self.acronym_dict[word].split(' '))
            else:
                text_temp.append(word)

        return ' '.join(text_temp)

    @staticmethod
    def remove_numbers(text):
        return ' '.join(re.findall("[a-z]+", text))

    @staticmethod
    def remove_stopwords(text):
        cached_stopwords = stopwords.words("english")
        text = [word for word in text.split(' ') if word != '']

        return ' '.join([word.lower() for word in text if
                         word.lower() not in cached_stopwords])

    def symspell(self, text):
        suggestions = self.sym_spell.\
            lookup_compound(text, self.max_edit_distance_lookup)
        return ' '.join([suggestion.term for suggestion in suggestions])

    def remove_chars(self, text):
        return ' '.join([word for word in text.split(' ') if
                         self.min_char < len(word) < self.max_char])


class TextSegmentation:
    def __init__(self, segments):
        self.segments = segments
        self.loc = -1

    def segment(self, text):
        loc = dict()
        for key in self.segments.keys():
            loc[key] = -1
            for item in self.segments[key]:
                if item.lower() in text.lower():
                    loc[key] = text.lower().find(item.lower())

        # Sometimes it would not be in the order it should be
        loc = sorted(loc.items(),
                     key=operator.itemgetter(
                         1)
                     )

        text_out = {key[0]: [] for key in loc}
        for index, location in enumerate(loc):
            key = location[0]
            value = location[1]

            if index == 3 and value > 0:
                text_out[key] = text[value:len(text)]

            elif value >= 0:
                itrtr = index + 1
                while itrtr < 4:
                    # locations[itrtr][1] is next value
                    if loc[itrtr][1] >= 0:
                        text_out[key] = text[value:loc[itrtr][1]]
                        break
                    itrtr = itrtr + 1

        return text_out
