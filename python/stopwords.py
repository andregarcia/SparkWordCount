from functions import strip_accents


class Stopwords:

    def __init__(self):
        self.stopwords = self.__load_stopwords()

    def __load_stopwords(self):
        stopwords = set()
        with open('stopwords.txt', 'r') as f:
            for line in f:
                line = line.strip().lower()
                if not line or line[0] == '#':
                    continue
                stopwords.add(strip_accents(line))
        return stopwords

    def is_stopword(self, w):
        return strip_accents(w.lower()) in self.stopwords



if __name__=='__main__':
    stopwords = Stopwords()
    print(stopwords.is_stopword('a'))
    print(stopwords.is_stopword('brasil'))
