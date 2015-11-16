__author__ = 'jack'

NUM_CODEWORDS = 12

wordmap = [[[None, 0] for i in range(NUM_CODEWORDS)] for j in range(NUM_CODEWORDS)]


class CodeWord:
    def __init__(self, word, score=0, valid=True):
        self.word = word
        self.score = score
        self.valid = valid

    def __str__(self):
        prefix = '' if self.valid else '*'
        return prefix + self.word

    def __repr__(self):
        return "{word} :: {score}".format(word=self.word, score=self.score)


def retrieve_codewords():
    codewords = []
    print("Enter the {numwords} codewords:".format(numwords=NUM_CODEWORDS))
    for i in range(NUM_CODEWORDS):
        codeword = CodeWord(raw_input())
        codewords.append(codeword)
    return codewords


def score_words(codewords):
    for i,word1 in enumerate(codewords):
        if i + 1 != len(codewords):
            for j,word2 in enumerate(codewords[i+1::]):
                k = i + 1 + j  # calculate the actual index of word2 since it is offset by i+1
                score = calculate_score(word1.word, word2.word)
                word1.score += score
                word2.score += score
                update_wordmap(i,k, -1 if i == k else score)


def update_scores(codewords):
    for word1 in codewords:
        word1.score = 0
    for word1 in codewords:
        if word1.valid:
            for word2 in codewords:
                if word2.valid:
                    score = calculate_score(word1.word, word2.word)
                    word1.score += score
                    word2.score += score


def try_word(codewords, suggestion=None):
    if not suggestion:
        index = int(raw_input("Input index of word to try: "))
    else:
        index = codewords.index(suggestion)
    likeness = int(raw_input("Likeness: "))
    for j in range(len(wordmap[index])):
        wordscore = wordmap[index][j][1]
        if wordscore != likeness:
            codewords[j].valid = False


def suggest_word(codewords):
    sorted_codewords = sorted((cw for cw in codewords if cw.valid), key=lambda codeword: codeword.score, reverse=True)
    suggested_word = sorted_codewords[0]
    print
    print "Try: {0}".format(suggested_word)
    return suggested_word


def init_wordmap(codewords):
    for i,word1 in enumerate(codewords):
        for j,word2 in enumerate(codewords):
            wordmap[i][j][0] = word1
            update_wordmap(i,j, -1 if i == j else 0)


def print_wordmap(codewords):
    wordlen = len(codewords[0].word)
    wordspace = wordlen + 2
    print "Scoremap:"
    print "{0:{1}}".format(' ', wordspace),
    for word in codewords:
        print "{0:>{1}}".format(str(word), wordspace),
    print
    for i,word1 in enumerate(codewords):
        print "{0:>{1}}".format(str(word1), wordspace),
        for j,word2 in enumerate(codewords):
            score = wordmap[i][j][1]
            print "{0:>{1}}".format(score, wordspace),
        print


def print_words(codewords):
    for word in codewords:
        if word.valid:
            print repr(word)
    print


def update_wordmap(j,k,score):
    wordmap[j][k][1] = score
    wordmap[k][j][1] = score


def calculate_score(word1, word2):
    score = 0
    for i in range(len(word1)):
        if word1[i] == word2[i]:
            score += 1
    return score


def is_unsolved(codewords):
    num_remaining = NUM_CODEWORDS
    for word in codewords:
        if not word.valid:
            num_remaining -= 1
    return num_remaining > 1


def main():
    codewords = retrieve_codewords()
    init_wordmap(codewords)
    score_words(codewords)
    print_words(codewords)
    print_wordmap(codewords)
    while is_unsolved(codewords):
        suggested_word = suggest_word(codewords)
        #try_word(codewords, suggested_word)
        try_word(codewords)
        print_words(codewords)
        print_wordmap(codewords)
        update_scores(codewords)

    for word in codewords:
        if word.valid:
            print
            print "The codeword is: {word}".format(word=word)

if __name__ == '__main__':
    main()


