#!/usr/bin/python

import sys
import os
import getopt;
from twitter import *

# Default values
def_counts = 10
user = "bilbo_pingouin"

# input parameters
def usage():
  print "Run: " + sys.argv[0] + " [OPTIONS]"
  print "Where OPTIONS is one the following: "
  print " -h --help"
  print " -c N --counts=N"
  print " -u \"name\" --user=\"name\""

def main(argv):
  try: 
    opts, args = getopt.getopt(argv,"hc:u:",["help","counts=","user="])
  except getopt.GetoptError:
    usage()
    exit(2)
  for opt,arg in opts:
    if opt in ["-h","--help"]:
      usage()
      exit(1)
    elif opt in ["-c","--counts"]:
      print "Retrieving "+str(arg)+" tweets."
      def_counts = arg
    elif opt in ["-u","--user"]:
      print "User: "+arg
      user = arg
    else:
      print "Got the following and I don't know what to do with it:"
      print opt + " " + arg
      usage()
      exit(2)
  

if __name__ == "__main__":
  main(sys.argv[1:])

# Retrieve the credentials for a given account
dir_creds = "~/.twit_cli/"
if not os.path.exists(dir_creds):
  os.makedirs(dir_creds) # I just assume there is not race issue here!

file_creds = dir_creds + user + ".token"
MY_TWITTER_CREDS = os.path.expanduser(file_creds)

if not os.path.exists(MY_TWITTER_CREDS):
  oauth_dance("Twit on CLI", CONSUMER_KEY, CONSUMER_SECRET,
	                  MY_TWITTER_CREDS)

oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)

# OAuth idnetification
t = Twitter(
    auth=OAuth(oauth_token,oauth_secret, 
		  "RkRkt25BDe2IDyM6QhorQ","S5o6nll11syRtwAPufzlNpsrDOAvzGeTzbNOxQ72eM")
    )
#TODO: try to setup a page on my server where those values could be obtained!

# Get status
data = t.statuses.home_timeline(count=def_counts)

# Print lines
for c in range(len(data)):
  print "* "+data[c]['user']['name']+'('+data[c]['user']['screen_name']+')'+" - "+data[c]['text']+" ## "+data[c]['created_at']


