import requests
from bs4 import BeautifulSoup
from alive_progress import alive_bar
import time
PROCESS_BULK_LINKS_COUNT = 100


def scrap_ref(page):
    soup = BeautifulSoup(page.text, 'html.parser')
    a_elements = soup.findAll('a', class_="wp-block-button__link has-vivid-green-cyan-background-color has-background")
    real_links = [ref['href'] for ref in a_elements]
    if len(real_links) != 1:
        return None
    return real_links[0]


def process_link(url):
    try:
        page = requests.get(url)
    except TimeoutError | ValueError:
        return None

    if (link := scrap_ref(page)) is None:
        return None
    if not link.startswith("https://click.linksynergy.com/"):
        return None

    link = link.split("url=")[1].split("%")
    return link[0] + "".join([
        bytearray.fromhex(split_part[:2]).decode() + split_part[2:] for split_part in link[1:]
    ])


def get_courses_links(urls):
    urls_count = len(urls)
    urls_bulk = [urls[i:i + PROCESS_BULK_LINKS_COUNT] for i in range(0, urls_count, PROCESS_BULK_LINKS_COUNT)]
    links = []
    errors = []
    for urls in urls_bulk:
        with alive_bar(PROCESS_BULK_LINKS_COUNT, force_tty=True) as bar:
            for url in urls:
                if (link := process_link(url)) is None:
                    errors.append(url)
                    continue
                links.append(link)
                bar()

    return links, errors


def open_links(urls):
    import webbrowser
    for url in urls:
        webbrowser.open_new_tab(url)