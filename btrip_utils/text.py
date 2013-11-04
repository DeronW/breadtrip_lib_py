#coding: utf-8
"""
Breadtrip bases
"""
import re
from hashes.simhash import simhash
from mmseg import seg_txt
from django.utils.encoding import smart_str, smart_unicode

TAG_RE = re.compile(ur"<[^>]*>|\s|&nbsp;")

def text_wrapped_by(start, end, content):
    """get the text wrapped by start、end in content"""
    si = content.find(start)
    if si != -1:
        si += len(start)
        ei = content.find(end, si)
        if ei != -1:
            return content[si:ei]
    return None

# From http://www.xhaus.com/alan/python/httpcomp.html#gzip
# Used with permission.
def compress_string(s):
    import cStringIO, gzip
    zbuf = cStringIO.StringIO()
    zfile = gzip.GzipFile(mode='wb', compresslevel=6, fileobj=zbuf)
    zfile.write(s)
    zfile.close()
    return zbuf.getvalue()

def decompress_string(s):
    """
    Uses zlib
    """
    import zlib
    return zlib.decompress(s, 16+zlib.MAX_WBITS)

def strip_tags(value):
    return TAG_RE.sub("", value)

def get_similarity(s1, s2):
    """
    Get the similarity of two english word
    """
    return simhash(s1).similarity(simhash(s2))

def get_chinese_similarity(s1, s2):
    """
    Get the similarity of two chinese word
    """
    hash1 = simhash([ smart_unicode(x) for x in seg_txt(smart_str(s1)) ])
    hash2 = simhash([ smart_unicode(x) for x in seg_txt(smart_str(s2)) ])
    return hash1.similarity(hash2)

if __name__ == "__main__":
    text = "Hello world!"
    compressed = compress_string(text)
    print compressed
    print decompress_string(compressed)

