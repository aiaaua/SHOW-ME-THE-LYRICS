from parse import Parser
from alpha import Alphabet

class Generator:
	def __init__(self, name, db, rnd):
		self.name = name
		self.db   = db
		self.rnd  = rnd

	def _get_next_word(self, word_list):
		candidate_words = self.db.get_word_count(word_list)
		total_next_words = sum(candidate_words.values())
		i = self.rnd.randint(total_next_words)
		t=0
		for w in candidate_words.keys():
			t += candidate_words[w]
			if (i <= t):
				return w
		assert False   
        
	def _jungsung_rhyme(self, word) :
		Alpha = Alphabet()
		return Alpha.get_jungsung_alphabetic(word)
        
	def _jongsung_rhyme(self, word) : 
		Alpha = Alphabet()
		return Alpha.get_jongsung_alphabetic(word)
        
	def _check_jungsung_rhyme(self, prev_word, pres_word, prev_pres_word, end_symbol) :
		for i in range(4) : 
			prev_jungsung_rhyme = self._jungsung_rhyme(prev_word)
			pres_jungsung_rhyme = self._jungsung_rhyme(pres_word)

			if prev_jungsung_rhyme == pres_jungsung_rhyme :
				break
			else : 
				while True : 
					pres_word = self._get_next_word(prev_pres_word)
					if pres_word == end_symbol[0] : 
						continue
					else : break
		else : 
			return False, pres_word
		return True, pres_word
        
	def _check_jongsung_rhyme(self, prev_word, pres_word, prev_pres_word, end_symbol) :
		for i in range(4) :
			prev_jongsung_rhyme = self._jongsung_rhyme(prev_word)
			pres_jongsung_rhyme = self._jongsung_rhyme(pres_word)

			if prev_jongsung_rhyme == pres_jongsung_rhyme and prev_jongsung_rhyme != [' '] :
				break
			else : 
				while True : 
					pres_word = self._get_next_word(prev_pres_word)
					if pres_word == end_symbol[0] : 
						continue
					else : break
		else : 
			return False, pres_word
		return True, pres_word

	def _check_rhyme(self, sentence, prev_sentence, depth, word_separator, end_symbol) : 
		prev_last_word = sentence[(-depth-1):(-depth)]
		last_word = sentence[(-depth):(-depth+1)]
		prev = prev_sentence.split(word_separator)
		check1, last_word = self._check_jungsung_rhyme(prev[-1], last_word[0], prev_last_word, end_symbol[0])
		sentence[(-depth):(-depth+1)] = last_word
                        
		if check1 != True :
			prev_last_word = sentence[(-depth-1):(-depth)]
			last_word = sentence[(-depth):(-depth+1)]
			prev = prev_sentence.split(word_separator)
			check2, last_word = self._check_jongsung_rhyme(prev[-1], last_word[0], prev_last_word, end_symbol[0])
			sentence[(-depth):(-depth+1)] = last_word
		return sentence
        
	def generate(self, word_separator, prev_sentence = None):
		depth = self.db.get_depth()
		sentence = [Parser.SENTENCE_START_SYMBOL] * (depth - 1)
		end_symbol = [Parser.SENTENCE_END_SYMBOL] * (depth - 1)
		cnt_w = 0
        
		while True:
			tail = sentence[(-depth+1):]
			if tail == end_symbol:
				if len(sentence) < 5 :
					if cnt_w >= 4 :
						break
					else :
						cnt_w += 1                        
						sentence.pop()
						continue
				else : 
					if prev_sentence == None :
						break
					else : 
						sentence = self._check_rhyme(sentence, prev_sentence, depth, word_separator, end_symbol)
						break
			else : 
				if len(sentence) >= 10 :
					sentence = self._check_rhyme(sentence, prev_sentence, depth, word_separator, end_symbol)
					sentence.append(end_symbol)
					break
			word = self._get_next_word(tail)
			sentence.append(word)
		
		return word_separator.join(sentence[depth-1:][:1-depth])
