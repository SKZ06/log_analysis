import logging
import matplotlib.pyplot as plt
"""
    in: list of results (dict), geo_location module
    out: 3 charts (failed by country, success by user, failed invalid user)
"""
logger=logging.getLogger('dashboard')
handler=logging.FileHandler('dashboard.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.ERROR)

def count(values):
    counts={}
    for value in values:
        counts[value]=counts.get(value, 0)+1
    return counts

def top(counts, n=10):
    return sorted(counts.items(), key=lambda item: item[1], reverse=True)[:n]

def draw_bar(data, title, xlabel, file_name):
    try:
        names=[item[0] for item in data]
        values=[item[1] for item in data]
        plt.figure(figsize=(10, 6))
        plt.bar(names, values)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel('attempts')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(file_name)
    except Exception as e:
        logger.error('cannot draw '+title+' : '+str(e))

def failed_by_country(results, get_country):
    countries=[get_country(r['ip']) for r in results if r['status']=='failed']
    draw_bar(top(count(countries)), 'Failed attempts by country', 'country', 'failed_by_country.png')

def success_by_user(results):
    users=[r['user'] for r in results if r['status']=='success']
    draw_bar(top(count(users)), 'Successful attempts by user', 'user', 'success_by_user.png')

def failed_invalid_user(results):
    users=[r['user'] for r in results if r['status']=='failed' and r['invalid']]
    draw_bar(top(count(users)), 'Failed attempts with invalid user', 'invalid user', 'failed_invalid_user.png')

def show():
    plt.show()