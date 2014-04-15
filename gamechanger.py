import time
import datetime


###Use to format timestamps to unix format
def unix_time(timestamp):
  timeFormat = '%m/%d/%Y %H:%M:%S'
  timestamp = timestamp.replace('"', '')
  unixTime = time.mktime(datetime.datetime.strptime(timestamp, timeFormat).timetuple())
  return unixTime

###Converts unix timestamp back to readable date/time
###In format M/D/Y h/m/s
def est_time(timestamp):
  return datetime.datetime.fromtimestamp(timestamp).strftime('%m/%d/%Y %H:%M:%S')

###Use to check if any matchups have changed (in case schedule should be re-printed
def get_sched(searchingFor, timestamp, matchups, schedule, tv):
  output = ''
  for key in searchingFor:
    output = output + '\n'+matchups[key] + '\t==\tNetwork: '+ tv[key] + '\t==\tScheduled Start: ' + schedule[key]
  return output.strip()

def GameChanger(tournamentTweets):

  ###Data gathered using Twitter Streaming API
  ###Goal is eventually to stream the tweets directly in real time instead of reading in file

  tweets = open(tournamentTweets)
  tweets = tweets.readlines()
  tweets = [tweet.lower() for tweet in tweets]


  ###Currently testing, so timestamp is simply first timestamp of input file
  ###Eventually, timestamp will be current time (since stream would be real-time)

  timestamp = unix_time(tweets[0][:tweets[0].find(',')])-14400
  print timestamp
  searchingFor = {}
  current_sched = ''

  tweetRates = {}
  tweetsPerInterval = {}

  ###Matchups, schedule, tv, and searchTerms currently hard coded as dictionaries
  ###Eventually read in from API or external files
  ###Data gathered from news article & ESPN Teams API

  matchups = {'WichitaStVKentucky': 'Wichita State v. University of Kentucky', 		
		'IowaStVUNC': 'Iowa State v. University of North Carolina',			
		'TennesseeVMercer': 'Tennessee v. Mercer',		
		'UCLAVStephenFAustin': 'UCLA v. Stephen F. Austin',	
		'CreightonVBaylor': 'Creighton v. Baylor'		
		}

  ###Key = matchup, Value = start time

  schedule = {'WichitaStVKentucky': '03/23/2014 14:45:00',
		'IowaStVUNC': '03/23/2014 17:15:00',
		'TennesseeVMercer': '03/23/2014 18:10:00',   #ACTUAL TIME IS 18:10:00
		'UCLAVStephenFAustin': '03/23/2014 19:10:00',
		'CreightonVBaylor': '03/23/2014 19:45:00'
		}
  
  #times not exact, estimated based on dataset
  #last three games didn't end in time period, so times not estimated
  
  end = {'WichitaStVKentucky': '03/23/2014 17:28:44',
		'IowaStVUNC': '03/23/2014 19:38:00',
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

  ###Key = matchup, Values = team abbreviations
  ###Later, use abbreviations, name, and nickname as values

  searchTerms = {'WichitaStVKentucky': ['WICH', 'UK', 'Shockers', 'Wichita St', 'Wildcats', 'Kentucky'], 		#, 'Shockers', 'Wichita State', 'Wildcats', 'Kentucky'
		'IowaStVUNC': ['ISU', 'UNC', 'Cyclones', 'Iowa St', 'Tar Heels', 'North Carolina'],			#, 'Cyclones', 'Iowa State', 'Tar Heels', 'North Carolina'
		'TennesseeVMercer': ['TENN', 'MER', 'Volunteers', 'Tennessee', 'Bears', 'Mercer'],			#, 'Volunteers', 'Tennessee', 'Bears', 'Mercer'
		'UCLAVStephenFAustin': ['UCLA', 'SFA', 'Bruins', 'Lumberjacks', 'SF Austin'],				#, 'Bruins', 'Lumberjacks', 'SF Austin'
		'CreightonVBaylor': ['CREI', 'BAY', 'Bluejays', 'Creighton', 'Bears', 'Baylor']				#, 'Bluejays', 'Creighton', 'Bears', 'Baylor'
		}


  ###check time to ensure matchup is occurring (loop every 30 secs)
  
  while timestamp < unix_time(tweets[len(tweets)-1][:tweets[len(tweets)-1].find(',')])-14400:	#i.e., reached end of file #was +30
    for key, value in schedule.iteritems():
      if unix_time(value) <= timestamp:
        searchingFor[key] = searchTerms[key]
    #print searchingFor
    for key, value in end.iteritems():
      if key in searchingFor:
        if unix_time(value) <= timestamp:
          del searchingFor[key]
    
        

    ###print sched if any matchups have changed
    new_sched = get_sched(searchingFor, timestamp, matchups, schedule, tv)
    if new_sched != current_sched:
      current_sched = new_sched
      print '\033[1m\n==========================================\nCURRENT GAMES (as of ' + str(est_time(timestamp))+ ')\n=========================================='
      for key in searchingFor:
        hoursAgo = timestamp - unix_time(schedule[key])
        print matchups[key] + '\t==\tNetwork: '+ tv[key] + '\t==\tScheduled Start: ' + schedule[key] + ' (' + str(round(hoursAgo/3600, 2)) +' hours ago)'
      print '==========================\n\033[0m'
      #print current_sched
    #print '\nTotal activity up to time: ' + str(est_time(timestamp))
    

    ###if matchup is occurring, check tweet text to see if it contains mention of matchup
    ###sum these instances for each matchup
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
        tweets.remove(tweet) #NOT SURE? trying to make more efficient?
        #print len(tweets)
      else:
        #print str(tweetsPerInterval) + ": THIS IS PER INTERVAL"
        #tweetsPerInterval.clear()
        break
    timestamp = timestamp + 30
    ##print tweetRates
    ##print tweetsPerInterval
    greatest = 0
    for value in tweetsPerInterval.values():
      if value > greatest:
        greatest = value
    if greatest > 0:
      print '\nActivity for time period: ' + str (est_time(timestamp-30)) + ' to ' + str(est_time(timestamp-1))
      greatestKey = tweetsPerInterval.keys()[tweetsPerInterval.values().index(greatest)]
      print "-----------------------------------------------------------\nThe most tweeted about game is: " + matchups[greatestKey] +" (" +str(greatest) + " tweets)\nWatch it live on "+ tv[greatestKey]+"!\n-----------------------------------------------------------"
    tweetsPerInterval.clear()



  ###find volume, peak activity


  ###if a game ends, print remaining games occurring at present



#Currently, just using a hand created basic text file to test, not the real data set
GameChanger('data/NCAA23Mar2014Tweets.txt')
