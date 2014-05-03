# -*- coding: utf-8 -*-
timestamp = 1395616822 #1395609292 # 1395616822#1395609952 #1395608362.0 #get the time when user kick in(talk to Brittany)

def school_tweet_rate(timestamp):  # this function calculates tweet rate of a particular game every minute the timeframe from the begining to timestamp; taimstamp represents user -in check-in time  
                                           
                                               
    dataset = []
    with open('data/graphData.txt', 'r') as f:
        for aline in f:
            data = aline.split(" ")
            dataset.append(data)
   # print len(dataset)
 
    for i in range(0,len(dataset)): 
        if float(dataset[i][2]) == timestamp:
            schoolname = dataset[i][0]
            smallesttime = float(dataset[i][2])
            for j in range(0,len(dataset)):
                if dataset[j][0] == schoolname:
                    if float(dataset[j][2]) < smallesttime:
                         smallesttime = float(dataset[j][2])
            schools = dataset[i][0].split('$')
            school_1 = schools[0]
            school_2 = schools[1]

            if timestamp-smallesttime == 0:
                print "The Game between" + school_1 + " and " + school_2 + "is starting now."
                return 0
            else:
                average_rate = float(dataset[i][1])/(abs(timestamp-smallesttime)/2)  #use minute as time format 1st loop down 
                s =  "The Game between " + school_1 + " and " + school_2 + ' has ' + 'average tweet rate '+str("%.2f" % average_rate)
                print s
                return average_rate 
                
school_tweet_rate = school_tweet_rate(timestamp)

def ave_tweet_rate_total(timestamp):  # this function calculates average tweet rate for all games for every minute for the same time frame as above.           
    
    dataset_1=[]
    with open('data/totalPerInterval.txt', 'r') as f:
        for aline in f:
            data=aline.split(" ")
            dataset_1.append(data)
    timestamp=1395608272.0
    
    smallesttime=dataset_1[0][1]
    for i in range(0,len(dataset_1)):
         if smallesttime> dataset_1[i][1]:
             smallesttime=dataset_1[i][1]
    print smallesttime
    smallesttime = float(smallesttime)
    
    tweets=0       
    for j in range(0,len(dataset_1)):
         if (float(dataset_1[j][1]) <= timestamp) and (float(dataset_1[j][1])>=smallesttime):
             tweets = tweets + float(dataset_1[j][0])
            
    print "The number of tweets is " + str(tweets)    
    
    if timestamp-smallesttime == 0:
        print "No game has started. "
        return 0
    else:
        average_rate = float(tweets)/(abs(timestamp-smallesttime)/2)  #use minute as time format 1st loop down 
        s =  "The average tweet rate for all games is " +  str("%.2f" % average_rate)
        print s 
        return average_rate
ave_tweet_rate_total = ave_tweet_rate_total(timestamp)


def compare_tweet_rate (school_tweet_rate, ave_tweet_rate_total):# This function compares average tweet rate for a particular school to that for all games.
     # for a particular school
    if school_tweet_rate > ave_tweet_rate_total:
        print "Tweet rate for this school is above average tweet rate for all school. So this game is worth watching."
    else:
        print "The game must be boring since the tweet rate is below average."

print compare_tweet_rate(school_tweet_rate, ave_tweet_rate_total)



# codes below are for graphing tweet volume for each game to see gamechanging moments.

import numpy as np
import pylab as pl

save_path = raw_input("Enter a save path to be able run the graphing: for instance '/Users/Desktop/yourname'")

infile=open('data/graphData.txt', 'r')
outfile=open(save_path + '/dataset_2.txt', 'w')
#outfile=open('/Users/Sunhwa/Desktop/dataset_2.txt', 'w')
aline=infile.readline()



#user = raw_input("Which school game are you interested in?:  ")

print "Would you like to see game changing moments by checking out tweet volume graph?"
print "There are five games to choose from:  "
print "Enter 1 for WichitaSt$Kentucky; 2 for IowaSt$UNC; 3 for Tennessee$Mercer;"
print "4 for UCLA$StephenFAustin; 5 for Creighton$Baylor"

 
user = int(raw_input("Which school game are you interested in?:  "))
if user==1:
    user="WichitaSt$Kentucky"
    
elif user==2:
      user="IowaSt$UNC"        
elif user==3:
      user="Tennessee$Mercer"
      print user
elif user==4:
      user="UCLA$StephenFAustin"
      print user
elif user==5:
      user="Creighton$Baylor"
    
else:
     
     print "Whoops! That is an invalid value.  Please reenter the valid one."
#user codes end here
       
data = ""
while aline:
	items=aline.split()
	if items[0] == user:
	    data = data + "; " + items[2]+ " " +items[1]
        #outfile.write(dataline + '\n')
   	aline=infile.readline()
	#print(dataline)
# add codes here  for multiple graph
#print data
data = np.array(np.mat(data[1:]))
#print data
pl.plot(data[:,0],data[:,1])
pl.title(user)
#pl.legend("user")
pl.xlabel("Time")
pl.ylabel("Number of Tweet")

pl.show()

open('text59.txt', 'w').close()

