import time
import datetime
import curses

def unix_time(timestamp):
  '''
  Use to format timestamps to unix format
  '''
  timeFormat = '%m/%d/%Y %H:%M:%S'
  timestamp = timestamp.replace('"', '')
  unixTime = time.mktime(datetime.datetime.strptime(timestamp, timeFormat).timetuple())
  return unixTime


def est_time(timestamp):
  '''
  Converts unix timestamp back to readable date/time
  In format M/D/Y h/m/s
  '''
  return datetime.datetime.fromtimestamp(timestamp).strftime('%m/%d/%Y %H:%M:%S')


def get_sched(searchingFor, timestamp, matchups, schedule, tv):
  '''
  Use to check if any matchups have changed (in case schedule should be re-printed
  '''
  output = ''
  for key in searchingFor:
    output = output + '\n'+matchups[key] + '\t==\tNetwork: '+ tv[key] + '\t==\tScheduled Start: ' + schedule[key]
  return output.strip()


def actionPrint(matchups, tv, greatest, greatestKey, timestamp, avgRate):
  '''
  Use to print updates in curses interface
  '''
  win = curses.newwin(8,0,8,0) #was 0,0
  win.clear()
  win.border(0)
  win.addstr(1,1,'Activity for time period: ' + str (est_time(timestamp-30)) + ' to ' + str(est_time(timestamp-1))) 
  win.addstr(2,1,'')
  if greatest > avgRate * 2.5 and greatest > 50:
    win.addstr(2,1, "GAME CHANGER! The tweet rate seems to be significantly above average")
  win.addstr(3,1, "The most tweeted about game is:")
  win.addstr(4,1, matchups[greatestKey] +" (" +str(greatest) + " tweets)")
  win.addstr(5,1,"")
  win.addstr(6,1,"Watch it live on "+ tv[greatestKey]+"!")
  win.refresh()

  
def printingSched(timestamp, matchups, tv, schedule, searchingFor):
  '''
  Used to print schedule in curses interface
  '''
  anotherwin = curses.newwin(0,0)
  anotherwin.clear()
  anotherwin.addstr(0,1,'CURRENT GAMES (as of ' + str(est_time(timestamp))+ ')')
  line = 2
  for key in searchingFor:
    hoursAgo = timestamp - unix_time(schedule[key])
    anotherwin.addstr(line,1, matchups[key] + '\t==\tNetwork: '+ tv[key] + '\t==\tScheduled Start: ' + schedule[key] + ' (' + str(round(hoursAgo/3600, 2)) +' hours ago)')
    line = line+1
  anotherwin.refresh()

      
def GameChanger(tournamentTweets):
  '''
  Main function used to run gamechanger program
  '''
  ###Data gathered using Twitter Streaming API
  ###Goal is eventually to stream the tweets directly in real time instead of reading in file
  tweets = open(tournamentTweets)
  tweets = tweets.readlines()
  tweets = [tweet.lower() for tweet in tweets]  #make lower to avoid missing matches due to case differences


  ###Currently testing, so timestamp is simply first timestamp of input file
  ###Eventually, timestamp will be current time (since stream would be real-time)
  ###For timestamps from dataset, have to subtract 14400 to convert to daylight savings EST (natively in GMT)
  timestamp = unix_time(tweets[0][:tweets[0].find(',')])-14400
  searchingFor = {}    #contains search terms matching each game, updated whenever schedule changes
  current_sched = ''

  tweetRates = {}        #accumulates totals for every matchup during the entire period
  tweetsPerInterval = {}  #adds up mentions of each matchup that occurs during each 30 sec period
  numIntervals = 0
  avgRate = 0
  q = -1

  ###Matchups, schedule, tv, and searchTerms currently hard coded as dictionaries
  ###Eventually read in from API or external files
  ###Data gathered from news article & ESPN Teams API

  ###Key = matchup, Value = full matchup name
  matchups = {'WichitaStVKentucky': 'Wichita State v. University of Kentucky', 		
		'IowaStVUNC': 'Iowa State v. University of North Carolina',			
		'TennesseeVMercer': 'Tennessee v. Mercer',		
		'UCLAVStephenFAustin': 'UCLA v. Stephen F. Austin',	
		'CreightonVBaylor': 'Creighton v. Baylor'		
		}

  ###Key = matchup, Value = start time
  ###Times in EST
  schedule = {'WichitaStVKentucky': '03/23/2014 14:45:00',
		'IowaStVUNC': '03/23/2014 17:15:00',
		'TennesseeVMercer': '03/23/2014 18:10:00',
		'UCLAVStephenFAustin': '03/23/2014 19:10:00',
		'CreightonVBaylor': '03/23/2014 19:45:00'
		}
  
  ###Key = matchup, Value = 10 minutes past estimated end time
  ###Times not exact, estimated based on dataset (approximate end time + 10 minutes)
  ###Last three games didn't end in time period, so times not estimated (just set equal to end of day)
  ###Times in EST
  end = {'WichitaStVKentucky': '03/23/2014 17:38:00',
		'IowaStVUNC': '03/23/2014 19:48:00',
		'TennesseeVMercer': '03/23/2014 23:59:00',
		'UCLAVStephenFAustin': '03/23/2014 23:59:00',
		'CreightonVBaylor': '03/23/2014 23:59:00'
		}

  ###Key = matchup, Value = TV channel
  tv = {'WichitaStVKentucky': 'CBS',
		'IowaStVUNC': 'CBS',
		'TennesseeVMercer': 'TNT',
		'UCLAVStephenFAustin': 'TBS',
		'CreightonVBaylor': 'truTV'
		}

  ###Key = matchup, Values = team abbreviations, name, nickname
  searchTerms = {'WichitaStVKentucky': ['WICH', 'UK', 'Shockers', 'Wichita St', 'Wildcats', 'Kentucky'],
		'IowaStVUNC': ['ISU', 'UNC', 'Cyclones', 'Iowa St', 'Tar Heels', 'North Carolina'],
		'TennesseeVMercer': ['TENN', 'MER', 'Volunteers', 'Tennessee', 'Bears', 'Mercer'],
		'UCLAVStephenFAustin': ['UCLA', 'SFA', 'Bruins', 'Lumberjacks', 'SF Austin'],
		'CreightonVBaylor': ['CREI', 'BAY', 'Bluejays', 'Creighton', 'Bears', 'Baylor']
		}

  screen = curses.initscr()
  curses.noecho()
  screen.keypad(1)

  ###check time to ensure matchup is occurring (loop every 30 secs)
  while timestamp < unix_time(tweets[len(tweets)-1][:tweets[len(tweets)-1].find(',')])-14400:	#i.e., reached end of file
    searchingFor = search_terms(searchingFor, timestamp, searchTerms, schedule, end)
    new_sched = get_sched(searchingFor, timestamp, matchups, schedule, tv)
    if new_sched != current_sched:
      current_sched = new_sched
      printingSched(timestamp, matchups, tv, schedule, searchingFor)
    tweetsPerInterval, tweetRates, tweets = find_current_totals(tweets, tweetRates, searchingFor, timestamp)
    
    ###Use to calculate moving average for comparison of rate over time
    totalInterval = 0
    for value in tweetsPerInterval.values():
      totalInterval = totalInterval + value
    avgRate = float(((numIntervals*avgRate)+totalInterval)/(numIntervals+1)) #Cumulative moving average, formula from http://en.wikipedia.org/wiki/Moving_average
    numIntervals = numIntervals + 1
    
    time.sleep(30)
    timestamp = timestamp + 30
    greatest = 0
    for value in tweetsPerInterval.values():
      if value > greatest:
        greatest = value
    if greatest > 0:
      greatestKey = tweetsPerInterval.keys()[tweetsPerInterval.values().index(greatest)]
      actionPrint(matchups, tv, greatest, greatestKey, timestamp, avgRate)
      
    
    tweetsPerInterval.clear()


def search_terms(searchingFor, timestamp, searchTerms, schedule, end):
  '''
  Used to find current search terms
  '''
  searchingFor = searchingFor
  for key, value in schedule.iteritems():
    if unix_time(value) <= timestamp:
      searchingFor[key] = searchTerms[key]
    #print searchingFor
  for key, value in end.iteritems():
    if key in searchingFor:
      if unix_time(value) <= timestamp:
        del searchingFor[key]
  return searchingFor


def find_current_totals(tweets, tweetRates, searchingFor, timestamp):
  '''
  calculate totals based on presence of one of the search strings
  if any of the matchup strings are found, that key is incremented
  if a tweet mentions more than one matchup, both keys are incremented
  '''
  tweetsPerInterval = {}
  tweetRates = tweetRates
  for tweet in tweets: 
    if (unix_time(tweet[:tweet.find(',')])-14400 < timestamp):
        continue
    elif (unix_time(tweet[:tweet.find(',')])-14400 >= timestamp) and (unix_time(tweet[:tweet.find(',')])-14400 < (timestamp+30)):
      for key, values in searchingFor.items():
        for value in values: 
          if value.lower() in tweet[tweet.find(',')+1:]:
            tweetRates[key] = tweetRates.get(key, 0)+1
            tweetsPerInterval[key] = tweetsPerInterval.get(key, 0)+1
            break
      tweets.remove(tweet)
    else:
      break
  return (tweetsPerInterval, tweetRates, tweets)

#Input is a data set of tweets containing 'marchmadness' or 'ncaa' from evening of March 23
#timestamps are in GMT
GameChanger('data/NCAA23Mar2014Tweets.txt')

