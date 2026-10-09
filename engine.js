/* Gallery math - exact arithmetic, labeled hanging norms.
   Labeled norms shown in the UI: eye level 145 cm from the floor, target gap
   8 cm between frames, standard frame widths small 20 / medium 30 / large 50 cm.
   Gaps and nail heights round to 0.1 cm. */
(function (root) {
  'use strict';

  var EYE_LEVEL = 145, TARGET_GAP = 8;
  var SIZES = { small: 20, medium: 30, large: 50 };

  function num(v, name) {
    if (typeof v !== 'number' || !isFinite(v)) throw new Error(name + ' must be a number');
    return v;
  }
  function round1(x) { return Math.round(x * 10) / 10; }

  function spacing(wallCm, frames, frameCm) {
    wallCm = num(wallCm, 'wall width');
    if (wallCm <= 0) throw new Error('wall width must be positive');
    if (wallCm > 2000) throw new Error('keep the wall under 20 m (labeled)');
    frames = num(frames, 'frames');
    if (!Number.isInteger(frames)) throw new Error('count frames in whole frames');
    if (frames < 1) throw new Error('frames must be positive');
    if (frames > 20) throw new Error('keep it under 21 frames (labeled)');
    frameCm = num(frameCm, 'frame width');
    if (frameCm <= 0) throw new Error('frame width must be positive');
    if (frameCm > 200) throw new Error('keep the frame under 200 cm (labeled)');
    var gap = round1((wallCm - frames * frameCm) / (frames + 1));
    if (gap <= 0) throw new Error('frames do not fit on this wall');
    var verdict = gap < 5 ? 'crowded - drop a frame' : gap < 20 ? 'a tight gallery' : gap <= 60 ? 'a classic row' : 'sparse - add a frame';
    return { gap_cm: gap, first_nail_cm: gap, frames_width_cm: frames * frameCm, verdict: verdict };
  }

  function hangHeight(frameHeightCm, dropCm) {
    frameHeightCm = num(frameHeightCm, 'frame height');
    if (frameHeightCm <= 0) throw new Error('frame height must be positive');
    if (frameHeightCm > 250) throw new Error('keep the frame under 250 cm (labeled)');
    dropCm = num(dropCm, 'hanger drop');
    if (dropCm < 0) throw new Error('hanger drop must be zero or more');
    if (dropCm >= frameHeightCm) throw new Error('hanger drop must be less than the frame height');
    var nail = round1(EYE_LEVEL + frameHeightCm / 2 - dropCm);
    var verdict = nail < 120 ? 'a low hang' : nail <= 170 ? 'the eye-level sweet spot' : 'a high hang - check the ceiling';
    return { nail_cm: nail, top_cm: round1(nail + dropCm), verdict: verdict };
  }

  function rowFit(wallCm, small, medium, large) {
    wallCm = num(wallCm, 'wall width');
    if (wallCm <= 0) throw new Error('wall width must be positive');
    if (wallCm > 2000) throw new Error('keep the wall under 20 m (labeled)');
    var counts = { small: small, medium: medium, large: large };
    var total = 0, framesWidth = 0;
    for (var k in counts) {
      var c = num(counts[k], k + ' frames');
      if (!Number.isInteger(c)) throw new Error('count frames in whole frames');
      if (c < 0) throw new Error(k + ' frames must be zero or more');
      if (c > 10) throw new Error('keep each size under 11 frames (labeled)');
      total += c;
      framesWidth += c * SIZES[k];
    }
    if (total === 0) throw new Error('hang at least one frame');
    var required = framesWidth + (total + 1) * TARGET_GAP;
    var fits = required <= wallCm;
    var verdict = fits ? 'fits with equal ' + TARGET_GAP + ' cm gaps' : 'too wide - trim a frame';
    return { frames: total, frames_width_cm: framesWidth, required_cm: required, fits: fits, verdict: verdict };
  }

  var api = { spacing: spacing, hangHeight: hangHeight, rowFit: rowFit };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.GalleryMath = api;
})(typeof window !== 'undefined' ? window : globalThis);
