from app.initials import initialStates
from GoogleNews import GoogleNews
from unidecode import unidecode

googlenews = GoogleNews()

def callGoogle(state):
    googlenews = GoogleNews(lang='pt')
    googlenews.search('covid ' + state)
    newsData = googlenews.get_texts()

    if state == 'Brasil':
        return newsData[0]
    
    for row in newsData:
        this_row = unidecode(row)
        if state in this_row \
            or initialStates[state] in this_row \
            or state.split(' ')[0] in this_row:
            return row
        elif state == 'Minas Gerais' and ('BH' or 'bh') in this_row:
            return row
    return newsData[0]