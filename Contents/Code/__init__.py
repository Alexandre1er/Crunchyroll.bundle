# -*- coding: utf-8 -*-
import re, string
import dateutil.tz, dateutil.relativedelta, dateutil.parser
import datetime
import uuid
import urllib

dateutilparser = dateutil.parser() # Because i have no idea why i can't call dateutil.parser.parse() directly...

TITLE = 'Crunchyroll'
ART = 'art-default.png'
ICON = 'icon-default.png'
ICON_QUEUE = 'icon-queue.png'
ICON_LIST = 'icon-list.png'
ICON_PREFS = 'icon-prefs.png'
ICON_SEARCH = 'icon-search.png'
ICON_NEXT = 'icon-next.png'

API_URL = "https://api.crunchyroll.com"
# Fake headers don't seem necessary
# API_HEADERS = {'User-Agent':"Mozilla/5.0 (iPhone; iPhone OS 8.3.0; en_US)", 'Accept-Encoding':"gzip, deflate", 'Accept':"*/*", 'Content-Type':"application/x-www-form-urlencoded"}
API_HEADERS = {}
API_VERSION = "2313.8"
API_ACCESS_TOKEN = "QWjz212GspMHH9h"
API_DEVICE_TYPE = "com.crunchyroll.iphone"
MANGA_API_URL = "https://api-manga.crunchyroll.com"
MANGA_API_VERSION = "1.0"

####################################################################################################
def Start():

	Plugin.AddViewGroup('InfoList', viewMode = 'InfoList', mediaType = 'items')
	Plugin.AddViewGroup('List', viewMode = 'List', mediaType = 'items')

	ObjectContainer.title1 = TITLE
	ObjectContainer.art = R(ART)
	ObjectContainer.view_group = 'List'

	DirectoryObject.thumb = R(ICON)
	DirectoryObject.art = R(ART)

	VideoClipObject.thumb = R(ICON)
	VideoClipObject.art = R(ART)

	HTTP.CacheTime = CACHE_1HOUR
	# HTTP.RandomizeUserAgent('Safari')
	# HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0'

####################################################################################################
def login(skip_cached = False):

	current_datetime = datetime.datetime.now(dateutil.tz.tzutc())
	username = Prefs['username']
	password = Prefs['password']

	# Check to see if a session_id doesn't exist or if the current auth token is invalid and if so start a new session and log it in.
	if (skip_cached is True or 'session_id' not in Dict or 'auth_expires' not in Dict or current_datetime > Dict['auth_expires']):

		# Start new session
		Log("Crunchyroll.bundle ----> Starting new session.")
		request = start_session()
		if request['error'] is False:
			Dict['session_id'] = request['data']['session_id']
			Dict['session_expires'] = (current_datetime + dateutil.relativedelta.relativedelta( hours = +4 ))
			Log("Crunchyroll.bundle ----> New session created! Session ID is: "+ str(Dict['session_id']))
		elif request['error'] is True:
			Log("Crunchyroll.bundle ----> Error starting new session. Error message is: "+ str(request['message']))
			return False

		# Login the session we just started.
		if not username or not password:
			Log("Crunchyroll.bundle ----> No Username or Password set")
			return False
		else:
			Log("Crunchyroll.bundle ----> Logging in the new session we just created.")
			options = {'session_id':Dict['session_id'], 'password':password, 'account':username, 'version':API_VERSION}
			request = JSON.ObjectFromURL(API_URL+"/login.0.json", values=options, cacheTime=0, headers=API_HEADERS)
			if request['error'] is False:
				Dict['auth_token'] = request['data']['auth']
				Dict['auth_expires'] = dateutilparser.parse(request['data']['expires'])
				Dict['premium_type'] = 'free' if request['data']['user']['premium'] == '' else request['data']['user']['premium']
				Log("Crunchyroll.bundle ----> Login successful.")
			elif request['error'] is True:
				Log("Crunchyroll.bundle ----> Error logging in new session. Error message was: "+ str(request['message']))
				return False

		# Verify user is premium
		if Dict['premium_type'] in 'anime|drama|manga':
			Log("Crunchyroll.bundle ----> User is a premium "+str(Dict['premium_type'])+" member.")
			Dict.Save()
			return True
		else:
			Log("Crunchyroll.bundle ----> User is not premium. Unable to load plugin.")
			return False

	# Check to see if a valid session and auth token exist and if so reinitialize a new session using the auth token.
	elif ('session_id' in Dict and 'auth_token' in Dict and current_datetime < Dict['auth_expires'] and current_datetime > Dict['session_expires']):

		# Re-start new session
		Log("Crunchyroll.bundle ----> Valid auth token was detected. Restarting session.")
		request = start_session(Dict['auth_token'])
		if request['error'] is False:
			Dict['session_id'] = request['data']['session_id']
			Dict['auth_expires'] = dateutilparser.parse(request['data']['expires'])
			Dict['premium_type'] = 'free' if request['data']['user']['premium'] == '' else request['data']['user']['premium']
			Dict['auth_token'] = request['data']['auth']
			Dict['session_expires'] = (current_datetime + dateutil.relativedelta.relativedelta( hours = +4 )) # 4 hours is a guess. Might be +/- 4.
			Log("Crunchyroll.bundle ----> Session restart successful. New session_id is: "+ str(Dict['session_id']))

			# Verify user is premium
			if Dict['premium_type'] in 'anime|drama|manga':
				Log("Crunchyroll.bundle ----> User is a premium "+str(Dict['premium_type'])+" member.")
				Dict.Save()
				return True
			else:
				Log("Crunchyroll.bundle ----> User is not premium. Unable to load plugin.")
				return False

		elif request['error'] is True:
			# Remove Dict variables so we start a new session next time around.
			del Dict['session_id']
			del Dict['auth_expires']
			del Dict['premium_type']
			del Dict['auth_token']
			del Dict['session_expires']
			Log("Crunchyroll.bundle ----> Error restarting session. Will now delete session data and attempt to start a new one. Error message was: "+ str(request['message']))

			Dict.Save()
			return login(skip_cached)

	# If we got to this point that means a session exists and it's still valid, we don't need to do anything.
	elif ('session_id' in Dict and current_datetime < Dict['session_expires']):
		# Test to make sure the session still works. (Sometimes sessions just stop working. Not sure why.
		options = {'media_types':'anime|drama','fields':'media.name'}
		request = makeAPIRequest('queue', options)
		if request['error'] is False:
			Log("Crunchyroll.bundle ----> A valid session was detected. Using existing session_id of: "+ str(Dict['session_id']))
			# Verify user is premium
			if Dict['premium_type'] in 'anime|drama|manga':
				Log("Crunchyroll.bundle ----> User is a premium "+str(Dict['premium_type'])+" member.")
				return True
			else:
				Log("Crunchyroll.bundle ----> User is not premium. Unable to load plugin.")
				return False
		elif request['error'] is True:
			Log("Crunchyroll.bundle ----> Something is wrong with the session. Will now delete session data and attempt to start a new one.")
			del Dict['session_id']
			del Dict['auth_expires']
			del Dict['premium_type']
			del Dict['auth_token']
			del Dict['session_expires']
			Dict.Save()
			return login(skip_cached)

	# This is here as a catch all in case something gets messed up along the way. Remove Dict variables so we start a new session next time around.
	else:
		del Dict['session_id']
		del Dict['auth_expires']
		del Dict['premium_type']
		del Dict['auth_token']
		del Dict['session_expires']
		Log("Crunchyroll.bundle ----> Something in the login process went wrong. Will now delete session data and attempt to start a new one.")

		Dict.Save()
		return login(skip_cached)

####################################################################################################
def start_session(auth_token = None):
	# Retreive the existing device_id or create a new one
	if not Data.Exists("device_id"):
		device_id = str(uuid.uuid4())
		Data.SaveObject("device_id", device_id)
		Log("Crunchyroll.bundle ----> New device_id created. New device_id is: "+device_id)
	else:
		device_id = Data.LoadObject("device_id")

	# Prepare the options
	options = {'device_id':device_id, 'device_type':API_DEVICE_TYPE, 'access_token':API_ACCESS_TOKEN, 'version':API_VERSION}
	if auth_token is not None:
		options['auth'] = auth_token

	if Prefs['session_in_us'] is True:
		# Use CR Manga API to create a US-based session``
		Log("Crunchyroll.bundle ----> Creating a session in the US")
		del options['version']
		options['api_ver'] = MANGA_API_VERSION
		query_string = urllib.urlencode(options)
		return JSON.ObjectFromURL(MANGA_API_URL+"/cr_start_session?"+query_string, cacheTime=0, headers=API_HEADERS)
	else:
		# Create a normal session using the main API
		Log("Crunchyroll.bundle ----> Creating a session")
		return JSON.ObjectFromURL(API_URL+"/start_session.0.json", values=options, cacheTime=0, headers=API_HEADERS)

####################################################################################################
def ValidatePrefs():
	loginResult = login(skip_cached = True)
	Log("Crunchyroll.bundle ----> Login result: " + str(loginResult))
	if loginResult is False:
		return ObjectContainer(
			header = "Failed to log in",
			message = "Could not log in to Crunchyroll. Please set your login credentials in the Preferences for this channel and try again."
		)

####################################################################################################
@handler('/video/crunchyroll', TITLE, thumb=ICON, art=ART)
def MainMenu():
	loginResult = login()
	Log("Crunchyroll.bundle ----> Login result: " + str(loginResult))

	oc = ObjectContainer(no_cache = True)

	if loginResult is True:
		oc.add(DirectoryObject(key=Callback(Queue, title = "My Queue"), title = "My Queue", thumb = R(ICON_QUEUE)))
		oc.add(DirectoryObject(key=Callback(History, title = "History", offset = 0), title = "History", thumb = R(ICON_QUEUE)))
		if 'anime' in Dict['premium_type']:
			oc.add(DirectoryObject(key=Callback(Channels, title = "Anime", type = "anime"), title = "Anime", thumb = R(ICON_LIST)))
		if 'drama' in Dict['premium_type']:
			oc.add(DirectoryObject(key=Callback(Channels, title = "Drama", type = "drama"), title = "Drama", thumb = R(ICON_LIST)))
		oc.add(InputDirectoryObject(key=Callback(Search), title = "Search", prompt = "Anime series, drama, etc", thumb = R(ICON_SEARCH)))
	else:
		oc.header = "Failed to log in",
		oc.message = "Could not log in to Crunchyroll. Please set your login credentials in the Preferences for this channel and try again."

	return oc

####################################################################################################
@route('/video/crunchyroll/queue')
def Queue(title):
	loginResult = login()
	Log("Crunchyroll.bundle ----> Login result: " + str(loginResult))

	oc = ObjectContainer(title2 = title)
	if Prefs['queue_type'] == 'Episodes':
		fields = "media.episode_number,media.name,media.description,media.media_type,media.series_name,media.available,media.available_time,media.free_available,media.free_available_time,media.duration,media.playhead,media.url,media.mature,media.screenshot_image,image.fwide_url,image.fwidestar_url"
		options = {'media_types':"anime|drama", 'fields':fields}
		request = makeAPIRequest('queue', options)
		if request['error'] is False:
			return list_media_items(request['data'], 'Queue', None, '1', 'queue')
		elif request['error'] is True:
			return ObjectContainer(header = 'Error', message = request['message'])

	elif Prefs['queue_type'] == 'Series':
		fields = "series.name,series.description,series.series_id,series.rating,series.media_count,series.url,series.publisher_name,series.year,series.mature,series.portrait_image,image.large_url,series.landscape_image,image.full_url"
		options = {'media_types':"anime|drama", 'fields':fields}
		request = makeAPIRequest('queue', options)
		if request['error'] is False:
			for series in request['data']:
				series = series['series']
				thumb = '' if (series['portrait_image'] is None or series['portrait_image']['large_url'] is None or 'portrait_image' not in series or 'large_url' not in series['portrait_image']) else series['portrait_image']['large_url'] # Becuase not all series have a thumbnail.
				art = '' if (series['landscape_image'] is None or series['landscape_image']['full_url'] is None or 'landscape_image' not in series or 'full_url' not in series['landscape_image']) else series['landscape_image']['full_url'] # Becuase not all series have art.
				rating = '0' if (series['rating'] == '' or 'rating' not in series) else series['rating'] # Because Crunchyroll seems to like passing series without ratings
				content_rating = 'R' if (series['mature'] is True) else '' # Only set the content_rating if the show is mature.
				if ('media_count' in series and 'series_id' in series and 'name' in series and series['media_count'] > 0): # Because Crunchyroll seems to like passing series without these things
					oc.add(TVShowObject(
						key = Callback(list_collections, series_id = series['series_id'], series_name = series['name'], thumb = thumb, art = art, count = series['media_count']),
						rating_key = series['url'],
						title = series['name'],
						summary = series['description'],
						studio = series['publisher_name'],
						source_title = TITLE,
						thumb = thumb,
						art = art,
						content_rating = content_rating,
						episode_count = int(series['media_count']),
						viewed_episode_count = 0,
						rating = (float(rating) / 10)))

			# Check to see if anything was returned
			if len(oc) == 0:
				return ObjectContainer(header='No Results', message='No results were found')

		elif request['error'] is True:
			return ObjectContainer(header = 'Error', message = request['message'])

	return oc

####################################################################################################
@route('/video/crunchyroll/history')
def History(title, offset):
	loginResult = login()
	Log("Crunchyroll.bundle ----> Login result: " + str(loginResult))

	oc = ObjectContainer(title2 = title)
	fields = "media.episode_number,media.name,media.description,media.media_type,media.series_name,media.available,media.available_time,media.free_available,media.free_available_time,media.duration,media.playhead,media.url,media.mature,media.screenshot_image,image.fwide_url,image.fwidestar_url"
	options = {'media_types':"anime|drama", 'fields':fields, 'limit':'64'}
	request = makeAPIRequest('recently_watched', options)
	if request['error'] is False:
		return list_media_items(request['data'], 'Recently Watched', None, '1', 'history')
	elif request['error'] is True:
		return ObjectContainer(header = 'Error', message = request['message'])

	return oc

####################################################################################################
@route('/video/crunchyroll/channels')
def Channels(title, type):
	oc = ObjectContainer(title2 = title)
	oc.add(DirectoryObject(key=Callback(list_series, title = "Popular", media_type = type, filter = "popular", offset = 0), title = "Popular", thumb = R(ICON_LIST)))
	oc.add(DirectoryObject(key=Callback(list_series, title = "Simulcasts", media_type = type, filter = "simulcast", offset = 0), title = "Simulcasts", thumb = R(ICON_LIST)))
	oc.add(DirectoryObject(key=Callback(list_series, title = "Updated", media_type = type, filter = "updated", offset = 0), title = "Updated", thumb = R(ICON_LIST)))
	oc.add(DirectoryObject(key=Callback(list_series, title = "Alphabetical", media_type = type, filter = "alpha", offset = 0), title = "Alphabetical", thumb = R(ICON_LIST)))
	oc.add(DirectoryObject(key=Callback(list_categories, title = "Genres", media_type = type, filter = "genre"), title = "Genres", thumb = R(ICON_LIST)))
	oc.add(DirectoryObject(key=Callback(list_categories, title = "Seasons", media_type = type, filter = "season"), title = "Seasons", thumb = R(ICON_LIST)))
	return oc

####################################################################################################
@route('/video/crunchyroll/search')
def Search(query):
	loginResult = login()
	Log("Crunchyroll.bundle ----> Login result: " + str(loginResult))

	oc = ObjectContainer(title2 = 'Search')
	fields = "series.name,series.description,series.series_id,series.rating,series.media_count,series.url,series.publisher_name,series.year,series.mature,series.portrait_image,image.large_url,series.landscape_image,image.full_url"
	options = {'media_types':Dict['premium_type'], 'classes':'series', 'fields':fields, 'limit':'64', 'q':query}
	request = makeAPIRequest('search', options)
	if request['error'] is False:
		for series in request['data']:
			thumb = '' if (series['portrait_image'] is None or series['portrait_image']['large_url'] is None or 'portrait_image' not in series or 'large_url' not in series['portrait_image']) else series['portrait_image']['large_url'] # Becuase not all series have a thumbnail.
			art = '' if (series['landscape_image'] is None or series['landscape_image']['full_url'] is None or 'landscape_image' not in series or 'full_url' not in series['landscape_image']) else series['landscape_image']['full_url'] # Becuase not all series have art.
			rating = '0' if (series['rating'] == '' or 'rating' not in series) else series['rating'] # Because Crunchyroll seems to like passing series without ratings
			content_rating = 'R' if (series['mature'] is True) else '' # Only set the content_rating if the show is mature.
			if ('media_count' in series and 'series_id' in series and 'name' in series and series['media_count'] > 0): # Because Crunchyroll seems to like passing series without these things
				oc.add(TVShowObject(
					key = Callback(list_collections, series_id = series['series_id'], series_name = series['name'], thumb = thumb, art = art, count = series['media_count']),
					rating_key = series['url'],
					title = series['name'],
					summary = series['description'],
					studio = series['publisher_name'],
					source_title = TITLE,
					thumb = thumb,
					art = art,
					content_rating = content_rating,
					episode_count = int(series['media_count']),
					viewed_episode_count = 0,
					rating = (float(rating) / 10)))

	elif request['error'] is True:
		return ObjectContainer(header = 'Error', message = request['message'])

	# Check to see if anything was returned
	if len(oc) == 0:
		return ObjectContainer(header='No Results', message='No results were found')

	return oc

####################################################################################################
@route('/video/crunchyroll/series')
def list_series(title, media_type, filter, offset):
	loginResult = login()
	Log("Crunchyroll.bundle ----> Login result: " + str(loginResult))

	oc = ObjectContainer(title2 = title)
	fields = "series.name,series.description,series.series_id,series.rating,series.media_count,series.url,series.publisher_name,series.year,series.mature,series.portrait_image,image.large_url,series.landscape_image,image.full_url"
	options = {'media_type':media_type, 'filter':filter, 'fields':fields, 'limit':'64', 'offset':offset}
	request = makeAPIRequest('list_series', options)
	if request['error'] is False:
		counter = 0
		for series in request['data']:
			thumb = '' if (series['portrait_image'] is None or series['portrait_image']['large_url'] is None or 'portrait_image' not in series or 'large_url' not in series['portrait_image']) else series['portrait_image']['large_url'] # Becuase not all series have a thumbnail.
			art = '' if (series['landscape_image'] is None or series['landscape_image']['full_url'] is None or 'landscape_image' not in series or 'full_url' not in series['landscape_image']) else series['landscape_image']['full_url'] # Becuase not all series have art.
			rating = '0' if (series['rating'] == '' or 'rating' not in series) else series['rating'] # Because Crunchyroll seems to like passing series without ratings
			content_rating = 'R' if (series['mature'] is True) else '' # Only set the content_rating if the show is mature.
			if ('media_count' in series and 'series_id' in series and 'name' in series and series['media_count'] > 0): # Because Crunchyroll seems to like passing series without these things
				oc.add(TVShowObject(
					key = Callback(list_collections, series_id = series['series_id'], series_name = series['name'], thumb = thumb, art = art, count = series['media_count']),
					rating_key = series['url'],
					title = series['name'],
					summary = series['description'],
					studio = series['publisher_name'],
					source_title = TITLE,
					thumb = thumb,
					art = art,
					content_rating = content_rating,
					episode_count = int(series['media_count']),
					viewed_episode_count = 0,
					rating = (float(rating) / 10)))
			counter = counter + 1
		if counter >= 64:
			offset = (int(offset) + counter)
			oc.add(DirectoryObject(key = Callback(list_series, title = title, media_type = media_type, filter = filter, offset = offset), title = "Next...", thumb = R(ICON_NEXT)))

		# Check to see if anything was returned
		if len(oc) == 0:
			return ObjectContainer(header='No Results', message='No results were found')

	elif request['error'] is True:
		return ObjectContainer(header = 'Error', message = request['message'])

	return oc

####################################################################################################
@route('/video/crunchyroll/categories')
def list_categories(title, media_type, filter):
	loginResult = login()
	Log("Crunchyroll.bundle ----> Login result: " + str(loginResult))

	oc = ObjectContainer(title2 = title)
	options = {'media_type':media_type}
	request = makeAPIRequest('categories', options)
	if request['error'] is False:
		if filter == 'genre':
			if 'genre' in request['data']:
				for genre in request['data']['genre']:
					oc.add(DirectoryObject(key=Callback(list_series, title = genre['label'], media_type = media_type, filter = 'tag:'+genre['tag'], offset = 0), title = genre['label'], thumb = R(ICON_LIST)))

		if filter == 'season':
			if 'season' in request['data']:
				for season in request['data']['season']:
					oc.add(DirectoryObject(key=Callback(list_series, title = season['label'], media_type = media_type, filter = 'tag:'+season['tag'], offset = 0), title = season['label'], thumb = R(ICON_LIST)))

		# Check to see if anything was returned
		if len(oc) == 0:
			return ObjectContainer(header='No Results', message='No results were found')

	elif request['error'] is True:
		return ObjectContainer(header = 'Error', message = request['message'])

	return oc

####################################################################################################
@route('/video/crunchyroll/collections')
def list_collections(series_id, series_name, thumb, art, count):
	loginResult = login()
	Log("Crunchyroll.bundle ----> Login result: " + str(loginResult))

	oc = ObjectContainer(title2 = series_name, art = art)
	fields = "collection.collection_id,collection.season,collection.name,collection.description,collection.complete,collection.media_count"
	options = {'series_id':series_id, 'fields':fields, 'sort':'desc', 'limit':count}
	request = makeAPIRequest('list_collections', options)
	if request['error'] is False:
		if len(request['data']) <= 1:
			for collection in request['data']:
				return list_media(collection['collection_id'], series_name, art, count, '1')
		else:
			for collection in request['data']:
				oc.add(SeasonObject(
					key = Callback(list_media, collection_id = collection['collection_id'], collection_name = collection['name'], art = art, count = collection['media_count'], season = collection['season']),
					rating_key = collection['collection_id'],
					index = int(collection['season']),
					title = collection['name'],
					summary = collection['description'],
					source_title = TITLE,
					show = str(series_name),
					thumb = thumb,
					art = art,
					episode_count = int(collection['media_count'])))

				# Check to see if anything was returned
				if len(oc) == 0:
					return ObjectContainer(header='No Results', message='No results were found')

	elif request['error'] is True:
		return ObjectContainer(header = 'Error', message = request['message'])

	return oc
####################################################################################################
@route('/video/crunchyroll/media')
def list_media(collection_id, collection_name, art, count, season):
	loginResult = login()
	Log("Crunchyroll.bundle ----> Login result: " + str(loginResult))

	sort = 'asc'
	fields = "media.episode_number,media.name,media.description,media.media_type,media.series_name,media.available,media.available_time,media.free_available,media.free_available_time,media.duration,media.playhead,media.url,media.mature,media.screenshot_image,image.fwide_url,image.fwidestar_url"
	options = {'collection_id':collection_id, 'fields':fields, 'sort':sort, 'limit':count}
	request = makeAPIRequest('list_media', options)
	if request['error'] is False:
		return list_media_items(request['data'], collection_name, art, season, 'normal')
	elif request['error'] is True:
		return ObjectContainer(header = 'Error', message = request['message'])

####################################################################################################
def list_media_items(request, collection_name, art, season, mode):
	oc = ObjectContainer(title2 = collection_name, art = art)
	for media in request:

		# The following are items to help display Recently Watched and Queue items correctly
		season = media['collection']['season'] if mode == "history" else season
		media = media['media'] if mode == "history" else media  # History media is one level deeper in the json string than normal media items.
		if mode == "queue" and 'most_likely_media' not in media: # Some queue items don't have most_likely_media so we have to skip them.
			continue
		media = media['most_likely_media'] if mode == "queue" else media  # Queue media is one level deeper in the json string than normal media items.

		# Dates, times, and such
		current_datetime = datetime.datetime.now(dateutil.tz.tzutc())
		available_datetime = dateutilparser.parse(media['available_time']).astimezone(dateutil.tz.tzlocal())
		available_date = available_datetime.date()
		available_delta = available_datetime - current_datetime
		available_in = str(available_delta.days)+" days." if available_delta.days > 0 else str(available_delta.seconds/60/60)+" hours."

		# Fix Crunchyroll inconsistencies & add details for upcoming or unreleased episodes
		media['episode_number'] = re.sub('\D', '', media['episode_number'])	# Because CR puts letters into some rare episode numbers.
		media['episode_number'] = '0' if media['episode_number'] == '' else media['episode_number'] # PV episodes have no episode number so we set it to 0.
		name = "Episode "+str(media['episode_number']) if media['name'] == '' else media['name'] # CR doesn't seem to include episode names for all media so we have to make one up.
		if media['available'] is False:
			# Set the name for upcoming episodes
			name = "Coming Soon"
		else:
			# Prepend an improvised progress indicator
			progress = float(media['playhead'] / float(media['duration']))
			progress = 1 if progress > 1 else progress # Cap progress value at 100%, just to be safe
			progress = 0 if progress < 0 else progress # Also make sure it never goes below 0%
			name_prefixes = [
				u'\u2800', # no dots
				u'\u2840', # ⡀
				u'\u28c0', # ⣀
				u'\u28c4', # ⣄
				u'\u28e4', # ⣤
				u'\u28e6', # ⣦
				u'\u28f6', # ⣶
				u'\u28f7', # ⣷
				u'\u28ff'  # ⣿
			]
			name_prefix = name_prefixes[int(round(progress * (len(name_prefixes)-1)))]
			name = name_prefix + " " + name
		thumb = "http://static.ak.crunchyroll.com/i/no_image_beta_full.jpg" if media['screenshot_image'] is None else media['screenshot_image']['fwide_url'] # because not all shows have thumbnails.
		thumb = "http://static.ak.crunchyroll.com/i/coming_soon_beta_fwide.jpg" if media['available'] is False else thumb # Sets the thumbnail to coming soon if the episode isn't available yet.
		description = "This episode will be available in "+str(available_in) if media['available'] is False else media['description'] # Set the description for upcoming episodes.
		duration = int(0) if media['available'] is False else int((float(media['duration']) * 1000))
		url = media['url']+str('&')+Dict['session_id'] # Add the session_id to the URL for the URLService
		content_rating = 'R' if (media['mature'] is True) else '' # Only set the content_rating if the show is mature.

		if media['media_type'] in Dict['premium_type']:
			oc.add(EpisodeObject(
				url = url,
				title = name,
				summary = description,
				originally_available_at = available_date,
				index = int(media['episode_number']),
				show = media['series_name'],
				season = int(season),
				source_title = TITLE,
				thumb = thumb,
				art = art,
				content_rating = content_rating,
				duration = duration
				)
			)

	# Check to see if anything was returned
	if len(oc) == 0:
		return ObjectContainer(header = 'No Results', message = 'No results were found')

	return oc

####################################################################################################
def makeAPIRequest(method, options):
	values = {'session_id':Dict['session_id'], 'version':API_VERSION}
	values.update(options)
	request = JSON.ObjectFromURL(API_URL+"/"+method+".0.json", values=values, cacheTime=0, headers=API_HEADERS, timeout=120)
	return request
