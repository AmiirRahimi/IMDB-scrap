import requests
import time
from bs4 import BeautifulSoup

def complete_url(movie_link):
 complete_url = f"https://www.imdb.com{movie_link}"
 return complete_url

def get_page_info(url):
 headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'accept-language': 'en-US,en;q=0.9,fa;q=0.8'
 }
 time.sleep(2)
 response = requests.get(url, headers=headers, cookies={'cookie_name': 'cookie_value'})
 if response.status_code == 200:
  soup = BeautifulSoup(response.content, 'html.parser')
  return soup
 return response.status_code

def get250MoviesHref():
 _250MoviesPage = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
 movies_doc = get_page_info(_250MoviesPage)
 if movies_doc:
  movies_link = movies_doc.find_all('a', class_='ipc-title-link-wrapper')
  movies_href = []
  for link in movies_link:
     movies_href.append(link.get('href'))
  movies_href = [complete_url(s) for s in movies_href if 'chttp_t' in s.lower()]
  return movies_href
 
def calculate_run_time(run_time):
 count = 0
 run_time = run_time.split(' ')
 for i in run_time:
   if 'h' in i:
    count += int(i.split('h')[0]) * 60
   if 'm' in i: 
    count += int(i.split('m')[0])
 return count

def get_genres(genres_tag):
 genres = []
 for genre in genres_tag:
  genres.append(genre.find('span', class_='ipc-chip__text').text)
 return genres

def get_writers_or_stars(writers_tag):
 writers = []
 for writer in writers_tag:
  writers.append({'name': writer.find('a').text, 'id':writer.find('a').get('href').split('/')[-2]})
 return writers

def get_gross_us_canada(gross):
   if 'Gross US & Canada' in gross.text:
      gross = gross.find('div').find('ul').find('li').find('span').text
      new_gross = gross.replace(',', '')
      new_gross = int(new_gross.replace('$', ''))
   else:
    new_gross = None
   return new_gross

def get_year_parental_guide_run_time(list):
   if len(list.findAll('li')) == 2:
    year = list.findAll('li')[0].text
    runtime = calculate_run_time(list.findAll('li')[1].text)
    return {'year':year,'parental_guide':None, 'runtime':runtime}
   else:
    year = list.findAll('li')[0].text
    parental_guide = list.findAll('li')[1].text
    runtime = calculate_run_time(list.findAll('li')[2].text)
    return {'year':year,'parental_guide':parental_guide, 'runtime':runtime}

def get_director(a):
   director_name = a.text
   id = a.get('href').split('/')[-2]
   return {'name': director_name, 'id': id}


def get_movies_info(movie_url):
 movie_doc = get_page_info(movie_url)
 try:
  title = movie_doc.find('span', class_='hero__primary-text').text
 except:
  title = ''

 try:
  year = get_year_parental_guide_run_time(movie_doc.findAll('ul', class_=['ipc-inline-list','ipc-inline-list--show-dividers','sc-d8941411-2','cdJsTz','baseAlt'])[1])['year']
 except:
  year = None

 try:
  parental_guide = get_year_parental_guide_run_time(movie_doc.findAll('ul', class_=['ipc-inline-list','ipc-inline-list--show-dividers','sc-d8941411-2','cdJsTz','baseAlt'])[1])['parental_guide']
 except:
  parental_guide = ''

 try:
  runtime = get_year_parental_guide_run_time(movie_doc.findAll('ul', class_=['ipc-inline-list','ipc-inline-list--show-dividers','sc-d8941411-2','cdJsTz','baseAlt'])[1])['runtime']
 except:
  runtime = None

 try:
  director = get_director(movie_doc.findAll('ul', class_=['ipc-inline-list','ipc-inline-list--show-dividers','sc-d8941411-2','cdJsTz','baseAlt'])[2].findAll('li')[0].find('a'))
 except:
  director = ''

 try:
  writer = get_writers_or_stars(movie_doc.findAll('ul', class_=['ipc-inline-list','ipc-inline-list--show-dividers','ipc-inline-list--inline','ipc-metadata-list-item__list-content baseAlt'])[3].findAll('li', class_=['ipc-inline-list__item']))
 except:
  writer = ''

 try:
  genre = get_genres(movie_doc.findAll('a', class_=['ipc-chip','ipc-chip--on-baseAlt']))
 except:
  genre = ''

 try:
  star = get_writers_or_stars(movie_doc.findAll('ul', class_=['ipc-inline-list','ipc-inline-list--show-dividers','ipc-inline-list--inline','ipc-metadata-list-item__list-content baseAlt'])[4].findAll('li', class_=['ipc-inline-list__item']))
 except:
  star = ''

 try:
  gross_us_canada = get_gross_us_canada(movie_doc.findAll('div', class_=['sc-f65f65be-0','bBlII'])[3].find('ul').findAll('li')[2])
 except:
  gross_us_canada = None
 
 movie_info = {'id':movie_url.split('/')[-2],'title':title, 'year':year, 'parental_guide':parental_guide, 'runtime':runtime, 'genre':genre, 'director':director, 'writer':writer, 'star':star, 'gross_us_canada':gross_us_canada}

 return movie_info

# print(get_movies_info('https://www.imdb.com/title/tt23849204/?ref_=chttp_t_53'))



