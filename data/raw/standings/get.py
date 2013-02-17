import urllib2 

for year in range(2002, 2014):
    url = "http://espn.go.com/mens-college-basketball/standings/_/year/%s" % year
    filename = "%s.html" % year
    f = open(filename, "w")
    print "fetching %s -> %s ..." % (url, filename)
    f.write(urllib2.urlopen(url).read())
    print "done."
    f.close()
