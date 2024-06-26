import os
import sys
import re

from io import open

# gitlab_base = 'http://gitlab.bitdust.io/devel/bitdust/blob/master/'

md_base = ''
site_url = "https://bitdust.io"
wikipath = '/wiki/'
idserverspath = 'https://identities.bitdust.io/'
blockchainpath = 'https://blockchain.bitdust.io/'

src = sys.argv[1]
dest = sys.argv[2]
basepath = '/'
if len(sys.argv) > 3:
    basepath = sys.argv[3]
if not os.path.isdir(os.path.dirname(dest)):
    print("create", os.path.dirname(dest))
    os.makedirs(os.path.dirname(dest))

menu_html = open('template_menu.htm', 'rt', encoding='utf-8').read()
menu_html = menu_html % {'wikipath': wikipath, }

template = open('template.htm', 'rt', encoding='utf-8').read()
if src.count('api.html'):
    template = open('template_api.htm', 'rt', encoding='utf-8').read()

keywords = open('keywords.txt', 'rt', encoding='utf-8').read().replace('\n', ', ')

sbody = open(src, 'rt', encoding='utf-8').read()
sbody = re.sub('a href="(.+?)\.md"', 'a href="%s\g<1>.html"' % md_base, sbody)
sbody = re.sub('a href="(.+?)\.md\#(.+?)"', 'a href="%s\g<1>.html#\g<2>"' % md_base, sbody)
# sbody = re.sub('a href="(.+?)\.py"', 'a href="%s\g<1>.py"' % gitlab_base, sbody)
sbody = re.sub('a href="../docs/(.+?)\.html"', 'a href="\g<1>.html"', sbody)
sbody = re.sub('a href="docs/(.+?)\.html"', 'a href="\g<1>.html"', sbody)
sbody = re.sub('\>\<img alt="', '><img width=1000 alt="', sbody) 
sbody = re.sub('a href="(\w+?)"', 'a href="\g<1>.html"', sbody)
sbody = re.sub('a href="#(.+?)"', 'a href="%s#\g<1>"' % os.path.basename(src), sbody)
sbody = re.sub('\<p\>\<style', '<style', sbody)
sbody = re.sub('\</style\>\</p\>', '</style>', sbody)
def _clear_id(inp):
    return inp.replace('<em>','_').replace('</em>','_').replace('<','').replace('>','').replace('[','').replace(']','').replace(' ','-').lower()
def _clear_title(inp):
    return inp.replace('<em>','_').replace('</em>','_').replace('<','&lt;').replace('>','&gt;')
sbody = re.sub('\<h(\d)\>(.+?)\<\/h(\d)\>',
               lambda m: '<h%s id="%s">%s</h%s>' % (m.group(1), _clear_id(m.group(2)), _clear_title(m.group(2)), m.group(3)), sbody)
sbody = re.sub('\<li\>\<a href="(.+?)"\>(.+?)\</a\>\</li\>', lambda m: '<li><a href="%s">%s</a></li>' % (m.group(1), _clear_title(m.group(2))), sbody)
# sbody = sbody.replace(
    # '<div class=fbcomments markdown="1">', 
    # '<div class="fb-comments" data-href="%s/%s" data-width="500" data-numposts="5">' % (
        # site_url, os.path.basename(dest)))

api_methods_links = ''
if src.count('api.html'):
    sbody = re.sub('\<h6 id=\"(.+?)\"\>', '<h6 class="api_method_header" id="\g<1>">', sbody)
    sbody = re.sub('\<h4 id=\"(.+?)\(.*?\)\"\>', '<h4 class="api_method" id="\g<1>">', sbody)
    all_api_methods = re.findall('<h4 class="api_method" id="(.*?)">', sbody)
    api_methods_links = '\n'.join(map(lambda m: '<a href="#%s">%s</a><br>' % (m, m, ), all_api_methods))

disqus = """
<div id="disqus_thread"></div>
<script>
    var disqus_config = function () {
        this.page.url = "%s";   
        this.page.identifier = "%s"
    };
    (function() { 
        var d = document, s = d.createElement('script');
        s.src = '//bitdust.disqus.com/embed.js';
        s.setAttribute('data-timestamp', +new Date());
        (d.head || d.body).appendChild(s);
    })();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript" rel="nofollow">comments powered by Disqus.</a></noscript>
""" % ((site_url+'/'+os.path.basename(dest)), src.replace('.html', '').replace('@build\\', ''))
        
sbody = sbody.replace(
    '<div class=fbcomments>', disqus)
    # '<div class="fb-comments" data-href="%s/%s" data-numposts="5" data-width="100%%" data-colorscheme="light">' % (
    #     site_url, os.path.basename(dest))) 
    
try:
    title = re.search('<h1.*?>(.+?)</h1>', sbody).group(1)
except:
    title = src.replace('.html', '').capitalize()
if not title.count('BitDust'):
    title = 'BitDust : ' + title
newbody = template % {
    'title': title,
    'keywords': keywords,
    'body': sbody, 
    'basepath': basepath,
    'wikipath': wikipath,
    'site_url': site_url,
    'idserverspath': idserverspath,
    'blockchainpath': blockchainpath,
    'filepath': os.path.basename(dest),
    'menu_html': menu_html,
    'api_methods_links': api_methods_links,
}
open(dest, 'wt', encoding='utf-8').write(newbody)
