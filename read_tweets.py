#!/usr/bin/python

from twitter import *
import json
from pprint import pprint

# see "Authentication" section below for tokens and keys
t = Twitter(
    auth=OAuth("17920223-IJrEHRqVdY9gIna906qC5iKXHD56Lle2fWZIvNjAJ","Bsv6vqtbqlNsZvm6uC28vU3iALWgj8ezoVZ2AbzvfyI0p", 
		  "RkRkt25BDe2IDyM6QhorQ","S5o6nll11syRtwAPufzlNpsrDOAvzGeTzbNOxQ72eM")
    )

# Get your "home" timeline
#data_out = open("data.json","w")
#data = t.statuses.home_timeline()
#data_parsed = json.loads(data)
#pprint(data_parsed)
#data_out.write()
#data.close()

# Get a particular friend's timeline
#t.statuses.friends_timeline(id="billybob")

# Also supported (but totally weird)
#t.statuses.friends_timeline.billybob()

# to pass in GET/POST parameters, such as `count`
data = t.statuses.home_timeline(count=5)
for c in range(5):
  print data[c]['user']['name']+'('+data[c]['user']['screen_name']+')'+" - "+data[c]['text']+" ## "+data[c]['created_at']

# to pass in the GET/POST parameter `id` you need to use `_id`
#t.statuses.oembed(_id=1234567890)

# Update your status
#t.statuses.update(
#          status="Using @sixohsix's sweet Python Twitter Tools.")

# Send a direct message
#t.direct_messages.new(
#          user="billybob",
#	      text="I think yer swell!")

# Get the members of tamtar's list "Things That Are Rad"
#t._("tamtar")._("things-that-are-rad").members()

# Note how the magic `_` method can be used to insert data
# into the middle of a call. You can also use replacement:
#t.user.list.members(user="tamtar", list="things-that-are-rad")

# An *optional* `_timeout` parameter can also be used for API
# calls which take much more time than normal or twitter stops
# responding for some reasone
#t.users.lookup(screen_name=','.join(A_LIST_OF_100_SCREEN_NAMES), _timeout=1)

# Overriding Method: GET/POST
# you should not need to use this method as this library properly
# detects whether GET or POST should be used, Nevertheless
# to force a particular method, use `_method`
#t.statuses.oembed(_id=1234567890, _method='GET')

# Search for the latest tweets about #pycon
#t.search.tweets(q="#pycon")
