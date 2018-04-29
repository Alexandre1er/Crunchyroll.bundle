About
=====
This plugin provides access to the Anime and Drama video content available at Crunchyroll.com. This plugin requires the user to have a **premium** crunchyroll.com membership. You can sign up for a free 14-day trial by [clicking here](https://www.crunchyroll.com/freetrial). Free membership accounts will not work.

While this plugin is considered stable, there will always be bugs. Please submit bugs via the [Github issue tracker](https://github.com/rimas-kudelis/Crunchyroll.bundle/issues) or in the [official thread on the Plex forums.](https://forums.plex.tv/index.php/topic/73626-rel-crunchyroll-plugin/) I would love to hear feedback and/or suggestions.

The original author of this plugin is [@MattRK](https://github.com/rimas-kudelis/Crunchyroll.bundle), but at some point he ceased development and expressed his disinterest in continuing it (his End of Life notice is quoted below). Since there were certain things in Matt's last release that were bugging me quite a lot, I decided to roll up my sleeves and fix them myself.

End of Life
====
This plugin is no longer maintained. As far as i know, it's still fully functional. However, there's no guarantee that it will continue to work. I highly recommend using the official Crunchyroll apps. They all stream in HD now and are actually very good. The Windows 10 app from the Windows Store works great as do the Android & ios mobile apps. I personally use the mobile app with a Google Chromecast. It's easy, cheap, and works every time. If you don't like the official apps, you can also check out [Crunchyroll Kodi/XBMC plugin.](https://github.com/Yoshiofthewire/CrunchyXBMC)

Requirements
============
This plugin **requires** a **premium** Crunchyroll.com account. You can sign up for free trial by [clicking here](https://www.crunchyroll.com/freetrial). When you get the plugin installed you will need to enter your username and password into the preferences section before you will be able to use it.

* **Plex Media Server:**
	* Version 0.9.12.3 or later (http://www.plexapp.com/getplex/)
	* Windows, Mac, Linux or NAS Appliance
* **Plex Clients:**
	* Plex Home Theater
	* Roku
	* AppleTV
	* Windows 8
	* iOS, Android, & Windows Phone
	* Plex Web

Installation
============
1. Download the latest version of the plugin from [here](https://github.com/rimas-kudelis/Crunchyroll.bundle/archive/v2.3.1.zip).

2. Unzip the content into the PMS plugins directory under your user account.
	* Windows 7, Vista, or Server 2008: C:\Users\[Your Username]\AppData\Local\Plex Media Server\Plug-ins
	* Windows XP, Server 2003, or Home Server: C:\Documents and Settings\[Your Username]\Local Settings\Application Data\Plex Media Server\Plug-ins
	* Mac/Linux: ~/Library/Application Support/Plex Media Server/Plug-ins
	* FreeNAS: /var/db/plexdata/Plex Media Server/Plug-ins

3. Rename the unzipped folder from "Crunchyroll.bundle-vx.x.x" to "Crunchyroll.bundle"

4. Restart PMS


Known Issues
============
* Watching an episode using this app does not mark it as "watched" in Plex or in the Crunchyroll queue. This is a limitation of the Plex Media Server API and there are no viable workarounds available. Hopefully Plex will update the API at some point so I can resolve this issue.


Frequently Asked Questions
==========================
**Q: I selected 1080P or 720P but the video is played in a lower resolution**

A: Not all content on Crunchyroll has HD quality videos available. This plugin will try to play content at the resolution you select. However, if a particular resolution is not available, it will play the next highest resolution available. This may also occur shortly after Crunchyroll releases a new video. Sometimes it takes Crunchyroll longer than expected to encode the HD quality videos. During this period of time the plugin only has access to the lower quality streams that have already been encoded. If this is the case, check back later and the HD quality video should be available.

**Q: How do I hide mature content?**

A: You can choose what type of content to show by changing the Mature Content Filter setting on the Crunchyroll website. Go to your [Account Settings](https://www.crunchyroll.com/acct/) and click on Video Preferences on the left side. Select the desired option from the Mature Content Filter drop down box. You should restart Plex Media Server after you've made this change.

**Q: I get a "Cannot load M3U8: crossdomain access denied" error when trying to use this plugin on Plex Web.**

A: Try un-checking the "Direct Play" box in the Plex Web settings. (Settings > Web > Player > Show Advanced > un-check Direct Play checkbox)

**Q: How do I change the subtitle language?**

A: You can configure this on the Crunchyroll website. Go to your [Account Settings](https://www.crunchyroll.com/acct/) and click on Video Preferences on the left side. Then select the desired language from the "Default Language" drop down box. This will cause all titles, descriptions, and subtitles to be displayed in that language. You should restart Plex Media Server after you've made this change.


Changes
=======
v2.3.0
* Always order episodes within a season from first to last
* Prepend an improvised progress indicator to episode names. This way, at least the videos marked as watched by other means will be indicated
* Use season name as collection title when listing season episodes
* Use a different query (ask for queue) to validate the session. Previously, data for some hardcoded media was being requested, but that call now fails (the media must have been removed)
* Test new login credentials properly when changing them in the settings
* Optionally allow tricking CR into creating US-based session
* Use the correct Next icon in paged listings
* Use a UUID as device id instead of just random string
* Removed ClientPlatformExclusions from info.plist. The plugin works just fine for me using Firefox
* Removed access to Pop video category, which seems to be no longer on CR

v2.2.0
* The plugin will now respect the language preference you set on the CR website. (Account Settings > Video Preferences > Default Language) All titles, descriptions, and subtitles will be shown in the selected language.
* Updated the README.md with several new FAQs

v2.1.5
* Fixed an issue introduced by a recent CR update

v2.1.4
* Fixed a bug that prevented all-access members from authenticating as premium users

v2.1.3
* Fixed bug from previous release preventing single season shows from displaying properly

v2.1.2:
* Fixed bug preventing some shows from displaying seasons properly
* Added episode counts to each season

v2.1.1:
* Added a countdown to episode release to upcoming episode descriptions
* Changed the object type of upcoming episodes to play nice with Plex Home Theater

v2.1.0:
* Added code to the URL Service to allow Plex/Web, Roku, Windows 8, iOS, & many other Plex clients to use the plugin
* Added ClientPlatformExclusions for Chrome & Firefox
* Added details to the README.md as to clarify which Plex clients are supported

v2.0.2:
* Added background art throughout the plugin.
* Changed the search function to only return results that match the user's Crunchyroll premium membership type. This will keep users from getting search results for media they can't access

v2.0.1:
* Updated the URL service pattern match regex so that it correctly matches URLs being passed by the API

v2.0.0:
* Major release
* The plugin now uses HLS streams instead of webkit based video
* Free account support has been removed. The plugin now requires a premium membership.
* The plugin will only show you content for which you pay (E.g. Anime members will not be able to see Drama content)

v1.2.2:
* Fixed a bug with the login code that caused problems when trying to resume an invalid session

v1.2.1:
* Aspect ratio and video frame rate attributes are now displayed properly

v1.2.0:
* Added search functionality
* Added null/zero result return handling
* Updated the icon for the My Queue and History sections
* Updated the preferences file label for quality to Video Quality for clarity

v1.1.0:
* Added more metadata to each video
* Added Seasons & Genres filter under each of the primary sections
* Added a Pop section to the main menu
* Fixed a small bug regarding datetimes for free users

v1.0.0:
* Initial release

Credits
=======
I want to thank pgp90 and JeremySH for their awesome plugin that has kept the Plex Anime & Drama community happy for the past few years. When I set out to help improve that plugin I had no idea that it would lead to a complete re-write of the code base.
