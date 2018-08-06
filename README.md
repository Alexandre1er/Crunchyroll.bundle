License
=======

If the software submitted to this repository accesses or calls any software provided by Plex (“Interfacing Software”), then as a condition for receiving services from Plex in response to such accesses or calls, you agree to grant and do hereby grant to Plex and its affiliates worldwide a worldwide, nonexclusive, and royalty-free right and license to use (including testing, hosting and linking to), copy, publicly perform, publicly display, reproduce in copies for distribution, and distribute the copies of any Interfacing Software made by you or with your assistance; provided, however, that you may notify Plex at legal@plex.tv if you do not wish for Plex to use, distribute, copy, publicly perform, publicly display, reproduce in copies for distribution, or distribute copies of an Interfacing Software that was created by you, and Plex will reasonable efforts to comply with such a request within a reasonable time.

About
=====
This plugin provides access to the Anime and Drama video content available at Crunchyroll.com. This plugin requires the user to have a **premium** crunchyroll.com membership. You can sign up for a free 14-day trial by [clicking here](https://www.crunchyroll.com/freetrial). Free membership accounts will not work.

While this plugin is considered stable, there will always be bugs. Please submit bugs via the Github issue tracker or in the [official thread on the Plex forums](https://forums.plex.tv/t/rel-crunchyroll-plugin/38007). Feedback and/or suggestions are welcome.

End of Life notice
==================
This plugin is no longer actively maintained. It should still be fully functional, but there's no guarantee that it will continue to work.

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
1. Download the latest version of the plugin from the releases page or by clicking the green **Clone and download** button on the GitHub page.
2. Unzip the content into the PMS plugins directory under your user account.
	* Windows 7, Vista, or Server 2008: C:\Users\[Your Username]\AppData\Local\Plex Media Server\Plug-ins
	* Windows XP, Server 2003, or Home Server: C:\Documents and Settings\[Your Username]\Local Settings\Application Data\Plex Media Server\Plug-ins
	* Mac/Linux: ~/Library/Application Support/Plex Media Server/Plug-ins
	* FreeNAS: /var/db/plexdata/Plex Media Server/Plug-ins
3. Rename the unzipped folder from "Crunchyroll.bundle-*" to "Crunchyroll.bundle"
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
v2.3.3
* Update spoofed device

v2.3.2
* Minor changes

v2.3.1
* Fixed a bug which caused 2.3.0 to actually not work at all

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
This plugin is mostly written by @MattRK, with contributions from @sander1, and later @rimas-kudelis.

The author wants to thank pgp90 and JeremySH for their awesome plugin that had kept the Plex Anime & Drama community happy for years before his own plugin was released. When he set out to help improve that plugin he had no idea that it would lead to a complete re-write of the code base.
