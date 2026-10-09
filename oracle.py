#!/usr/bin/env python3
# Oracle for gallerymath. Mirrors engine.js float ops exactly (IEEE 754 doubles).
import math, json, os

EYE_LEVEL, TARGET_GAP = 145, 8
SIZES = {'small': 20, 'medium': 30, 'large': 50}

def jround(x):
    return math.floor(x + 0.5)
def round1(x):
    return jround(x * 10) / 10

def spacing(wallCm, frames, frameCm):
    gap = round1((wallCm - frames * frameCm) / (frames + 1))
    if gap <= 0:
        raise ValueError('fit')
    verdict = 'crowded - drop a frame' if gap < 5 else 'a tight gallery' if gap < 20 else 'a classic row' if gap <= 60 else 'sparse - add a frame'
    return {'gap_cm': gap, 'first_nail_cm': gap, 'frames_width_cm': frames * frameCm, 'verdict': verdict}

def hangHeight(frameHeightCm, dropCm):
    nail = round1(EYE_LEVEL + frameHeightCm / 2 - dropCm)
    verdict = 'a low hang' if nail < 120 else 'the eye-level sweet spot' if nail <= 170 else 'a high hang - check the ceiling'
    return {'nail_cm': nail, 'top_cm': round1(nail + dropCm), 'verdict': verdict}

def rowFit(wallCm, small, medium, large):
    counts = {'small': small, 'medium': medium, 'large': large}
    total = sum(counts.values())
    framesWidth = sum(counts[k] * SIZES[k] for k in counts)
    required = framesWidth + (total + 1) * TARGET_GAP
    fits = required <= wallCm
    verdict = f'fits with equal {TARGET_GAP} cm gaps' if fits else 'too wide - trim a frame'
    return {'frames': total, 'frames_width_cm': framesWidth, 'required_cm': required, 'fits': fits, 'verdict': verdict}

FUN = {'spacing': spacing, 'hangHeight': hangHeight, 'rowFit': rowFit}

CASES = [
  {'card':'spacing','args':[300,3,40]},  {'card':'spacing','args':[300,5,40]},
  {'card':'spacing','args':[200,2,50]},  {'card':'spacing','args':[500,4,60]},
  {'card':'spacing','args':[120,3,30]},  {'card':'spacing','args':[800,6,50]},
  {'card':'spacing','args':[150,1,30]},  {'card':'spacing','args':[1000,10,30]},
  {'card':'spacing','args':[250,8,20]},  {'card':'spacing','args':[180,4,35]},
  {'card':'spacing','args':[600,3,80]},  {'card':'spacing','args':[90,2,25]},
  {'card':'spacing','args':[0,3,40],'error':'positive'},
  {'card':'spacing','args':[300,0,40],'error':'positive'},
  {'card':'spacing','args':[300,2.5,40],'error':'whole frames'},
  {'card':'spacing','args':[100,5,40],'error':'do not fit'},
  {'card':'spacing','args':[300,3,0],'error':'positive'},
  {'card':'spacing','args':[3000,3,40],'error':'under 20 m'},
  {'card':'hangHeight','args':[40,5]},   {'card':'hangHeight','args':[60,10]},
  {'card':'hangHeight','args':[30,3]},   {'card':'hangHeight','args':[100,20]},
  {'card':'hangHeight','args':[50,0]},   {'card':'hangHeight','args':[80,15]},
  {'card':'hangHeight','args':[25,2]},   {'card':'hangHeight','args':[120,30]},
  {'card':'hangHeight','args':[70,8]},   {'card':'hangHeight','args':[200,40]},
  {'card':'hangHeight','args':[90,12]},  {'card':'hangHeight','args':[35,4]},
  {'card':'hangHeight','args':[0,5],'error':'positive'},
  {'card':'hangHeight','args':[40,-2],'error':'zero or more'},
  {'card':'hangHeight','args':[40,40],'error':'less than'},
  {'card':'hangHeight','args':[300,5],'error':'under 250'},
  {'card':'rowFit','args':[300,2,2,1]},  {'card':'rowFit','args':[200,2,2,1]},
  {'card':'rowFit','args':[500,4,3,2]},  {'card':'rowFit','args':[150,1,1,1]},
  {'card':'rowFit','args':[100,1,1,0]},  {'card':'rowFit','args':[800,5,4,3]},
  {'card':'rowFit','args':[120,0,2,1]},  {'card':'rowFit','args':[60,1,0,0]},
  {'card':'rowFit','args':[250,3,1,1]},  {'card':'rowFit','args':[400,2,4,2]},
  {'card':'rowFit','args':[90,0,1,1]},   {'card':'rowFit','args':[1000,10,5,4]},
  {'card':'rowFit','args':[0,2,2,1],'error':'positive'},
  {'card':'rowFit','args':[300,0,0,0],'error':'at least one'},
  {'card':'rowFit','args':[300,2.5,0,0],'error':'whole frames'},
  {'card':'rowFit','args':[300,-1,0,0],'error':'zero or more'},
  {'card':'rowFit','args':[300,11,0,0],'error':'under 11'},
]

out = []
for c in CASES:
    row = dict(c)
    if 'error' not in c:
        row['expect'] = FUN[c['card']](*c['args'])
    out.append(row)
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'expected.json')
with open(path, 'w') as fh:
    json.dump(out, fh, indent=1)
    fh.write('\n')
print(len(out), 'cases written')
