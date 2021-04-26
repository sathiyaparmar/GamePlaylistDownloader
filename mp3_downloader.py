# Author - Sathiya Parmar

from pprint import pprint 

import os, json, requests
from bs4 import BeautifulSoup
from pathlib import Path

class GamePlaylistDownloader(object):

	"""
	Download playlist from https://downloads.khinsider.com
	"""

	def __init__(self,url,showLog=True):
		self.url = url
		self.showLog = showLog
		self.albumName = self.url.split('/')[-1]

		musicDirectory = os.path.join(Path.home(),'Music')

		self._savePath = os.path.join(musicDirectory,self.albumName)

		if not os.path.exists(self._savePath):
			os.mkdir(self._savePath)

		for i in self.url.split('/'):
			if '.com' in i:
				break

		self.site = self.url.split('/')[0]+'//'+i
		self.songsEndpoints = dict()
		self.enc = {
			'%2520':'_',
			'%2526':'&',
			'%2527':"'",
			'%2528':'(',
			'%2529':')'
		}

	def _convert_raw_to_name(self,rawname):
		"""
		Converts raw html url into meaningful name
		"""
		
		songname = rawname
		for code,parse in self.enc.items():
			songname = songname.replace(code,parse)

		return songname

	def _find_songs_endpoints(self):
		"""
		Finds all links in webpages that ends with music file extension
		"""
		response = requests.get(self.url)
		soup = BeautifulSoup(response.text,'html.parser')

		for link in soup.findAll('a'):
			linkPath = link.get('href')
			if linkPath:
				if linkPath.endswith('.mp3'):
					self.songsEndpoints[self.site+linkPath] = self._convert_raw_to_name(linkPath.split('/')[-1])

	def download(self):

		self._find_songs_endpoints()

		for sLink,sName in self.songsEndpoints.items():
			song = requests.get(sLink)

			soup = BeautifulSoup(song.text,'html.parser')
			
			for link in soup.findAll('a'):
				linkPath = link.get('href')
				if linkPath:
					if linkPath.endswith('.mp3'):
						finalLink = linkPath
						break

			actualSong = requests.get(finalLink)
			with open(os.path.join(self._savePath,sName), 'wb') as f:
				f.write(actualSong.content)
				f.close()

			if self.showLog:
				print(f"Downloaded {sName}")

if __name__ == '__main__':

	url = "https://downloads.khinsider.com/game-soundtracks/album/far-cry-3"

	M1 = GamePlaylistDownloader(url=url,showLog=True)

	M1.download()