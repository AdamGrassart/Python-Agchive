#!/usr/bin/env python
# -*- coding: utf8 -*-

# system commande  
import os
import shutil
import glob
import subprocess
# compression modules
import zipfile


class Agchive:

	srcDir = None			# Src archive unzip
	destDir = None       	# Destination unzip
	removeSrc = False		# Remove the source archive after extract
	fileAndExt = None		# Array with file and extention 
	dependencies = {}		# dependencies between extention and methods


	def __init__(self):
		""" Constructor Class
		 Init dependencies betwen extention and method
		"""
		self.__setDependencies()


	# --------------------------------------------------------------
	# --- Compress, Decompress : Action to call --------------------
	# --------------------------------------------------------------

	def extract(self, srcDir, destDir, removeSrc = False):
		""" extract : controller
		Get generals informations to extract with good method
		"""
		# Define generals informations about extract action
		self.__setInfo(srcDir, destDir, removeSrc)
		self.__setInfoExtention(srcDir)
		# Call method in dependencies array with extention used
		self.dependencies[self.fileAndExt[1]]['extract']()


	def compress(self, srcDir, destDir, removeSrc = False):
		""" compress : controller
		Get generals informations to compress with good method
		"""
		# Define generals informations about compress action
		self.__setInfo(srcDir, destDir, removeSrc)
		self.__setInfoExtention(destDir)
		# Call method in dependencies array with extention used
		self.dependencies[self.fileAndExt[1]]['compress']()


	# --------------------------------------------------------------
	# --- SETTER and GETTER informations	    --------------------
	# --------------------------------------------------------------


	def __setInfo(self, srcDir, destDir, removeSrc):
		""" setInfo : general
		Set info about source -> destination | keepSource ? 
		"""
		self.srcDir = srcDir
		self.destDir = destDir
		self.removeSrc = removeSrc


	def __setInfoExtention(self,extention):
		""" setInfo : extention file src or dest 
		Used to know extention and what app to call (zip, rar, 7z...)
		"""
		self.fileAndExt = os.path.splitext(extention)


	# --------------------------------------------------------------
	# --- For Zip methods 	----------------------------------------
	# --------------------------------------------------------------

	def agZip(self):
		""" Compress with ZIP
		Zip an archive folder or simple file
		"""
		# folder ? --> Recursive zip for all subdir
		if os.path.isdir(self.srcDir):
			lenParentFolder = len(self.srcDir)+1
			def _agZip(zfile, path):
				for i in glob.glob(path+'\\*'):
					if os.path.isdir(i): _agZip(zfile, i )
					else:
						zfile.write(i, i[lenParentFolder:])
			zfile = zipfile.ZipFile(self.destDir,'w',compression=zipfile.ZIP_DEFLATED)
			_agZip(zfile, self.srcDir)
			zfile.close()
		if self.removeSrc:
			shutil.rmtree(self.srcDir)
		# File ? --> Simple compress
		else:
			fileToComp = os.path.basename(os.path.normpath(self.srcDir))
			f = zipfile.ZipFile(self.destDir,'w',zipfile.ZIP_DEFLATED)
			f.write(self.srcDir, fileToComp)
			f.close()
		if self.removeSrc:
			os.remove(self.srcDir)


	def agUnzip(self):
		""" Extract with ZIP
		unZip an archive
		"""
		try:
			with zipfile.ZipFile(self.srcDir) as zf:
				zf.extractall(self.destDir)
			# Remove archive source if removeSrc == True
			if self.removeSrc:
				os.remove(self.srcDir)
		except IOError as e:
			print ("I/O error({0}): {1}".format(e.errno, e.strerror))


	# --------------------------------------------------------------
	# --- For rar methods 	----------------------------------------
	# --------------------------------------------------------------


	def agUnrar(self):
		""" Extract with RAR
		unRar an archive whit unrar.exe application
		"""
		try:
			appRar = os.getcwd() + "/app/unrar/unrar.exe"
			compress = subprocess.call(appRar + ' x "' + self.srcDir + '" "' + self.destDir + '\\"', stdout = open(os.devnull, 'wb'))
			# Remove archive source if removeSrc == True
			if self.removeSrc:
				os.remove(self.srcDir)
		except IOError as e:
			print ("I/O error({0}): {1}".format(e.errno, e.strerror))


	# --------------------------------------------------------------
	# --- For 7z methods 	----------------------------------------
	# --------------------------------------------------------------


	def agSzip(self):
		""" compress with 7z
		Create an archive with 7z.exe application
		"""
		try:
			app7ze = os.getcwd() + "/app/7za/7za.exe"
			compress = subprocess.call(app7ze+ ' u -tzip "' + self.destDir + '" "' + self.srcDir +'"', stdout = open(os.devnull, 'wb'))
			# Remove archive source if removeSrc == True
			if self.removeSrc:
				shutil.rmtree(self.srcDir)
		except IOError as e:
			print ("I/O error({0}): {1}".format(e.errno, e.strerror))


	def agUnszip(self):
		""" Extract with 7z
		unSzip an archive with 7z.exe application
		"""
		try:
			app7ze = os.getcwd() + "/app/7za/7za.exe"
			decompress = subprocess.call(app7ze + ' x "' + self.srcDir + '" -o"' + self.destDir + '"', stdout = open(os.devnull, 'wb'))
			# Remove archive source if removeSrc == True
			if self.removeSrc:
				os.remove(self.srcDir)
		except IOError as e:
			print ("I/O error({0}): {1}".format(e.errno, e.strerror))


	# --------------------------------------------------------------
	# --- dependencies 		----------------------------------------
	# --------------------------------------------------------------


	def __setDependencies(self):
		""" dependencies library 
		To know the link between :
		extention + action <==> method to call
		"""
		self.dependencies = {
			".zip"	:{ # Zip application for .zip
				"compress"	:	self.agZip,
				"extract":	self.agUnzip,
				},
			".rar"	:{ # Rar application for .rar
				"extract" 	:	self.agUnrar
				},
			".7z"	:{ # Rar application for .rar
				"compress" 	:	self.agSzip,
				"extract" 	:	self.agUnszip
				}
		}
