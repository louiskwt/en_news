from django.core.management.base import BaseCommand

import requests
from bs4 import BeautifulSoup, Comment
import json
import re

from scraping.models import Headline


class Command(BaseCommand):
    help = 'collect news'

    # Logic of the scaping command
    def handle(self, *args, **options):

        # open site
        html = requests.get('https://www.scmp.com/hk')

        # result
        soup = BeautifulSoup(html.text, 'html.parser')

        # headline
        title = soup.find(
            class_='article-title__article-link article-hover-link')

        title_text = " ".join(title.find_all(
            text=lambda t: not isinstance(t, Comment)))

        title_length = len(title_text)

        # Clean up title using regex
        x = re.search('[|]', title_text)

        if x:
            title_text = title_text[x.start() + 1:title_length]

        # find summary
        summary_lines = soup.find_all(
            class_='article-level-five__summary--li content--li', limit=2)

        summary = []

        for line in summary_lines:
            summary.append(line.string)

        # save in db
        try:
            Headline.objects.create(
                title=title_text,
                summary_one=summary[0],
                summary_two=summary[1]
            )
            print('%s added' % (title_text))
        except:
            print('Something went wrong')

        self.stdout.write('Job Complete')
