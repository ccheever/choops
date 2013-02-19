import pyquery
import sqlite3
import logging
import re
import urllib
import os

DB = sqlite3.connect("../../espn.db")

teams = [x[0] for x in DB.execute("SELECT team_id FROM teams").fetchall()]

def get_games_for_year(year):
    games = set([])
    for team_id in teams:
        try:
            pq = pyquery.PyQuery(open("../schedules/%s/%s.html" % (year, team_id)).read())
        except IOError:
            # No team schedule for given year
            continue

        print("Querying team %s for year %s ..." % (team_id, year))
        for link in pq("a"):
            try:
                url = link.attrib["href"]

                game_id = int(re.match(".*?gameId=([\d]+)", url).group(1))
                games.add(game_id)
                #print("gameId=%s url=%s" % (game_id, url))
                #game_id = int(re.match(".*?id=([\d]+)", url).group(1))
                continue
            except KeyError:
                pass
            except IndexError:
                pass
            except AttributeError:
                pass
            #print("Nothing for %s" % url)
    return games


def _download(filename, url):
    f = open(filename, "wb")
    f.write(urllib.request.urlopen(url).read())
    f.close()
    return True

def download(games, year):
    for game_id in games:
        for ty in ("recap", "boxscore", "playbyplay"):
            print("Downloading %s for %s in %s" % (ty, game_id, year))
            _download("%s/%s_%s.html" % (year, game_id, ty), "http://espn.go.com/ncb/%s?gameId=%s" % (ty, game_id))

def download_all():
    for year in range(2002, 2014):
        print("YEAR %s" % year)
        games = get_games_for_year(year)
        try:
            os.system("mkdir %s" % year)
        except IOError:
            print("Directory already exists for %s" % year)
        download(games, year)
