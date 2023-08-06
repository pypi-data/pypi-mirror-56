# Crawler providers system

[![Build status](https://travis-ci.com/manga-py/providers.svg?branch=master "Last build status")](https://travis-ci.com/manga-py/providers)


### What is it?
Manga crawler plugin system (see [manga-py/manga_py](https://github.com/manga-py/manga-py/tree/0f9f5ba5abd97e98b6589c479fa43018616660ef/manga_py/providers))


#### Usage example

```python
from sys import stderr

from crawler_providers import get_providers
from crawler_providers.exceptions import *
from crawler_providers.types import *

url = 'http://best-site/manga/awesome'

try:
    providers = get_providers(url)  # type: list
except ProviderNotFoundError as e:
    print('Provider not found', file=stderr)
    exit(1)
print('Providers count: {}'.format(len(providers)))

for p in providers:
    provider = p(url)  # OR p.new(url) OR p(url, quiet=True) for "silent mode" See documentation: https://manga-py.com/providers/ or https://manga-py.github.com/providers/

    # overload default chapter name:
    Chapter.name_format = '%s/{vol:>03}_ch_{ch:>03}' % (provider.__class__.__name__,)

    try:
        chapters = provider.get_chapters()
    except ChaptersNotFoundException as e:
        print('Chapters not found')
        continue

    for chapter in chapters:
        print('chapter: {}'.format(chapter))

        try:
            files = provider.get_chapter_files(chapter)
        except ImagesNotFoundException as e:
            # e.chapter == chapter (for async methods)
            print('Images not found for chapter: {}'.format(e.chapter))
            continue

    print('Files count: {}'.format(len(files)))

``` 

