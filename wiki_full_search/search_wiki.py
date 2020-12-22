import sys
import timeit

INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]
SEARCH_STRS = sys.argv[3].split(',')
NOT_F = True if len(sys.argv) > 4 and sys.argv[4] == 'not' else False

start_time = timeit.default_timer()

def filter_article(article):
    article = article.lower()
    for search_txt in SEARCH_STRS:
        if search_txt in article:
            return True
    return False

bytes = reads_counter = saved_article_counter = article_counter = 0
current_article = []
with open(INPUT_FILE ,'rt') as read_f, open(OUTPUT_FILE, 'a') as save_f:
    while True:
        lines = [i for i in read_f.readlines(1024*1024)]
        if not lines:
            break
        bytes += sum([len(line)+1 for line in lines])
        reads_counter += 1
        if reads_counter % 10 == 0:
            print(f'processed {round(bytes/1e9, 3)} GB \t{article_counter:,} articles \tsaved {saved_article_counter:,} articles')
        for line in lines:
            if line == '  <page>\n':
                article_counter += 1
                current_article = '\n'.join(current_article) + '\n'
                if filter_article(current_article) ^ NOT_F:
                    _ = save_f.write(current_article)
                    saved_article_counter += 1
                current_article = []
            current_article.append(line)

print(f'\nProcessed in {round(timeit.default_timer() - start_time)} seconds')
