import numpy as np
import random
import re
import csv

from odf import text, teletype
from odf.opendocument import load

word_match = "(?<!\\w)(?!\\w)\\w+"
word_match = "\\w+"
sentence_sep = "(?<!\\w\\.\\w.)(?<![A-Z][a-z]\\.)(?<=\\.|\\?|!)\\s"

voc_file = "Lexique382.tsv"

class FillInGaps:
	def __init__(self):
		self.freq_max = 1000
		self.voc = {}
		self.load_voc(voc_file)
		self.is_valid = False

	def load_voc(self, file):
		voc_reader = csv.reader(open(file, "r"), delimiter="\t")
		for id_row, row in enumerate(voc_reader):
			if id_row == 0:
				keys = ["ortho", "freqlivres"]
				key2id = dict(zip(keys, [row.index(_) for _ in keys]))
			else:
				freq = float(row[key2id["freqlivres"]])
				word = row[key2id["ortho"]]
				word = word.lower()
				self.voc[word] = max(freq, self.voc.get(word, -1))

	def load_file(self, file):
		textdoc = load(file)
		allparas = textdoc.getElementsByType(text.P)
		allparas = [teletype.extractText(_) for _ in allparas]
		allparas = [_ for _ in allparas if len(_) > 20]
		self.allparas = allparas
		self.is_valid = True

	def draw_text(self):
		if not self.is_valid:
			raise RuntimeError("Input text was not initialized")
		id_para = random.randint(0,len(self.allparas)-1)
		para = self.allparas[id_para]
		if len(para) < 200:
			text = para
		else:
			sents = re.split(sentence_sep, para)
			id_sent = random.randint(0, len(sents)-1)
			text = sents[id_sent]

		text_gaps = text
		word_match_re = re.compile(word_match)
		words = list(word_match_re.finditer(text))
		words = [(m.start(), m.group()) for m in words] # list of (index, str)
		tries = 0
		gaps = 0
		gaps_pos = []
		gaps_words = []
		while gaps < 3 and tries < 100:
			tries += 1
			id_word = random.randint(0, len(words)-1)
			if id_word not in gaps_pos:
				word_start, word = words[id_word]
				word = word.lower()
				if self.voc.get(word, -1) > self.freq_max:
					print(word, self.voc.get(word, -1))
					continue
				gaps_pos.append(id_word)
				gaps_words.append(word)
				gaps += 1
				text_gaps = text_gaps[:word_start] + "_"*len(word) + text_gaps[word_start+len(word):]
		
		gaps_sort = np.argsort(gaps_pos)
		gaps_words = list(np.array(gaps_words)[gaps_sort])
		return text, text_gaps, gaps_words

def main():
	fig = FillInGaps("doc.odt")
	print(fig.draw_text())

if __name__ == '__main__':
	main()
