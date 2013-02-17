import sqlite3
import os
import urllib

db = sqlite3.connect("../../espn.db")
team_ids = [x[0] for x in db.execute("SELECT team_id FROM teams").fetchall()]

def schedule_url(team_id, year):
    return "http://espn.go.com/mens-college-basketball/team/schedule/_/id/%s/year/%s/" % (team_id, year)

def get_schedules():
    for year in range(2002, 2014):
        print("Year %s" % year)
        os.system("mkdir %s" % year)
        for team_id in team_ids:
            url = schedule_url(team_id, year)
            print("%s %s..." % (year, team_id))
            f = open("%s/%s.html" % (year, team_id), "wb")
            f.write(urllib.request.urlopen(url).read())
            f.close()


    
    
    
    
