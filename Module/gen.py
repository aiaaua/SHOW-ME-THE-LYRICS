from parse import Parser
from alpha import Alphabet
from konlpy.tag import Okt
from konlpy.tag import Mecab
import re

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
    
	def _check_digit(self, word_list) :
		for word in word_list :
			if word.isdigit() :
				break
		else : return False
		return True
        
	def _check_jungsung_rhyme(self, prev_word, pres_word, prev_pres_word, end_symbol) :
		for i in range(4) : 
			prev_jungsung_rhyme = self._jungsung_rhyme(prev_word)
			pres_jungsung_rhyme = self._jungsung_rhyme(pres_word)
			print(pres_word)

			if prev_jungsung_rhyme == pres_jungsung_rhyme :
				break
			else : 
				while True : 
					pres_word = self._get_next_word(prev_pres_word)
					if self._check_digit(list(pres_word[0])) :
						continue
					if pres_word == end_symbol : 
						continue
					else : break
		else : 
			return False, pres_word
		return True, pres_word
        
	def _check_jongsung_rhyme(self, prev_word, pres_word, prev_pres_word, end_symbol) :
		for i in range(4) :
			prev_jongsung_rhyme = self._jongsung_rhyme(prev_word)
			pres_jongsung_rhyme = self._jongsung_rhyme(pres_word)
			print('pres_word : ', pres_word)
            
			if prev_jongsung_rhyme == pres_jongsung_rhyme and prev_jongsung_rhyme != [' '] :
				break
			else : 
				while True : 
					pres_word = self._get_next_word(prev_pres_word)
					if self._check_digit(list(pres_word[0])) :
						continue
					if pres_word == end_symbol : 
						continue
					else : break
		else : 
			return False, pres_word
		return True, pres_word

	def _check_rhyme(self, sentence, prev_sentence, depth, word_separator, end_symbol) : 
		prev_last_word = sentence[(-depth-1):(-depth)]
		last_word = sentence[(-depth):(-depth+1)]
		prev = prev_sentence.split(word_separator)
		print('prev_last_word : ', prev_last_word)
		print('last_word : ', last_word)
        
		check_d1 = self._check_digit(list(prev_last_word[0]))
		print('check_d1 : ', check_d1)
		check_d2 = self._check_digit(list(last_word[0]))
		print('check_d2 : ', check_d2)
		check_d3 = self._check_digit(list(prev[-1]))
		print('check_d3 : ', check_d3)
            
		if check_d1 or check_d2 or check_d3 :
			return sentence
        
		else : 
			check_r1, last_word = self._check_jungsung_rhyme(prev[-1], last_word[0], prev_last_word, end_symbol[0])
			sentence[(-depth):(-depth+1)] = last_word
                        
			if check_r1 != True :
				check_r2, last_word = self._check_jongsung_rhyme(prev[-1], last_word[0], prev_last_word, end_symbol[0])
				sentence[(-depth):(-depth+1)] = last_word
			return sentence

	#===UPDATE===
	def _get_word_pos(self, prev_sentence, mode = 'okt') : #앞 문장의 명사 랜덤 출력
		### 변수 설명 ###
        # prev_sentence: 이전 문장
        # mode = 'okt' / 'mecab'
        #################
		
		if mode == 'mecab' :
			posGen = Mecab('C://mecab') 
		else : 
			posGen = Okt()
		sentence_pos = posGen.pos(prev_sentence) #앞 문장 형태소 분석    
		randomNoun = None
		nounlist = [Parser.SENTENCE_START_SYMBOL]
	    
		for i in sentence_pos :
			if i[1] == 'Noun' or re.match('NP|NNG|NNP',i[1]) != None : #명사리스트 (Noun : okt, NNG/NNP/NP : mecab)
				nounlist.append(i[0]) #명사 모두 추출

		idx = self.rnd.randint_min(0,len(nounlist)-1) #randint(0, len(nounlist)-1) #랜덤 선택
		randomNoun = nounlist[idx]
	    
		if randomNoun == Parser.SENTENCE_START_SYMBOL : #선택한 랜덤값이 '^' 경우 
			return None
		else :
			return randomNoun
        
	def generate(self, word_separator, prev_sentence = None):
		depth = self.db.get_depth()
        
		#===UPDATE===
		if prev_sentence == None : # 앞 문장이 없으면
			sentence = [Parser.SENTENCE_START_SYMBOL] * (depth - 1)
		else : 
			word_noun = self._get_word_pos(prev_sentence,'mecab') #명사 랜덤 추출
			print('word_noun : ',word_noun)
	        
			if word_noun == None :
				sentence = [Parser.SENTENCE_START_SYMBOL] * (depth - 1)
			else : 
				sentence = [Parser.SENTENCE_START_SYMBOL] * (depth - 1) + [word_noun]
		#===UPDATE===
		#sentence = [Parser.SENTENCE_START_SYMBOL] * (depth - 1)
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
					if prev_sentence == None :
						break
					else : 
						sentence = self._check_rhyme(sentence, prev_sentence, depth, word_separator, end_symbol)
						sentence.append(end_symbol)
						break
			word = self._get_next_word(tail)
			sentence.append(word)
		
		return word_separator.join(sentence[depth-1:][:1-depth])
