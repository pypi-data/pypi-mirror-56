
class TestVariables:
    default_manga_url = 'https://readmanga.me/van_pis/'
    default_chapter_url = 'https://readmanga.me/van_pis/0/1.5'
    default_image_url = 'https://i.imgur.com/sIz74wK_lq.mp4'
    default_html = '<html><title>Title</title><body>' \
                   '<a href="{ch}">Link text</a>' \
                   '<div class="image" style="background: url({img})"><img src="{img}"<div>' \
                   '<div class="bad-image" style="background: url()"></div>' \
                   '<div class="inner-element-text"><span>text</text></div>' \
                   '<div class="empty-element" title="element-title"></div>' \
                   '<div class="space-only-element"> </div>' \
                   '</body></html>'.format(ch=default_chapter_url, img=default_image_url)
