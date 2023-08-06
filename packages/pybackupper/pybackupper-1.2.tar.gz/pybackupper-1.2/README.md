# Author: Savelev Matthew (savelevmatthew@gmail.com)

# Description:
	This Lib upload your file or directory on few Cloud services such as Google Drive and Yandex Disk
	To import Lib as package use:
		pip install pybackupper


# Requirements:
	Python 3.7
	All packages from requirements.txt

# Lib Contains:
	- Google - package to work with Google Drive
		|
		|
			- GAuth.py - Google Drive Authoriztion methods
			- GMain.py - Contains main functions for working with Google Drive
			-	GRequests.py - Google Drive Requests methods
	- Yandex - package to work with YaDisk
		|
		|
			- YMain.py - Contains main functions for working with Yandex Disk
			- YAuth.py - Yandex Drive Authoriztion methods
			- YRequests.py - Yandex Requsets Requests methods

# Project contains:
	google_client_secret.json - File with app data
	requirements.txt - list of requirement packages. use pip install -r requirements.txt to install them
	main.py -  test file to launch
