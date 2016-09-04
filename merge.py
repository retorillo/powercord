# (C) 2016 Retorillo
# Distributed under the MIT license.

import os
import sys
import fontforge

scodFile = sys.argv[1]
miguFile = sys.argv[2]
sbolFile = sys.argv[3]
weight = sys.argv[4]
half = sys.argv[5] == "half"

if half:
  suffix = "0M"
else:
  suffix = "1M"

name = "PowerCord%s-%s" % (suffix, weight)
if weight != "Regular":
  family = "Power Cord %s %s" % (suffix, weight)
else:
  family = "Power Cord %s" % (suffix)
tmpDir = "tmp"
destDir = "dest"
version = "1.1"
copyright = "Copyright 2010, 2012 Adobe Systems Incorporated \n\
Copyright (C) 2002-2015 M+ FONTS PROJECT \n\
Copyright(c) Information-technology Promotion Agency, Japan (IPA), 2003-2011."
miguSfd = "tmp/migu.sfd"

def awidth(font):
  font.selection.select("a")
  for g in font.selection.byGlyphs:
    w = g.width
  font.selection.none()
  return w

scod = fontforge.open(scodFile)
migu = fontforge.open(miguFile)

scodwidth = awidth(scod)
miguwidth = awidth(migu)

# Fullwidth glyphs will take too wider area (maybe 4 characters) with
# os2_version = 3
scod.os2_version = 1

# To be a valid fixed-width font in terminal, code page should be changed,
# unless all full-width glyphs are shrinked to half-width.
scod.os2_codepages = migu.os2_codepages

migu.em = scod.em
migu.ascent = scod.ascent
migu.descent = scod.descent
for g in migu.glyphs():
  if g.width == 0:
    continue
  elif g.width == miguwidth * 2:
    if not half:
      g.width = scodwidth * 2
    else:
      g.transform((scodwidth / (miguwidth * 2.0), 0, 0, 1, 0, 0))
      g.width = scodwidth
  elif g.width == miguwidth:
    g.width = scodwidth
  else:
    g.clear()

if not os.access(tmpDir, os.R_OK):
  os.makedirs(tmpDir)

migu.save(miguSfd)
scod.mergeFonts(sbolFile)
scod.mergeFonts(miguSfd)

scod.sfnt_names = (( "English (US)", "Copyright", copyright ), 
  ( "English (US)", "Version", version ),
  ( "English (US)", "UniqueID", "{1};{0}".format(name, version) ))
scod.fontname = name
scod.fullname = family
scod.familyname = family
scod.weight = weight
scod.version = version

if not os.access(destDir, os.R_OK):
  os.makedirs(destDir)
scod.generate("{0}/{1}.ttf".format(destDir, name))
