import random


class CharLanguageApproximator:
    def __init__(self):
        self._samples: [str] = []
        self._file_content: str = ''
        self._probabilities: dict = {}
        self._conditional_probabilities: dict = {}
        self.MAX_DEGREE: int = 5

    def fit(self, data_file_path: str):
        self._tokenize(data_file_path)
        self._analyze()

    def _tokenize(self, data_file_path: str):
        file_content = ''
        with open(data_file_path, 'r') as file:
            for line in file:
                file_content += line
        self._file_content = file_content
        self._samples = file_content.split(' ')

    def _analyze(self):
        occurrences, total_tokens = self._count()
        self._probabilities, self._conditional_probabilities = self._find_probabilities(occurrences, total_tokens)

    def _count(self):
        occurrences: dict = {}
        total_tokens: [int] = [0 for i in range(self.MAX_DEGREE + 1)]
        for end_pos in range(1, len(self._file_content)):
            for degree in range(1, self.MAX_DEGREE + 1):
                start_pos = end_pos - degree
                if start_pos < 0:
                    continue
                total_tokens[degree] += 1
                token = self._file_content[start_pos:end_pos]
                if token in occurrences:
                    occurrences[token] += 1
                else:
                    occurrences[token] = 1
        return occurrences, total_tokens

    def _find_probabilities(self, occurrences: dict, total_tokens: []):
        probabilities = {}
        conditional_probabilities = {}
        for token in occurrences:
            probabilities[token] = occurrences[token] / total_tokens[len(token)]

        for token in occurrences.keys():
            if len(token) > 1:
                sub_token = token[:-1]
                conditional_probabilities[token] = probabilities[token] / probabilities[sub_token]
        return probabilities, conditional_probabilities

    def generate(self, length: int, degree: int, output_file_path: str):
        sentence = self._generate_sentence(length, degree)
        self._save_sentence(sentence, output_file_path)
        return sentence

    def _generate_sentence(self, length: int, degree: int):
        generate_sentence: str = ''
        token = ''
        for i in range(1, length + 1):
            chosen_letter = self._choose_random(token)
            generate_sentence += chosen_letter
            if i >= degree:
                token = token[1:] + chosen_letter
            else:
                token += chosen_letter
        return generate_sentence

    def _save_sentence(self, sentence: str, output_file_path: str):
        with open(output_file_path, "w+") as file:
            file.write(sentence)

    def _choose_random(self, prefix: str):
        rnd = random.uniform(0, 1)
        collected = 0
        if prefix == '':
            for key in self._probabilities.keys():
                if len(key) == 1:
                    collected += self._probabilities[key]
                    if collected > rnd:
                        return key
        else:
            for key in self._conditional_probabilities.keys():
                if key[:-1] == prefix:
                    collected += self._conditional_probabilities[key]
                    if collected > rnd:
                        return key[len(key) - 1]


class SentenceLanguageApproximator:
    def __init__(self):
        self.MAX_DEGREE: int = 5
        self._probabilities: dict = {}
        self._conditional_probabilities: dict = {}

    def fit(self, data_file_path: str):
        self._tokenize(data_file_path)
        self._analyze()

    def _tokenize(self, data_file_path: str):
        file_content = ''
        with open(data_file_path, 'r') as file:
            for line in file:
                file_content += line
        self._file_content = file_content
        self._samples = file_content.split(' ')

    def _analyze(self):
        occurrences, total_tokens = self._count()
        self._probabilities, self._conditional_probabilities = self._find_probabilities(occurrences, total_tokens)

    def _find_probabilities(self, occurrences: dict, total_tokens: []):
        probabilities = {}
        conditional_probabilities = {}
        for token in occurrences:
            probabilities[token] = occurrences[token] / total_tokens[len(token)]

        for token in occurrences.keys():
            if len(token) > 1:
                sub_token = token[:-1]
                conditional_probabilities[token] = probabilities[token] / probabilities[sub_token]
        return probabilities, conditional_probabilities

    def _count(self):
        occurrences: dict = {}
        total_tokens: [int] = [0 for i in range(self.MAX_DEGREE + 1)]
        for end_pos in range(1, len(self._samples)):
            for degree in range(1, self.MAX_DEGREE + 1):
                start_pos = end_pos - degree
                if start_pos < 0:
                    continue
                total_tokens[degree] += 1
                token = tuple(self._samples[start_pos:end_pos])
                if token in occurrences:
                    occurrences[token] += 1
                else:
                    occurrences[token] = 1
        return occurrences, total_tokens

    def generate(self, length: int, degree: int, output_file_path: str):
        sentence: [str] = self._generate_sentence(length, degree)
        self._save_sentence(sentence, output_file_path)
        return sentence

    def _save_sentence(self, sentence: [str], output_file_path: str):
        with open(output_file_path, "w+") as file:
            file.write(
                ' '.join(sentence)
            )

    def _generate_sentence(self, length: int, degree: int):
        generate_sentence: [str] = []
        token: [str] = []
        for i in range(1, length + 1):
            chosen_letter = self._choose_random(token)
            generate_sentence.append(chosen_letter)
            if i >= degree:
                token = token[1:]
                token.append(chosen_letter)
            else:
                token.append(chosen_letter)
        return generate_sentence

    def _choose_random(self, prefix: str):
        rnd = random.uniform(0, 1)
        collected = 0
        if len(prefix) == 0:
            for key in self._probabilities.keys():
                if len(key) == 1:
                    collected += self._probabilities[key]
                    if collected > rnd:
                        return key[0]
        else:
            for key in self._conditional_probabilities.keys():
                if same(key[:-1], prefix):
                    collected += self._conditional_probabilities[key]
                    if collected > rnd:
                        return key[len(key) - 1]


def same(el1: (), el2: ()) -> bool:
    if len(el1) != len(el2):
        return False
    for i in range(len(el1)):
        if el1[i] != el2[i]:
            return False
    return True
