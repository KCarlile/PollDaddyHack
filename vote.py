import requests, re, json, time, random
requests.packages.urllib3.disable_warnings()

# Created by Alex Beals
# Last updated: January 29th, 2016

base_url = 'https://polldaddy.com/poll/'
redirect = ""

def vote_once(form, value):
	c = requests.Session()
	init = c.get(base_url + str(form) + "/", headers=redirect, verify=False)
	# Search for the data-vote JSON object
	data = re.search("data-vote=\"(.*?)\"",init.text).group(1).replace('&quot;','"')
	data = json.loads(data)
	# Search for the hidden form value
	pz = re.search("type='hidden' name='pz' value='(.*?)'",init.text).group(1)
	# Build the GET url to vote
	request = "https://polldaddy.com/vote.php?va=" + str(data['at']) + "&pt=0&r=0&p=" + str(form) + "&a=" + str(value) + "%2C&o=&t=" + str(data['t']) + "&token=" + str(data['n']) + "&pz=" + str(pz)
	send = c.get(request, headers=redirect, verify=False)
	return ('revoted' in send.url)

def vote(form, value, times, wait_min = None, wait_max = None):
	global redirect
	redirect = {"Referer": base_url + str(form) + "/", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36", "Upgrade-Insecure-Requests":"1", "Accept-Encoding": "gzip, deflate, sdch", "Accept-Language": "en-US,en;q=0.8"}
	# For each voting attempt
	for i in xrange(1,times+1):
		b = vote_once(form, value)
		# If successful, print that out, else try waiting for 60 seconds (rate limiting)
		if not b:
			print "Voted (time number " + str(i) + " of " + str(times) + " times)!"

			if wait_min and wait_max:
				seconds = random.randint(wait_min, wait_max)
			else:
				seconds = 3

			print "Sleeping " + str(seconds) + " seconds before next vote."

			time.sleep(seconds)
		else:
			print "Locked.  Sleeping for 60 seconds."
			i-=1
			time.sleep(60)

# Initialize these to the specific form and how often you want to vote
poll_id = 0
answer_id = 0
number_of_votes = 0

# To simulate organic voting, set a min and max random wait time (in seconds)
# and voting will occur at intervals within the range. Not providing a value
# will default to 3 seconds.
wait_min = None
wait_max = None

# For an even more organic voting experience and to avoid banning by IP, enable
# TOR and setup a proxy for all voting calls to go through the TOR network
# resulting in varying source IP addresses.

vote(poll_id, answer_id, number_of_votes, wait_min, wait_max)
