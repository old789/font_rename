#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import fnmatch
from fontTools import ttLib

FONT_SPECIFIER_NAME_ID = 4
FONT_SPECIFIER_FAMILY_ID = 1
def shortName( font ):
	"""Get the short name from the font's names table"""
	name = ""
	family = ""
	for record in font['name'].names:
		if record.nameID == FONT_SPECIFIER_NAME_ID and not name:
			if '\000' in record.string:
				name = unicode(record.string, 'utf-16-be').encode('utf-8')
			else:
				name = record.string
		elif record.nameID == FONT_SPECIFIER_FAMILY_ID and not family:
			if '\000' in record.string:
				family = unicode(record.string, 'utf-16-be').encode('utf-8')
			else:
				family = record.string
		if name and family:
			break
	return name, family

def fontRen(fontFile):
	if fnmatch.fnmatch(fontFile.lower(), "*.ttf"):
		fontExt='ttf'
	elif fnmatch.fnmatch(fontFile.lower(), "*.otf"):
		fontExt='otf'
	else:
		print 'Unknown type of file',item
		return
	print 'Try to rename',fontFile
	t = ttLib.TTFont(fontFile)
	fontName=shortName(t)[0]
	newFileName=fontName.replace(' ','_')+'.'+fontExt
	curDir=os.path.dirname(fontFile)
	if len(curDir) > 0:
		newFileName=os.path.join(curDir,newFileName)
	if newFileName != fontFile:
		if os.path.exists(newFileName):
			print 'Can\'t rename',fontFile,'-->',newFileName,' - file exists'
		else:
			print fontFile+' --> '+newFileName
			os.rename(fontFile,newFileName)

item=''
indexOfDirLs=''
f=sys.argv[1]
if os.path.isfile(f):
	fontRen(f)
elif os.path.isdir(f):
	indexOfDirLst=os.listdir(f)
	if len(indexOfDirLst) > 0:
		for item in indexOfDirLst:
			fontRen(os.path.join(f,item))
