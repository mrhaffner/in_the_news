import pathlib
import pytest
from bs4 import BeautifulSoup
from scripts.parser import Article

with open(pathlib.Path(__file__).parent.joinpath('data/2022/05/03/18/breitbart.xml')) as f:
    breitbart_soup = BeautifulSoup(f, 'xml')

with open(pathlib.Path(__file__).parent.joinpath('data/2022/05/03/18/cbc.xml')) as f:
    cbc_soup = BeautifulSoup(f, 'xml')

with open(pathlib.Path(__file__).parent.joinpath('data/2022/05/03/18/cnn.xml')) as f:
    cnn_soup = BeautifulSoup(f, 'xml')

with open(pathlib.Path(__file__).parent.joinpath('data/2022/05/03/18/fox.xml')) as f:
    fox_soup = BeautifulSoup(f, 'xml')

with open(pathlib.Path(__file__).parent.joinpath('data/2022/05/03/18/freebe.xml')) as f:
    freebe_soup = BeautifulSoup(f, 'xml')

with open(pathlib.Path(__file__).parent.joinpath('data/2022/05/03/18/guardian.xml')) as f:
    guardian_soup = BeautifulSoup(f, 'xml')

with open(pathlib.Path(__file__).parent.joinpath('data/2022/05/03/18/huffpo.xml')) as f:
    huffpo_soup = BeautifulSoup(f, 'xml')

with open(pathlib.Path(__file__).parent.joinpath('data/2022/05/03/18/npr.xml')) as f:
    npr_soup = BeautifulSoup(f, 'xml')

with open(pathlib.Path(__file__).parent.joinpath('data/2022/05/03/18/pundit.xml')) as f:
    pundit_soup = BeautifulSoup(f, 'xml')

class TestArticle:
    breitbart_article = Article(breitbart_soup.find('item'))
    cbc_article = Article(cbc_soup.find_all('item')[1])
    cnn_article = Article(cnn_soup.find('item'))
    fox_article = Article(fox_soup.find('item'))
    freebe_article = Article(freebe_soup.find('item'))
    guardian_article = Article(guardian_soup.find('item'))
    huffpo_article = Article(huffpo_soup.find('item'))
    npr_article = Article(npr_soup.find('item'))
    pundit_article = Article(pundit_soup.find('item'))
 

class TestAuthor(TestArticle):
    def test_breitbart(self):
        assert self.breitbart_article.author == 'Charlie Spiering'

    def test_cbc(self):
        assert self.cbc_article.author == 'Haley Ryan'

    def test_cnn(self):
        assert self.cnn_article.author == ''

    def test_fox(self):
        assert self.fox_article.author == 'Gabriel Hays'

    def test_freebe(self):
        assert self.freebe_article.author == 'Adam Kredo'

    def test_guardian(self):
        assert self.guardian_article.author == 'Richard Luscombe (now) and Alexandra Topping (earlier)'

    def test_huffpo(self):
        assert self.huffpo_article.author == ''

    def test_npr(self):
        assert self.npr_article.author == 'Joe Hernandez'
    
    def test_pundit(self):
        assert self.pundit_article.author == 'Cristina Laila'