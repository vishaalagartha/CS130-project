from multiprocessing import Pool
from psaw import PushshiftAPI

def fetch(ranges):
    gen =  api.search_comments(subreddit='nba', before=ranges['before'],
            after=ranges['after'])

    batch_count = 0
    text = ''
    # generator returns in batches of 50
    for g in gen:
        try:
            text+=(g.body+' ')
        except:
            pass
    return text

nthreads = 5
start_date = 1541246800
end_date = 1541266115

api = PushshiftAPI()
size = int((end_date-start_date)/nthreads)
date_ranges = []
while end_date>start_date:
    date_ranges.append({'after': end_date-size, 'before': end_date})
    end_date -= size
with Pool(len(date_ranges)) as p:
    l = p.map(fetch, date_ranges)
all_text = ''.join(l)
    
print(all_text)
