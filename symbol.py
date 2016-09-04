# Copyright (C) 2016 Retorillo
# Distributed under the MIT license

import fontforge    
import math
import sys
import os

refFile = sys.argv[1]
dest = sys.argv[2]

previewDir = "%s.preview" % dest

if not os.access(previewDir, os.R_OK):
  os.makedirs(previewDir)

def drawStar(pen, cx, cy, outarc, inarc, tips, rot):
  c = 0
  t = rot
  while c < tips:
    outrad = (math.pi * 2 / tips) * t
    inrad = (math.pi * 2 / tips) * (t + 0.5)
    xi = cx + math.sin(inrad) * inarc
    yi = cy + math.cos(inrad) * inarc
    xo = cx + math.sin(outrad) * outarc
    yo = cy + math.cos(outrad) * outarc
    if c == 0:
      pen.moveTo((xo, yo))
    else:
      pen.lineTo((xo, yo))
    pen.lineTo((xi, yi))
    c += 1
    t += 1
  pen.closePath()

def drawRectangle(pen, cx, cy, width, height):
  pen.moveTo((cx - width / 2, cy - height / 2))
  pen.lineTo((cx + width / 2, cy - height / 2))
  pen.lineTo((cx + width / 2, cy + height / 2))
  pen.lineTo((cx - width / 2, cy + height / 2))
  pen.closePath()

def drawTrigram(pen, cx, cy, width, stroke, gap, tricode):
  y = stroke + gap
  for t in tricode:
    w = (width - gap * (t - 1)) / t
    x = - (width / 2.0) + w / 2.0
    for h in range(1, t + 1):
      drawRectangle(pen, cx + x, cy + y, w, stroke)
      x += w + gap
    y -= stroke + gap

ref = fontforge.open(refFile)

font = fontforge.font()
font.em = ref.em # 1000 is expected
font.ascent = ref.ascent
font.descent = ref.descent
font.encoding = "Unicode"
font.weight = "Regular"
font.fontname = "PowerCordSymbols-Regular"
font.familyname = "Power Cord Symbols"
font.fullname = font.familyname   
font.copyright = "Copyright (C) 2016 Retorillo\
\nDistributed under the MIT license"

bound = ref[0x007d].boundingBox() # curly bracket
centerY = (bound[1] + bound[3]) / 2.0

glyphWidth = 600
trigramWidth = glyphWidth * 0.8
trigramStroke = font.em / 7.0
trigramGap = trigramStroke
starArc = bound[3] / 2.0
starInArc = starArc * 0.35
starHeavyInArc = starArc * 0.45

stars = [
  { # trigram for Heaven
    "type": "trigram",
    "unicode": 0x2630,
    "width": trigramWidth,
    "stroke": trigramStroke,
    "gap": trigramGap,
    "tricode": [ 1, 1, 1 ]
  },
  { # trigram for Lake
    "type": "trigram",
    "unicode": 0x2631,
    "width": trigramWidth,
    "stroke": trigramStroke,
    "gap": trigramGap,
    "tricode": [ 2, 1, 1 ]
  },
  { # trigram for Fire
    "type": "trigram",
    "unicode": 0x2632,
    "width": trigramWidth,
    "stroke": trigramStroke,
    "gap": trigramGap,
    "tricode": [ 1, 2, 1 ]
  },
  { # trigram for Thunder
    "type": "trigram",
    "unicode": 0x2633,
    "width": trigramWidth,
    "stroke": trigramStroke,
    "gap": trigramGap,
    "tricode": [ 2, 2, 1 ]
  },
  { # trigram for Wind
    "type": "trigram",
    "unicode": 0x2634,
    "width": trigramWidth,
    "stroke": trigramStroke,
    "gap": trigramGap,
    "tricode": [ 1, 1, 2 ]
  },
  { # trigram for Water
    "type": "trigram",
    "unicode": 0x2635,
    "width": trigramWidth,
    "stroke": trigramStroke,
    "gap": trigramGap,
    "tricode": [ 2, 1, 2 ]
  },
  { # trigram for Mountain
    "type": "trigram",
    "unicode": 0x2636,
    "width": trigramWidth,
    "stroke": trigramStroke,
    "gap": trigramGap,
    "tricode": [ 1, 2, 2 ]
  },
  { # trigram for Earth
    "type": "trigram",
    "unicode": 0x2637,
    "width": trigramWidth,
    "stroke": trigramStroke,
    "gap": trigramGap,
    "tricode": [ 2, 2, 2 ]
  },
  { # eight pointed black start
    "type": "star",
    "unicode": 0x2734,
    "outarc": starArc,
    "inarc": starInArc,
    "tips": 8,
    "rot": 0,
  },
  { # six pointed black star
    "type": "star",
    "unicode": 0x2736,
    "outarc": starArc,
    "inarc": starInArc,
    "tips": 6,
    "rot": 0,
  },
  { # eight pointed rectiliner black star
    "type": "star",
    "unicode": 0x2737,
    "outarc": starArc,
    "inarc": starInArc,
    "tips": 8,
    "rot": 0.5,
  },
  { # heavy eight pointed rectiliner black star
    "type": "star",
    "unicode": 0x2738,
    "outarc": starArc,
    "inarc": starHeavyInArc,
    "tips": 8,
    "rot": 0.5,
  },
  { # twelve pointed black star
    "type": "star",
    "unicode": 0x2739,
    "outarc": starArc,
    "inarc": starHeavyInArc,
    "tips": 15,
    "rot": 0,
  },
]

for s in stars:
  font.createChar(s["unicode"])
  glyph = font[s["unicode"]]
  pen = glyph.glyphPen()
  if s["type"] == "star":
    drawStar(pen, glyphWidth / 2, centerY, s["outarc"],
      s["inarc"], s["tips"], s["rot"])
  elif s["type"] == "trigram":
    drawTrigram(pen, glyphWidth  / 2, centerY, s["width"],
      s["stroke"], s["gap"], s["tricode"])
  glyph.width = glyphWidth
  glyph.export("%s/U+%x.bmp" % (previewDir, s["unicode"]))
font.save(dest)
