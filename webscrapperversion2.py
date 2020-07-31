import requests
import pandas as pd
from bs4 import BeautifulSoup
from random import randint
from time import sleep
from functools import reduce
from multiprocessing import Pool
#url = "https://www.goodreads.com/shelf/show/to-read"
url = "https://www.goodreads.com/list/show/1.Best_Books_Ever"

class Url:
    def __init__(self, url):
        self.url = url

    def geturl(self):
        result = requests.get(url)
        soup = BeautifulSoup(result.text, 'html.parser')
        return soup


class Page_Url:
    
    all_url = []
    def get_pages(self):
        for i in range(2):
            self.all_url.append('https://www.goodreads.com/list/show/1.Best_Books_Ever?page=' + str(i+1))
        return self.all_url

class Book_Url:
    book_url = []

    def __init__(self, url):
        self.url = url

    def get_book_url(self):
        obj = Url(url)
        soup = obj.geturl()
        self.book_url.append([('/').join(url.split('/')[:-3]) + x.get('href') for x in soup.findAll('a', class_='bookTitle')])
        return self.book_url


class Author:
    def __init__(self, url):
        self.url = url
    
    author = []
    author_follower = []
    title = []
    rate = []
    desc = []
    book_format = []
    language = []
    similar_book = []
    review = []
    review_count = []
    rating_count = []
    def get_author(self):
        obj = Url(url)
        soup = obj.geturl()
        self.author.append(soup.find('span', itemprop='name').text)
        self.author_follower.append(soup.find('div', class_='bookAuthorProfile__followerCount').text.split('\n')[1])
        self.title.append(soup.find('h1', id='bookTitle').text.split('\n')[1].lstrip())
        self.rate.append(soup.find('span', itemprop='ratingValue').text.split('\n')[1].lstrip())
        self.desc.append(soup.find('div', class_='readable stacked').find_next('span').find_next('span').text)
        self.book_format.append(soup.find('div', class_='row').span.text)
        self.language.append(soup.find('div', itemprop="inLanguage").text)
        #self.review.append(soup.find('div', class_="reviewText stacked").text)
        self.review_count.append(soup.find('meta', itemprop='reviewCount').text.split('\n')[1].lstrip())
        self.rating_count.append(soup.find('meta', itemprop='ratingCount').text.split('\n')[1].lstrip())
        list1 = [x.a.img.get('alt') for x in soup.findAll('div', class_='js-tooltipTrigger tooltipTrigger')]
        similar = ''
        for i in list1:
            similar += str(i) + ","
        self.similar_book.append(similar)
        return self.author, self.author_follower, self.title, self.rate, self.desc, self.book_format, self.language, self.similar_book, self.review_count, self.rating_count



class Score:
    def __init__(self, url):
        self.url = url
    
    book_score = []
    def get_book_score(self):
        obj = Url(url)
        soup = obj.geturl()
        self.book_score.append([x.text.split('\n')[1].split(':')[1] for x in soup.findAll('span', class_='smallText uitext')])
        return self.book_score
    

class Genres:
    def __init__(self, url):
        self.url = url

    genres = []
    def get_genres(self):
        obj = Url(url)
        soup = obj.geturl()
        self.genres.append([x.text for x in soup.find_all('a', class_='actionLinkLite bookPageGenreLink')])
        return self.genres


class Author_Url:
    def __init__(self, url):
        self.url = url
    
    author_url = []
    def get_author_url(self):
        obj = Url(url)
        soup = obj.geturl()
        self.author_url.append([('/').join(url.split('/')[:-3]) + soup.find('div', class_='bookAuthorProfile__name').a.get('href')])
        return self.author_url


class Author_Info:
    def __init__(self, url):
        self.url = url
    
    author_rate = []
    no_of_author_rate = []
    no_of_review_author = []
    no_of_times_shelved = []

    def get_author_info(self):
        obj = Url(url)
        soup = obj.geturl()
        list1 = soup.find('div', class_='leftContainer').div.text.split('\n')[2:]
        self.author_rate.append(list1[0].lstrip().split(' ')[2])
        self.no_of_author_rate.append(list1[1].lstrip().split(' ')[0])
        self.no_of_review_author.append(list1[2].lstrip().split(' ')[0])
        self.no_of_times_shelved.append(list1[3].lstrip().split(' ')[1])
        return self.author_rate, self.no_of_author_rate, self.no_of_review_author, self.no_of_times_shelved





pages_url = Page_Url()
page_url = pages_url.get_pages()
print(page_url)

for url in page_url:
    book_score = Score(url)
    book_score = book_score.get_book_score()
    book_score = reduce(lambda x,y: x+y, book_score)

#for url in pages_url.get_pages():
#    book_score = Score(url)
#    book_score = book_score.get_book_score()
#    book_score = reduce(lambda x,y: x+y, book_score)
print(len(book_score))


for url in page_url:
    book_url = Book_Url(url)
    book_url = book_url.get_book_url()

all_book_url = reduce(lambda x,y: x+y, book_url)
all_book_url = all_book_url[:20]

for url in all_book_url:
    author_obj = Author(url)
    author_obj.get_author()

for url in all_book_url:
    genre_obj = Genres(url)
    genre_obj.get_genres()

new_genres = []
for i in genre_obj.genres:
    new_genres.append((',').join(i))



for url in all_book_url:
    get_url_obj = Author_Url(url)
    get_url_obj.get_author_url()

author_url = get_url_obj.author_url
author_url = reduce(lambda x,y: x+y, author_url)

author_url1 = []
for i in author_url:
    url1 = list(map(lambda x: x.replace('show', 'list'), i.split('/')))
    url2 = ('/').join(url1)
    author_url1.append(url2)

for url in author_url1:
    get_author = Author_Info(url)
    get_author.get_author_info()

author_rate = get_author.author_rate
no_of_author_rate = get_author.no_of_author_rate
no_of_review_author = get_author.no_of_review_author
no_of_times_shelved = get_author.no_of_times_shelved


author_follower = author_obj.author_follower
author = author_obj.author
title = author_obj.title
rate = author_obj.rate
desc = author_obj.desc
book_format = author_obj.book_format
language = author_obj.language
similar_book = author_obj.similar_book
#review = obj2.review
rating_count = author_obj.rating_count
review_count = author_obj.review_count

author = pd.DataFrame(author, columns=['Author'])
author_follower = pd.DataFrame(author_follower, columns=['Author_Followers'])
rate = pd.DataFrame(rate, columns=['Rate'])
desc = pd.DataFrame(desc, columns=['Desc'])
book_format = pd.DataFrame(book_format, columns=['Book_Format'])
language = pd.DataFrame(language, columns=['Language'])
title = pd.DataFrame(title, columns=['Book_Title'])
similar = pd.DataFrame(similar_book, columns=['Books_By_Similar_Author'])
genres = pd.DataFrame(new_genres, columns=['Genres'])
#review = pd.DataFrame(review, columns=['Review'])
review_count = pd.DataFrame(review_count, columns=['No_Of_Review'])
rating_count = pd.DataFrame(rating_count, columns=['No_Of_Rating'])
author_rate = pd.DataFrame(author_rate, columns=['Author_Rate'])
no_of_author_rate = pd.DataFrame(no_of_author_rate, columns=['No_Of_Author_Rate'])
no_of_review_author = pd.DataFrame(no_of_review_author, columns=['No_Of_Review_Author'])
no_of_times_shelved = pd.DataFrame(no_of_times_shelved, columns=['No_Of_Times_Shelved'])
book_score = pd.DataFrame(book_score, columns=['Book_Score'])
#print(no_shelve)


author['Book Title'] = title
author['Author Follower'] = author_follower
author['Rate'] = rate
author['Book_Score'] = book_score
author['Description'] = desc
author['Book Format'] = book_format
author['Language'] = language
author['Genres'] = genres
#author['Review'] = review
author['No_Of_Review'] = review_count
author['No_Of_Rating'] = rating_count
author['Author_Rate'] = author_rate
author['No_Of_Author_Ratings'] = no_of_author_rate
author['No_Of_Review_Author'] = no_of_review_author
author['No_Of_Times_Author_Shelved'] = no_of_times_shelved
author['Books_By_Similar_Author'] = similar

author.to_csv('booklist123.csv')










