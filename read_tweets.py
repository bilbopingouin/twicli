#!/usr/bin/python
# https://codereview.stackexchange.com/questions/122449/cli-twitter-client-in-python

# print is a function print() and python3 does not allow mix of tabs and spaces for indentation

import sys
import os
import argparse
import colorama
from twitter import *

# Default values
def_counts = 10
users = []
dir_creds = "./data/oauth/"

# Colorama: init() for windows parsing
colorama.init()
# for n in range(100):
#     print n, '\033['+str(n)+'m'+"whatever"+'\033[0m'
col_bgred   = colorama.Back.RED
col_bgblue  = colorama.Back.BLUE

col_bold    = colorama.Style.BRIGHT

col_fgred   = colorama.Fore.RED
col_fgblue  = colorama.Fore.BLUE
col_fggreen = colorama.Fore.GREEN
col_fggrey  = '\x1b[90m' # this is grey

col_end     = colorama.Style.RESET_ALL



def main(argv):
    global def_counts, users

    user = ''
    
    parser = argparse.ArgumentParser(description='twicli Twitter App')
    parser.add_argument('-c', '--counts', help='Count of tweets to retrieve.',  required=False, action="store", dest="def_counts", type=int)
    parser.add_argument('-u', '--user',   help='Username',	                required=False, action="store", dest="user")
    parser.add_argument('-a', '--all',    help='All Users',	                required=False, action="store_true")
    parser.add_argument('-l', '--list',   help='List available users',          required=False, action="store_true")
    try:
        options = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    if len(user)>0:
        users.append(user)

    if options.all or options.list:
        print(col_fgred + "All users:" + col_end)
        if os.path.exists(os.path.expanduser(dir_creds)):
            token_files = filter(lambda x: x.endswith('.token'), os.listdir(os.path.expanduser(dir_creds)))
            for f in token_files:
                usr = f[:f.index(".token")]
                if options.all:
                    users.append(usr)
                else:
                    print(usr)     
            if options.list:
                exit(0)
        else:
            print(col_bgblue + "No user to be added, path undefined" + col_end)
            exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])

if len(users) < 1:
    users.append("bilbo_pingouin")


for user in users:
    print ("\n" + col_bgred + col_bold + user + col_end)
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
        print("ERROR: The app is not identified!")

    if not os.path.exists(MY_TWITTER_CREDS):
        oauth_dance("Twit on CLI", cust_token, cust_secret,
                    MY_TWITTER_CREDS)

    oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)

    # OAuth idnetification
    t = Twitter(auth=OAuth(oauth_token,oauth_secret,cust_token,cust_secret))

    # Get status
    data = t.statuses.home_timeline(count=def_counts)

    # Print lines
    for c in range(len(data)):
        twit = '* '
        twit += col_fggreen+col_bold+data[c]['user']['name']+col_end
        twit += ' (' + col_fgblue+data[c]['user']['screen_name']+col_end + ')'
        twit += " - " + data[c]['text']
        twit += col_fggrey+" ## "+data[c]['created_at']+col_end
        print(twit)
        #print "* " + col_fggreen+col_bold+data[c]['user']['name']+col_end + ' (' + col_fgblue+data[c]['user']['screen_name']+col_end + ')' + " - " + data[c]['text'] + col_fggrey+" ## "+data[c]['created_at']+col_end


