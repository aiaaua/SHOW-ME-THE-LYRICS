import re
import sys

"""
초성 중성 종성 분리 하기
유니코드 한글은 0xAC00 으로부터
초성 19개, 중성21개, 종성28개로 이루어지고
이들을 조합한 11,172개의 문자를 갖는다.
한글코드의 값 = ((초성 * 21) + 중성) * 28 + 종성 + 0xAC00
(0xAC00은 'ㄱ'의 코드값)
따라서 다음과 같은 계산 식이 구해진다.
유니코드 한글 문자 코드 값이 X일 때,
초성 = ((X - 0xAC00) / 28) / 21
중성 = ((X - 0xAC00) / 28) % 21
종성 = (X - 0xAC00) % 28
이 때 초성, 중성, 종성의 값은 각 소리 글자의 코드값이 아니라
이들이 각각 몇 번째 문자인가를 나타내기 때문에 다음과 같이 다시 처리한다.
초성문자코드 = 초성 + 0x1100 //('ㄱ')
중성문자코드 = 중성 + 0x1161 // ('ㅏ')
종성문자코드 = 종성 + 0x11A8 - 1 // (종성이 없는 경우가 있으므로 1을 뺌)
"""

class Alphabet :
	BASE_CODE = 44032 
	CHOSUNG =  588
	JUNGSUNG = 28
	CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
	JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
	JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

	def _get_alphabetic(self, word):
		split_word_list = list(word)
		chosung = list()
		jungsung = list()
		jongsung = list()

		for word in split_word_list:
			char_code = ord(word) - self.BASE_CODE

			char1 = int(char_code / self.CHOSUNG)
			chosung.append(self.CHOSUNG_LIST[char1])

			char2 = int((char_code - (self.CHOSUNG * char1)) / self.JUNGSUNG)
			jungsung.append(self.JUNGSUNG_LIST[char2])

			if word == split_word_list[-1] :
				char3 = int((char_code - (self.CHOSUNG * char1) - (self.JUNGSUNG * char2)))
				jongsung.append(self.JONGSUNG_LIST[char3])

		return jungsung, jongsung

	def get_jungsung_alphabetic(self, word) :
		jungsung, jongsung = self._get_alphabetic(word)
		return jungsung

	def get_jongsung_alphabetic(self, word) : 
		jungsung, jongsung = self._get_alphabetic(word)
		return jongsung
