import time
import datetime


###Use to format timestamps to unix format
def unix_time(timestamp):
  timeFormat = '%m/%d/%Y %H:%M:%S'
  unixTime = time.mktime(datetime.datetime.strptime(timestamp, timeFormat).timetuple())
  return unixTime


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


  ###Currently testing, so timestamp is simply first timestamp of input file
  ###Eventually, timestamp will be current time (since stream would be real-time)

  timestamp = unix_time(tweets[0][:tweets[0].find(',')])

  searchingFor = {}
  current_sched = ''

  tweetRates = {}

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
		'TennesseeVMercer': '03/23/2014 18:01:00',   #ACTUAL TIME IS 18:10:00, just changed for testing
		'UCLAVStephenFAustin': '03/23/2014 19:10:00',
		'CreightonVBaylor': '03/23/2014 19:45:00'
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

  searchTerms = {'WichitaStVKentucky': ['WICH', 'UK'], 		#Shockers, Wichita State, Wildcats, Kentucky
		'IowaStVUNC': ['ISU', 'UNC'],			#Cyclones, Iowa State, Tar Heels, North Carolina
		'TennesseeVMercer': ['TENN', 'MER'],		#Volunteers, Tennessee, Bears, Mercer
		'UCLAVStephenFAustin': ['UCLA', 'SFA'],		#Bruins, Lumberjacks, SF Austin
		'CreightonVBaylor': ['CREI', 'BAY']		#Bluejays, Creighton, Bears, Baylor
		}


  ###check time to ensure matchup is occurring (loop every 30 secs)
  
  while timestamp < unix_time(tweets[len(tweets)-1][:tweets[len(tweets)-1].find(',')])+30:	#i.e., reached end of file
    for key, value in schedule.iteritems():
      if unix_time(value) <= timestamp:
        searchingFor[key] = searchTerms[key]

    ###print sched if any matchups have changed
    new_sched = get_sched(searchingFor, timestamp, matchups, schedule, tv)
    if new_sched != current_sched:
      current_sched = new_sched
      print '\n=============\nCURRENT GAMES\n============='
      for key in searchingFor:
        hoursAgo = timestamp - unix_time(schedule[key])
        print matchups[key] + '\t==\tNetwork: '+ tv[key] + '\t==\tScheduled Start: ' + schedule[key] + ' (' + str(round(hoursAgo/3600, 2)) +' hours ago)'
      #print current_sched
    
    ###if matchup is occurring, check tweet text to see if it contains mention of matchup
    ###sum these instances for each matchup
    for tweet in tweets: 
      if (unix_time(tweet[:tweet.find(',')]) < timestamp):
          continue
      elif (unix_time(tweet[:tweet.find(',')]) >= timestamp) and (unix_time(tweet[:tweet.find(',')]) < (timestamp+30)):
        for key, values in searchingFor.items():
          for value in values: 
            if value in tweet[tweet.find(',')+1:]:
              tweetRates[key] = tweetRates.get(key, 0)+1
              break
      else:
        break
    timestamp = timestamp + 30
    print tweetRates
    print timestamp



  ###find volume, peak activity


  ###if a game ends, print remaining games occurring at present



#Currently, just using a hand created basic text file to test, not the real data set
GameChanger('tournamentTweets.txt')

