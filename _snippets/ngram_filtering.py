from collections import Counter

FNAME = 'google-10000-english-usa.txt'
# google-10000-english.txt google-10000-english-usa.txt Oxford 3000.txt  Oxford 5000.txt words.txt


def split_word_to_ngrams(word, n):
    return [word[index:index+n] for index in range(len(word) - n + 1)]


def modify_counter(counter, lst, increment):
    for elem in lst:
        counter[elem] += increment


def modify_combinations(combinations_counter, word, filtered, combination_len, increment):
    word_ngrams = split_word_to_ngrams(word, combination_len)
    modify_counter(combinations_counter, [ngram for ngram in word_ngrams if ngram not in filtered], increment)


#def get_filtering combinations(fname, combination_len, apply_combinations, threshold):
# params
fname = FNAME
combination_len = 2  # bigram/trigram/etc
apply_combinations = 2
# threshold = 0.05

assert combination_len > 1  # at least bigrams
assert apply_combinations > 0  # start with 1st

# get words and filter a little
words = [word.strip().lower() for word in open(fname).readlines()]
init_N = len(words)
print(f'uploaded {init_N} words from {fname}')
words = set(words)  # drop same
print(f'dropped {init_N - len(words)} repetitions')
# drop words that are impossible to filter out
words = [word for word in words if len(set(split_word_to_ngrams(word, combination_len))) >= apply_combinations]  # drop 'iii', 'abab', etc
words = [(word, set()) for word in words]  # word plus list of combinations that were used on it
print(f'dropped {init_N - len(words)} bad words (including repetitions)')
N = len(words)

# run processing
apply_combinations_stage = 1
prev_len = -1
while apply_combinations_stage <= apply_combinations:
    print(f'START cycle: {init_N=} {N=} {apply_combinations_stage=}')
    combinations = Counter()
    for word, filtered in words:
        modify_combinations(combinations, word, filtered, combination_len, +1)

    #
    step = 1
    processing_words = list(words)
    while len(processing_words) > 0:
        # process single best filtering ngram
        new_processing_words = []
        best_combination = combinations.most_common(1)[0][0]
        for word, filtered in processing_words:
            assert len(filtered) < apply_combinations_stage
            if best_combination in filtered:  # cannot filter right now, already used this one on the world
                new_processing_words.append((word, filtered))
            elif best_combination not in word:  # keep word, can't filter with current combination
                new_processing_words.append((word, filtered))
            else:  # drop word
                modify_combinations(combinations, word, filtered, combination_len, -1)
                filtered.add(best_combination)
        #
        processing_words = new_processing_words
        print(f'{apply_combinations_stage=} {step=} {best_combination=} {len(new_processing_words)=}')
        step += 1
        if len(new_processing_words) == prev_len:  # could not drop words on previous step
            print('\n\nDEBUG STOP')
            print(combinations)
            print(new_processing_words)
            break
        prev_len = len(new_processing_words)
    #
    apply_combinations_stage += 1

print('min power', 26**(combination_len+apply_combinations-1))  # amount of all permutations

"""
1 stage:
bigrams 100 lc 496
trigrams  1057 tft 500

some are impossible ti filter our
"""