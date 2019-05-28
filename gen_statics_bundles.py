#!/usr/bin/env python3
import itertools, os, re, sys
from hashlib import sha1

# This is pretty bad... please rewrite me

def cat(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def sed(filepath, pattern, value):
    with open(filepath, 'r+') as f:
        data = f.read()
        f.seek(0)
        f.write(re.sub(pattern, value, data))
        f.truncate()


print('Generating CSS bundle')
short_hash = sha1(cat('static/main.css') + cat('static/csslibs/uikit-3.1.5.min.css')).hexdigest()[:7]
sed('templates/base.html', '-SHORTSHA1-[a-z0-9]+.css', '-SHORTSHA1-{}.css'.format(short_hash))
css_bundle_filepath = 'static/bundle-SHORTSHA1-{}.css'.format(short_hash)
files_created = not os.path.exists(css_bundle_filepath)
with open(css_bundle_filepath, 'wb') as bundle:
    bundle.write(cat('static/csslibs/uikit-3.1.5.min.css'))
    bundle.write(cat('static/csslibs/solarized-highlight.css'))
    bundle.write(cat('static/csslibs/tipuesearch.css'))
    bundle.write(cat('static/main.css'))

print('Generating JS bundle')
short_hash = sha1(cat('static/jslibs/uikit-3.1.5.min.js') + cat('static/jslibs/jquery-3.4.1.min.js')).hexdigest()[:7]
sed('templates/base.html', '-SHORTSHA1-[a-z0-9]+.js', '-SHORTSHA1-{}.js'.format(short_hash))
for SHARE, MG_FILTER_TAGS in itertools.product(range(2), repeat=2):
    js_bundle_filepath = 'static/bundle-SHARE-{}-MG_FILTER_TAGS-{}-SHORTSHA1-{}.js'.format(
            SHARE, MG_FILTER_TAGS, short_hash)
    files_created |= not os.path.exists(js_bundle_filepath)
    with open(js_bundle_filepath, 'wb') as bundle:
        bundle.write(cat('static/jslibs/html5shiv-3.7.3.min.js'))
        bundle.write(cat('static/jslibs/jquery-3.4.1.min.js'))
        bundle.write(cat('static/jslibs/uikit-3.1.5.min.js'))
        bundle.write(cat('static/jslibs/uikit-icons-3.1.5.min.js'))
        bundle.write(cat('static/jslibs/lazysizes-5.0.0.min.js'))
        if SHARE:
            bundle.write(cat('static/jslibs/jquery.sticky-kit-1.1.2.min.js'))
            bundle.write(cat('static/js/social.js'))
        if MG_FILTER_TAGS:
            bundle.write(cat('static/js/filter-tags.js'))

if files_created:
    print('New bundle files were created', file=sys.stderr)
    sys.exit(1)
