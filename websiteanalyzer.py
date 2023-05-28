import requests
from bs4 import BeautifulSoup
from collections import Counter
import re


def get_web_page(url):
    try:
        response = requests.get(url)
        return response.content
    except requests.exceptions.RequestException:
        return None


def extract_meta_tags(soup):
    meta_tags = soup.find_all('meta')
    meta_data = {}
    for tag in meta_tags:
        if tag.get('name'):
            meta_data[tag['name']] = tag.get('content')
        elif tag.get('property'):
            meta_data[tag['property']] = tag.get('content')
    return meta_data


def extract_headings(soup):
    headings = soup.find_all(re.compile('^h[1-6]$'))
    return [heading.text.strip() for heading in headings]


def extract_links(soup):
    links = soup.find_all('a')
    return [link.get('href') for link in links if link.get('href')]


def extract_word_frequency(text):
    words = re.findall(r'\b\w+\b', text)
    word_counts = Counter(words)
    return word_counts


def summarize_web_page(url):
    page_content = get_web_page(url)
    if not page_content:
        print('Failed to retrieve the web page.')
        return

    soup = BeautifulSoup(page_content, 'html.parser')
    meta_tags = extract_meta_tags(soup)
    headings = extract_headings(soup)
    links = extract_links(soup)
    text = soup.get_text()
    word_frequency = extract_word_frequency(text)

    print('Meta Tags:')
    for name, content in meta_tags.items():
        print(f'{name}: {content}')

    print('\nHeadings:')
    for heading in headings:
        print(heading)

    print('\nLinks:')
    for link in links:
        print(link)

    print('\nWord Frequency:')
    for word, count in word_frequency.most_common(10):
        print(f'{word}: {count}')


# Example usage:
url = 'https://3dprintingindustry.com/3d-printing-basics-free-beginners-guide'  # Replace with the desired URL
summarize_web_page(url)
