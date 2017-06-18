import sys

unicode_str = u'GENEL M\xdcD\xdcRL\xdcK'
print "unicode_str :"
print u'GENEL M\xdcD\xdcRL\xdcK'
print [u'GENEL M\xdcD\xdcRL\xdcK']
print type(u'GENEL M\xdcD\xdcRL\xdcK')
print ""
print "unicode_str.encode('utf-8') :"
print unicode_str.encode('utf-8')
print [unicode_str.encode('utf-8')]
print type(unicode_str.encode('utf-8'))
print ""
print "unicode_str.encode('utf-8').decode(sys.stdout.encoding) :"
print unicode_str.encode('utf-8').decode(sys.stdout.encoding)
print [unicode_str.encode('utf-8').decode(sys.stdout.encoding)]
print type(unicode_str.encode('utf-8').decode(sys.stdout.encoding))
