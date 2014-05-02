def main_menu():
    print "Welcome to GameChanger"
    file = 'data/NCAA23Mar2014.txt'
    sport = ''
    tournament = ''
    while sport not in ('A', 'a'):
        user = raw_input("What sports would you want to follow? Type A for Men's basketball: " )
        print user
        if user in ('A', 'a'):
           sport = user
           print ( user+', ' +"You are a basketball fan. Great!")
        else:
           print "Whoops! What you just entered is an invalid input.  Could you reenter the right input: A?"
    while tournament not in ('A', 'a'):
        user = raw_input ("What tournament do you want to follow? Type A for 2014 NCAA Men's Tournament:" )
        if user in ('A', 'a'):  
           tournament = user
           print (user+', ' "You are about to explore which games are more exciting!")
        else:
           print "Whoops! What you just entered is an invalid input.  Could you reenter a right input: A?"
    if tournament in ('A', 'a'):
        return file

def school_tweet_rate(school,tweetnumber, time):  #time in number of minutes, this function calculates tweet rate of each school every minute  #time=part of data, taimstamp=specific time   
                                               #timestamp=entered time by a user
    for i in range(0,len(school)): 
         averagetweet=float(tweetnumber[i])/float(2*time)#time in minutes, [i]=position of tweetnumber
    return averagetweet
#print '%.2f'%ave_tweet_rate()

def ave_tweet_rate_total(school,totaltweets,time):  #updating every minute, requires the given time in               
                                                               #minutes for all school
    for i in range(0,len(school)):
         averagetweetT=float(totaltweets[i][position of totaltweets]])/float(2*time)# this across every school  function calculates# average    tweet rate for total 
	return averagetweetT
                                                                                                
def compare_tweet_rate (school_tweet_rate, ave_tweet_rate_total):# works for both whole day vs. a given time
     # for a particular school
    if school_rate > ave_tweet_rate:
         print "Tweet rates for these schools are above average tweet rates are worth watching.”
    else:
         print “The game(s) must be boring since the tweet rates are below average.”
def compare_tweet_rate (array of school_tweet_rate, ave_tweet_rate_total):# for whole school list comparing to toal tweet rate across all schools depending on your preference
    for i in range(0, len(school)):
        if school_rate > ave_tweet_rate:
            print "Tweet rates for these schools are above average tweet rates:" + school name + " is worth watching”
        else:
           Print “Games by these schools aren’t interesting”
def draw_gragph(schoolname_user_specified, school,#oftweets, time):#schoolname_user_specified=user entered, school=part of data
    file = open(’testdata.txt’, ’w’)   
    for i in range(0, len(school)):
        if schoolname_user_specified==school:
                # Write #tweet,time into a file
	        txt = str(time) + ’\t’ + str(#oftweets) + ’ \n’# time and number of tweets from the data
    file.write(txt)  # outside for- loop
            # Close your file
    file.close()
    import numpy as np #graphing starts here
    import pylab as pl
    # Use numpy to load the data contained in the file
    # ’fakedata.txt’ into a 2-D array called data
    data = np.loadtxt("/Users/Sunhwa/Desktop/fakedata.txt")
    # plot the first column as x, and second column as y
	  pl.title("Plot of Number of Tweets vs. Time")
    pl.plot(data[:,0], data[:,1], "ro")
    pl.xlabel("Time")
    pl.ylabel("number of Tweet")
    pl.xlim(0.0, 10.)
    pl.show()
    open(’testdata.txt’, 'w').close() #erase the file,,so you get new data for each school for graphing.






