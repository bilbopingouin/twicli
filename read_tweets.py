#!/usr/bin/python

import sys
import os
import argparse
import string
import colorama
from twitter import *

# Default values
def_counts = 10
users = []
search_terms = ''
dir_creds = './data/oauth/'

# Colorama: init() for windows parsing
colorama.init()

# Definitions of some colours
col_bgred   = colorama.Back.RED
col_bgblue  = colorama.Back.BLUE

col_bold    = colorama.Style.BRIGHT

col_fgred   = colorama.Fore.RED
col_fgblue  = colorama.Fore.BLUE
col_fggreen = colorama.Fore.GREEN
col_fggrey  = '\x1b[90m' # this is grey

col_end     = colorama.Style.RESET_ALL


# Argument(s) parsing
def main(argv):
    global def_counts, users, search_terms

    #user = ''
    
    parser = argparse.ArgumentParser(description=col_bold+'twicli Twitter App'+col_end)
    parser.add_argument('-c', '--counts', help='Count of tweets to retrieve.',  required=False, action='store', dest='counts', type=int)
    parser.add_argument('-u', '--user',   help='Username',	                required=False, action='store', dest='user')
    parser.add_argument('-a', '--all',    help='All Users',	                required=False, action='store_true')
    parser.add_argument('-l', '--list',   help='List available users',          required=False, action='store_true')
    parser.add_argument('-s', '--search', help='Search terms on twitter using the default account', required=False, action='store_true')
    parser.add_argument('search_term',    help='Terms searched using [-s]', nargs='+')
    try:
        options = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)
        
    #print(options)

    if options.user:
        users.append(options.user)
        #print(users)
        
    if options.counts:
        def_counts=options.counts

    if options.all or options.list:
        print(col_fgred + 'All users:' + col_end)
        if os.path.exists(os.path.expanduser(dir_creds)):
            token_files = filter(lambda x: x.endswith('.token'), os.listdir(os.path.expanduser(dir_creds)))
            for f in token_files:
                usr = f[:f.index('.token')]
                if options.all:
                    users.append(usr)
                else:
                    print(usr)     
            if options.list:
                exit(0)
        else:
            print(col_bgblue + 'No user to be added, path undefined' + col_end)
            exit(2)
            
    if options.search:
        search_terms = string.join(options.search_term, ' ')
        #print(search_terms)


if __name__ == '__main__':
    main(sys.argv[1:])

if len(users) < 1:
    users.append('bilbo_pingouin')


for user in users:
    print ("\n" + str(def_counts) + " from " + col_bgred + col_bold + user + col_end)
    
    # API Token
    api_token_file = 'data/api_token.dat'
    if os.path.exists(api_token_file):
        cust_token, cust_secret = read_token_file(os.path.expanduser(api_token_file))
    else:
        print(col_bgred+'ERROR: The app is not identified!'+col_end)
        
    # User credentials directory
    if not os.path.exists(dir_creds):
        os.makedirs(dir_creds) # I just assume there is not race issue here!

    # User credentials file
    file_creds = dir_creds + user + '.token'
    MY_TWITTER_CREDS = os.path.expanduser(file_creds)

    # Adding the credentials if they are not already there
    if not os.path.exists(MY_TWITTER_CREDS):
        oauth_dance('Twit on CLI', cust_token, cust_secret,
                    MY_TWITTER_CREDS)

    # Getting tokens for oauth
    oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)

    # OAuth idnetification
    tapi = Twitter(auth=OAuth(oauth_token,oauth_secret,cust_token,cust_secret))

    # Are we searching something?
    if len(search_terms)>0:
        total_data = tapi.search.tweets(q=search_terms,count=def_counts)
        data = total_data['statuses']
        #print(data)
        #for t in data:
        #    print(t)
        #    for t1 in data[t]:
        #        print(t1['user'])
    else:
        # Get status
        data = tapi.statuses.home_timeline(count=def_counts)

    # Print lines
    for t in data:
        twit = '* '
        twit += col_fggreen+col_bold + t['user']['name'] + col_end
        twit += ' (' + col_fgblue + t['user']['screen_name'] + col_end + ')'
        twit += " - " + t['text']
        twit += col_fggrey + " ## " + t['created_at'] + col_end
        print(twit)
