About
=====
This plugin provides access to the Anime and Drama video content available at Crunchyroll.com. This plugin requires the user to have a **premium** crunchyroll.com membership. You can sign up for a free 14-day trial by [clicking here](https://www.crunchyroll.com/freetrial/anime). Free membership accounts will not work.

While this plugin is considered stable, there will always be bugs. Please submit bugs via the Github issue tracker on this page. I would also love to hear feedback and/or suggestions. 

Version 2
=========
Version 2 is a major step towards stability and reliability. Version 1 of this app was based on Webkit and flash video. While this did work, it was not remotely stable or reliable. Version 2 has been redesigned to use HLS streams which are much more stable and reliable. The video quality is also much better. 

The biggest change, however, is that Version 2 no longer supports *free* Crunchyroll accounts. While i regret this, i would like to point out that none of Crunchyroll's official apps (PS3, Xbox, Apple TV, etc) support free accounts either. The main reason is because of the way Crunchyroll encodes their videos. They don't currently insert ADs with these higher quality streams. When/if they change this in the future, i will certainly update the app to support free accounts again. 

Requirements
============
This plugin **requires** a **premium** Crunchyroll.com account. You can sign up for free trial by [clicking here](https://www.crunchyroll.com/freetrial/anime). When you get the plugin installed you will need to enter your username and password into the preferences section before you will be able to use it. 

* **Plex Media Server:**
	* Version 0.9.7.28 or later (http://www.plexapp.com/getplex/)
	* Windows & Mac
	* *Linux & NAS Appliances have not been tested yet. If you have success with these platforms please let me know so i can update this readme.*
* **Plex Clients:**
	* Plex Media Center & Plex Home Theater for Windows & Mac
	* Roku
	* Windows 8
	* iOS
	* Plex/Web in Safari *(Firefox & Chrome do not work)*
	* PlexConnect for AppleTV
	* *Android, Windows Phone, LG TVs, Samsung TVs, and Google TV have not been tested yet. If you have success with these clients please let me know so i can update this readme.*

Installation
============
1. Download the latest version of the plugin from [here](https://github.com/MattRK/Crunchyroll.bundle/archive/v2.1.0.zip).

2. Unzip the content into the PMS plugins directory under your user account.
	* Windows 7, Vista, or Server 2008: C:\Users\[Your Username]\AppData\Local\Plex Media Server\Plug-ins
	* Windows XP, Server 2003, or Home Server: C:\Documents and Settings\[Your Username]\Local Settings\Application Data\Plex Media Server\Plug-ins
	* Mac/Linux: ~/Library/Application Support/Plex Media Server/Plug-ins

3. Rename the unzipped folder from "Crunchyroll.bundle-vx.x.x" to "Crunchyroll.bundle"

4. Restart PMS


Known Issues
============
* Some of the Pop videos don't play correctly. This is due to the way Crunchyroll formats those URLs. They are not standardized and as such it is hard to ensure the plugin is able to handle these properly. Fortunately this is not an issue for any of the Anime or Drama videos.  


Frequently Asked Questions
==========================
**Q: I selected 1080P or 720P but the video is played in a lower resolution**

A: Not all content on Crunchyroll has HD quality videos available. This plugin will try to play content at the resolution you select. However, if a particular resolution is not available, it will play the next highest resolution available. This may also occur shortly after Crunchyroll releases a new video. Sometimes it takes Crunchyroll longer than expected to encode the HD quality videos. During this period of time the plugin only has access to the lower quality streams that have already been encoded. If this is the case, check back later and the HD quality video should be available. 

**Q: How do i hide mature content?**

A: You can choose what type of content to show by changing the Mature Content Filter setting found under "Account Settings" > "Video Preferences" of the http://www.crunchyroll.com website. 

To-do
====
- [ ] Change the available_at descriptions to relative datetimes rather than actual datetimes. (E.g. 2 Days rather than 2013-03-05 11:00 PM) 
- [ ] Add support for Simulcast countdowns 

Changes
=======
v2.1.0:
* Added code to the URL Service to allow Plex/Web, Roku, Windows 8, iOS, & many other Plex clients to use the plugin. 
* Added ClientPlatformExclusions for Chrome & Firefox
* Added details to the README.md as to clarify which Plex clients are supported.  

v2.0.2:
* Added background art throughout the plugin.
* Changed the search function to only return results that match the user's Crunchyroll premium membership type. This will keep users from getting search results for media they can't access.

v2.0.1:
* Updated the URL service pattern match regex so that it correctly matches URLs being passed by the API.

v2.0.0:
* Major release
* The plugin now uses HLS streams instead of webkit based video
* Free account support has been removed. The plugin now requires a premium membership. 
* The plugin will only show you content for which you pay. (E.g. Anime members will not be able to see Drama content.)

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