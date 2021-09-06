import Tree

verbose = False


def printV(*args):
    if verbose:
        print(*args)

# A Python implementation of the AIMA CYK-Parse algorithm in Fig. 23.5 (p. 837).


def CYKParse(words, grammar):
    T = {}
    P = {}  # table of probabilitys
    # Instead of explicitly initializing all P[X, i, k] to 0, store
    # only non-0 keys, and use this helper function to return 0 as needed.

    def getP(X, i, k):  # X = lexical category
        key = str(X) + '/' + str(i) + '/' + str(k)
        if key in P:
            return P[key]
        else:
            return 0
    # Insert lexical categories for each word
    for i in range(len(words)):
        for X, p in getGrammarLexicalRules(grammar, words[i]):
            P[X + '/' + str(i) + '/' + str(i)] = p
            T[X + '/' + str(i) + '/' + str(i)] = Tree.Tree(X,
                                                           None, None, lexiconItem=words[i])
    printV('P:', P)
    printV('T:', [str(t)+':'+str(T[t]) for t in T])

    # ADDED: Construct X_i:k from Y_i:k, span of 1
    for i in range(len(words)):
        for X, Y, Z, p in getGrammarSyntaxRules(grammar):
            if Z is None:
                PY = getP(Y, i, i) * p
                if PY > getP(X, i, i):
                    printV('     C171F: inserting from', i, '-', i, ' ', X, '->', T[Y+'/'+str(i)+'/'+str(i)],
                           'because', PY, '=', getP(
                               Y, i, i), '*', p, '>', getP(X, i, i), '=',
                           'getP(' + X + ',' + str(i) + ',' + str(i) + ')')
                    P[X + '/' + str(i) + '/' + str(i)] = PY
                    T[X + '/' + str(i) + '/' + str(i)] = Tree.Tree(X,
                                                                   None, None, lexiconItem=T[Y+'/'+str(i)+'/'+str(i)])

    # Construct X_i:j from Y_i:j + Z_j+i:k, shortest spans first
    for i, j, k in subspans(len(words)):
        for X, Y, Z, p in getGrammarSyntaxRules(grammar):   # X -> Y Z
            if Z is not None:   # CNF
                # probability of X -> Y Z
                PYZ = getP(Y, i, j) * getP(Z, j+1, k) * p
                if PYZ > getP(X, i, k):
                    P[X + '/' + str(i) + '/' + str(k)] = PYZ
                    T[X + '/' + str(i) + '/' + str(k)] = Tree.Tree(X,
                                                                   T[Y+'/'+str(i)+'/'+str(j)], T[Z+'/'+str(j+1)+'/'+str(k)])
            else:   # C171F, X_i:k from Y_i:k
                # probability of X -> Y
                PY = getP(Y, i, k) * p
                if PY > getP(X, i, k):
                    P[X + '/' + str(i) + '/' + str(k)] = PY
                    T[X + '/' + str(i) + '/' + str(k)] = Tree.Tree(X,
                                                                   None, None, lexiconItem=T[Y+'/'+str(i)+'/'+str(k)])

    printV('T:', [str(t)+':'+str(T[t]) for t in T])
    #printV('P:', P)
    return T, P

# Python uses 0-based indexing, requiring some changes from the book's
# 1-based indexing: i starts at 0 instead of 1


def subspans(N):
    for length in range(2, N+1):
        for i in range(N+1 - length):
            k = i + length - 1
            for j in range(i, k):
                yield i, j, k

# These two getXXX functions use yield instead of return so that a single pair can be sent back,
# and since that pair is a tuple, Python permits a friendly 'X, p' syntax
# in the calling routine.


def getGrammarLexicalRules(grammar, word):
    # if unknown word
    if word not in [rule[1] for rule in grammar['lexicon']]:
        yield 'Unknown', 0.05

    else:
        for rule in grammar['lexicon']:

            # if rule[1] == word:
            #     yield rule[0], rule[2]
            if rule[1].lower() == word.lower():
                yield rule[0], rule[2]


def getGrammarSyntaxRules(grammar):
    rulelist = []
    for rule in grammar['syntax']:
        # ['S', 'Greeting', 'S', 0.25]  CNF
        # ['S', 'Greeting', None, 0.25] C1F
        yield rule[0], rule[1], rule[2], rule[3]


def getGrammarWeather():
    return {
        'syntax': [
            ###
            ['Name', 'Unknown', None, 0.05],

            ['S', 'NP', 'VP', 0.5],
            ['S', 'WQuestion', 'VP', 0.25],
            ['S', 'Verb', 'NP', 0.3],
            ['S', 'WQuestion', 'NP', 0.3],
            ['S', 'WQuestion', 'S', 0.3],

            ['VP', 'Verb', 'NP', 0.3],
            ['VP', 'Verb', 'NP+AdverbPhrase', 0.3],
            ['VP', 'Verb', 'AdverbPhrase', 0.3],
            ['VP', 'Adverb+VP+Adverb', 'AdverbPhrase', 0.2],

            ['Adverb+VP', 'Adverb', 'VP', 1],
            ['Adverb+VP+Adverb', 'Adverb+VP', 'Adverb', 1],


            ['NP', 'Article', 'NP', 0.2],
            ['NP', 'Noun', None, 0.2],
            ['NP', 'Name', None, 0.2],
            ['NP', 'Pronoun', None, 0.2],
            ['NP', 'NP', 'NP', 0.2],

            ['NP', 'Adjective', 'Noun', 0.2],



            ['Adverb', 'Article', 'Adverb', 0.4],

            ['NP+AdverbPhrase', 'NP', 'AdverbPhrase', 0.4],
            ['NP+AdverbPhrase', 'NP', 'Adverb', 0.35],
            ['NP+AdverbPhrase', 'AdverbPhrase', 'NP', 0.1],
            ['NP+AdverbPhrase', 'Adverb', 'NP+AdverbPhrase', 0.05],
            ['NP+AdverbPhrase', 'Article', 'NP+AdverbPhrase', 0.05],
            ['NP+AdverbPhrase', 'Adverb', 'NP', 0.1],

            ['AdverbPhrase', 'Preposition', 'NP', 0.4],
            ['AdverbPhrase', 'Adverb', 'AdverbPhrase', 0.2],
            ['AdverbPhrase', 'AdverbPhrase', 'Adverb', 0.4],

        ],
        'lexicon': [
            ['Greeting', 'hi', 0.5],
            ['Greeting', 'hello', 0.5],

            ['WQuestion', 'what', 0.5],
            ['WQuestion', 'when', 0.25],
            ['WQuestion', 'which', 0.1],
            ['WQuestion', 'will', 0.15],
            ['WQuestion', 'how', 0.15],

            ['Verb', 'am', 0.25],
            ['Verb', 'is', 0.5],
            ['Verb', 'be', 0.25],
            ['Verb', 'use', 0.25],


            ['Pronoun', 'I', 1.0],

            ['Noun', 'man', 0.2],
            ['Noun', 'name', 0.2],
            ['Noun', 'temperature', 0.6],
            ['Noun', 'weather', 0.6],
            ['Noun', 'precipitation', 0.6],
            ['Noun', 'pressure', 0.6],
            ['Noun', 'precip', 0.6],
            ['Noun', 'height', 0.6],
            ['Noun', 'wind', 0.6],
            ['Noun', 'speed', 0.6],
            ['Noun', 'humidity', 0.6],
            ['Noun', 'system', 0.6],
            ['Noun', 'celsius', 0.6],
            ['Noun', 'fahrenheit', 0.6],



            ['Noun', 'snow', 0.6],
            ['Noun', 'rain', 0.6],
            ['Noun', 'sunshine', 0.6],
            ['Noun', 'frost', 0.6],
            ['Noun', 'thunder', 0.6],
            ['Noun', 'overcast', 0.6],



            ['Noun', 'chance', 0.6],



            ['Article', 'the', 0.7],
            ['Article', 'a', 0.3],
            ['Article', 'this', 0.3],
            ['Article', 'next', 0.3],
            ['Article', 'last', 0.3],
            ['Article', 'of', 0.3],

            ['Adjective', 'my', 1.0],
            ['Adjective', 'highest', 1.0],
            ['Adjective', 'lowest', 1.0],
            ['Adjective', 'metric', 1.0],
            ['Adjective', 'imperial', 1.0],
            ['Adjective', 'weekly', 1.0],
            ['Adjective', 'average', 0.6],
            ['Adjective', 'much', 0.6],

            ['Adverb', 'now', 0.3],
            ['Adverb', 'today', 0.3],
            ['Adverb', 'tomorrow', 0.2],
            ['Adverb', 'yesterday', 0.2],
            ['Adverb', 'week', 0.2],


            ['Preposition', 'with', 0.5],
            ['Preposition', 'in', 0.5],

            ['Unknown', '', 0.05]
        ]
    }


# Unit testing code
if __name__ == '__main__':
    verbose = True

    CYKParse(['my', 'name', 'is', 'Peter'], getGrammarWeather())
    CYKParse(['hi', 'I', 'am', 'Peter'], getGrammarWeather())
    CYKParse(['what', 'is', 'the', 'temperature',
             'in', 'Irvine'], getGrammarWeather())
    CYKParse(['what', 'is', 'the', 'temperature', 'in',
             'Irvine', 'now'], getGrammarWeather())
    CYKParse(['what', 'is', 'the', 'temperature', 'now',
             'in', 'Irvine'], getGrammarWeather())
    CYKParse(['what', 'is', 'now', 'the', 'temperature',
             'in', 'Irvine'], getGrammarWeather())
    CYKParse(['will', 'tomorrow', 'be', 'hotter', 'than',
             'today', 'in', 'Pasadena'], getGrammarWeather())
    CYKParse(['will', 'yesterday', 'be', 'hotter', 'than',
             'tomorrow', 'in', 'Pasadena'], getGrammarWeather())
