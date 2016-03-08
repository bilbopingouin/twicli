#!/usr/bin/python

import sys
import os
import getopt
from twitter import *

# Default values
def_counts = 10
users = []
dir_creds = "./data/oauth/"

# input parameters
def usage():
  print "Run: " + sys.argv[0] + " [OPTIONS]"
  print "Where OPTIONS is one the following: "
  print " -h --help"
  print " -c N --counts=N"
  print " -u \"name\" --user=\"name\""
  print " -a --all"
  print " -l --list"

def main(argv):
  global def_counts, users
  try: 
    opts, args = getopt.getopt(argv,"hc:u:al",["help","counts=","user=","all","list"])
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
      users.append(arg)
    elif opt in ["-a","--all"]:
      print "all users"
      if os.path.exists(os.path.expanduser(dir_creds)):
	      token_files = filter(lambda x: x.endswith('.token'), os.listdir(os.path.expanduser(dir_creds)))
	      for file in token_files:
	        usr = file[:file.index(".token")]
	        users.append(usr)
      else:
	      print "No user to be added, path undefined"
	      exit(2)
    elif opt in ["-l","--list"]:
      if os.path.exists(os.path.expanduser(dir_creds)):
	      token_files = filter(lambda x: x.endswith('.token'), os.listdir(os.path.expanduser(dir_creds)))
	      for file in token_files:
	        usr = file[:file.index(".token")]
	        print usr
      else:
	      print "No user found, path undefined"
	      exit(2)
      exit(1)
    else:
      print "Got the following and I don't know what to do with it:"
      print opt + " " + arg
      usage()
      exit(2)
  

if __name__ == "__main__":
  main(sys.argv[1:])

if len(users) < 1:
  users.append("bilbo_pingouin")
  
# for n in range(100):
#     print n, '\033['+str(n)+'m'+"whatever"+'\033[0m'
col_bgred   = '\033[41m'
col_bold    = '\033[1m'
col_fgblue  = '\033[34m'
col_fggreen = '\033[32m'
col_fggrey  = '\033[90m'
col_end     = '\033[0m'

for user in users:
  print "\n" + col_bgred + col_bold + user + col_end
  # Retrieve the credentials for a given account
  if not os.path.exists(dir_creds):
    os.makedirs(dir_creds) # I just assume there is not race issue here!

  file_creds = dir_creds + user + ".token"
  MY_TWITTER_CREDS = os.path.expanduser(file_creds)

  #TODO: try to setup a page on my server where those values could be obtained!
  api_token_file = "data/api_token.dat"
  if os.path.exists(api_token_file):
    cust_token, cust_secret = read_token_file(os.path.expanduser(api_token_file))
  else:
    print "ERROR: The app is not identified!"

  if not os.path.exists(MY_TWITTER_CREDS):
    oauth_dance("Twit on CLI",cust_token,cust_secret,
			    MY_TWITTER_CREDS)

  oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)

  # OAuth idnetification
  t = Twitter(auth=OAuth(oauth_token,oauth_secret,cust_token,cust_secret))

  # Get status
  data = t.statuses.home_timeline(count=def_counts)

  # Print lines
  for c in range(len(data)):
    #print "* "+data[c]['user']['name']+'('+data[c]['user']['screen_name']+')'+" - "+data[c]['text']+" ## "+data[c]['created_at']
    print "* " + col_fggreen+col_bold+data[c]['user']['name']+col_end + ' (' + col_fgblue+data[c]['user']['screen_name']+col_end + ')' + " - " + data[c]['text'] + col_fggrey+" ## "+data[c]['created_at']+col_end


