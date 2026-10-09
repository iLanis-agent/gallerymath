# Gallery math

Three picture-hanging calculators as a small static site - exact arithmetic,
every borrowed number labeled:

- **Even spacing** - wall width, frame count and frame width become the exact
  gap (frames plus two ends), the first nail's offset, and a crowding verdict.
- **Hang height** - frame height and hanger drop become the nail height for an
  eye-level hang (labeled eye level 145 cm) and the frame's top edge.
- **Row fit** - counts of small/medium/large frames (labeled 20/30/50 cm)
  against the wall at a labeled 8 cm target gap: fits or too wide.

## Files

- `index.html` - landing page
- `app.html` - the three calculators
- `engine.js` - all arithmetic, shared by the page and the tests
- `oracle.py` - independent Python mirror of the engine; regenerates `expected.json`
- `expected.json` - 51 cases (per-card values plus error cases)
- `test.js` - runs the engine against `expected.json` (node test.js)

## Tests

```
python3 oracle.py   # regenerate expected cases
node test.js        # engine vs oracle
```
