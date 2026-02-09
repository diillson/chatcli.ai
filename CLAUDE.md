# chatcli.edilsonfreitas.com Landing Page

## Data Files

### Showcase (`src/data/showcase.json`)
- "What People Are Building" page - detailed tweets with projects/workflows
- **Sorted into uniform rows**: all-SHORT rows, all-MED rows, all-LONG rows
- This ensures consistent row heights in the 3-column CSS grid
- Categories: SHORT (<200 chars), MED (200-400), LONG (>400)
- Fields: `id`, `author`, `quote`, `category`, `likes`, `images?` (array of URLs)
- **Important**: `showcase.astro` uses JSON order directly (no re-sorting) — maintain order in JSON

### Testimonials (`src/data/testimonials.json`)
- Short praise quotes for the shoutouts page
- Sorted by quote length (most detailed/impressive first)
- Deduplicated by author (keep longest quote)
- Backup: `testimonials-backup.json` contains weakest 10% removed

## Maintenance

When adding new tweets:
1. Use `bird read <tweet_id>` to fetch content and like count
2. "Building" tweets → showcase.json (describe what they built)
3. "Praise" tweets → testimonials.json (short praise/reactions)
4. Re-sort after batch additions

Showcase sorting script pattern:
```js
// Group by size for uniform row heights
const longs = sorted.filter(t => t.quote.length > 400);
const meds = sorted.filter(t => t.quote.length > 200 && t.quote.length <= 400);
const shorts = sorted.filter(t => t.quote.length <= 200);
// Alternate: 3 shorts, 3 meds, 3 longs, repeat
// Keeps high-engagement items near top within each category
```
