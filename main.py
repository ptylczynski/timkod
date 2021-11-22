# Press the green button in the gutter to run the script.
from language_approximation.approximator import CharLanguageApproximator

if __name__ == '__main__':
    # approximator = SentenceLanguageApproximator()
    approximator = CharLanguageApproximator()
    approximator.fit('language_approximation/norm_wiki_sample.txt')
    print(approximator.generate(20, 5, 'result.txt'))
