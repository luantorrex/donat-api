from app.initials import initialStates
from GoogleNews import GoogleNews
from unidecode import unidecode

googlenews = GoogleNews()

def callGoogle(state):
    try:
        googlenews = GoogleNews(lang='pt')
        googlenews.search('covid ' + state)
        newsData = googlenews.results(sort=True)
        returned_dict = {}

        if state == 'Brasil':
            returned_dict['titulo'] = newsData[0]['title']
            returned_dict['desc'] = newsData[0]['desc']
            returned_dict['link'] = newsData[0]['link']
            returned_dict['fonte'] = newsData[0]['media']
            returned_dict['data'] = newsData[0]['date']
            return returned_dict

        for row in newsData:
            this_row = row['title']
            if state in this_row \
                or initialStates[state] in this_row \
                or state.split(' ')[0] in this_row:
                returned_dict['titulo'] = row['title']
                returned_dict['desc'] = row['desc']
                returned_dict['link'] = row['link']
                returned_dict['fonte'] = row['media']
                returned_dict['data'] = row['date']
                return returned_dict
            elif state == 'Minas Gerais' and ('BH' or 'bh') in this_row:
                returned_dict['titulo'] = row['title']
                returned_dict['desc'] = row['desc']
                returned_dict['link'] = row['link']
                returned_dict['fonte'] = row['media']
                returned_dict['data'] = row['date']
                return returned_dict
        
        returned_dict['titulo'] = newsData[0]['title']
        returned_dict['desc'] = newsData[0]['desc']
        returned_dict['link'] = newsData[0]['link']
        returned_dict['fonte'] = newsData[0]['media']
        returned_dict['data'] = newsData[0]['date']
        return returned_dict
    except:
        return 'Google News API is not working'