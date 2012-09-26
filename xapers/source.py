import os
import sys
from urlparse import urlparse

import xapers.sources

def list_sources():
    sources = []
    return ['doi']
    for s in dir(xapers.sources):
        # skip the __init__ file when finding sources
        if '__' in s:
            continue
        sources.append(s)
    return sources


def get_source(source, sid=None):
    try:
        exec('from xapers.sources.' + source + ' import Source')
        return Source(sid)
    except:
        return None

def source_from_url(url):
    source = None
    sid = None

    if os.path.exists(url):
        name = os.path.basename(url)
    
    for ss in list_sources():
        print >>sys.stderr, 'trying', ss, '...', 

        smod = get_source(ss)

        if os.path.exists(url):
            base, ext = os.path.splitext(os.path.basename(url))
            if base == ss:
                smod.sid = '1234'
                smod.file = url
        else:
            o = urlparse(url)
            smod.parse_url(o)

        if smod.sid:
            print >>sys.stderr, 'match!'
            break
        else:
            smod = None
            print >>sys.stderr, ''

    return smod
