import requests
from bs4 import BeautifulSoup
import pprint
import textwrap

pubmed_url = "https://pubmed.ncbi.nlm.nih.gov"
saved_search = "/?term=scRNAseq%2C+cancer%2C+leukemia%2C+TALL&filter=simsearch2.ffrft&sort=date&size=100"


res = requests.get(pubmed_url+saved_search)
soup = BeautifulSoup(res.text, "html.parser")
links = soup.select('.docsum-title')

open("results-articles.txt", "w").close()

list_articles = []

for i in range(len(links)):
    title = links[i].get_text(strip=True)
    authors = soup.select(
        '.docsum-citation span.short-authors')[i].get_text(strip=True)
    director = soup.select(
        '.docsum-citation span.full-authors')[i].get_text(strip=True).split(",")[-1].strip()
    article = requests.get(pubmed_url+links[i].get("href", None))
    art_soup = BeautifulSoup(article.text, "html.parser")
    abstract = art_soup.select("#eng-abstract p")[0].get_text(strip=True)
    date = art_soup.select(".cit")[0].get_text(strip=True).split()[0]

    with open("./results-articles.txt", "a", encoding="utf-8") as file:
        file.write(f'Publication date: {date}\n')
        file.write(f'Title           : {title}\n')
        file.write(f'Director        : {director}\n')
        file.write(f'Authors         : {authors}\n')
        file.write(f'Abstract        :\n')
        file.write(f'=================\n')
        file.write(f'{textwrap.fill(abstract, width=100)}\n\n\n')

    list_articles.append({"title": title,
                          "abstract": abstract,
                          "authors": authors,
                          "director": director,
                          "publication-date": date})


pprint.pprint(list_articles[:])


# Project to build:
#####################
# Title
# Abstract
# Ref to the full text as a link
# If possible add an option whether we want to download the article or not

# Do something interactive like from the beginning having inputs to make (for filtering)
# And then for example at the start printing a message like 'get the materials ready and list
# these materials' and then like having the sys.sleep() for maybe 20s before continuying
