/**
 * Bubble stories from the command line, for Claude and Codex. It uses the
 * same engine and picture library as the studio (/studio/stories), so what
 * it checks and renders is exactly what Frank sees.
 *
 *   npm run stories -- help
 *
 * Frank's saved studio edits live in the database and win over the files
 * here; pull them first (see `help`) before changing a story he has edited.
 */

import { spawnSync } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'
import { bubbleOutline, compileStory, FPS, itemTransform, type Frame } from '../src/activityStories/compile'
import { LIBRARY, STORY_FILES } from '../src/activityStories/drafts'
import { cleanStory, describeStep, groupPictures, playsText, STORY_SCHEMA, versionFor, type Story } from '../src/activityStories/format'

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const STORIES_DIR = path.join(ROOT, 'data/activity-stories/stories')
const DRAFTS_TS = path.join(ROOT, 'src/activityStories/drafts.ts')
const OUT_DIR = path.join(ROOT, 'tmp/activity-stories')
const REPO_PREFIX = '/activity-stories/repo/'

const HELP = `Bubble stories: the command-line tool (same engine as the studio)

  npm run stories -- pictures [search]
      Every picture in the library, in the studio's groups, with the id a
      story uses. Add a word to search (e.g. "sponge", "bbq", "marks").

  npm run stories -- list
      Every story: length, how often it plays in a 20–30 s activity, problems.

  npm run stories -- check <story-id | path/to/story.json>
      The steps in order with their timing, and every problem the studio
      would show. Exits 1 if anything cannot play.

  npm run stories -- render <story-id | path/to/story.json> [options]
      Draws the story's frames onto one picture sheet (PNG) to look at.
        --reduced        the reduced-motion version
        --every N        every Nth frame (default: about 36 frames in all)
        --from F --to T  only frames F to T (1-based, as the studio counts)
        --restart        the last frames of a telling, then the retelling's first
        --out DIR        where to write (default tmp/activity-stories/)

  npm run stories -- new <story-id> --label "Name" [--like garden-bbq]
      Starts a story file and lists it in the studio. --like copies an
      existing story to start from.

Related:
  node --env-file=.env.local scripts/pull_activity_stories.mjs
      Copy Frank's saved studio edits into the repo (read-only on the database).
  npm run activity-stories:add-picture -- <id> <file.png> --note "…"
      Add a picture, or a new version of one (Codex).
  npm run verify:activity-stories
      Check the library and every story's picture references.

Formats and rules: data/activity-stories/README.md`

const args = process.argv.slice(2).filter((a) => a !== '--')
const [command, target] = args
const flag = (name: string) => {
  const i = args.indexOf(`--${name}`)
  return i >= 0 ? args[i + 1] : undefined
}
const has = (name: string) => args.includes(`--${name}`)
function fail(msg: string): never {
  console.error(`✗ ${msg}`)
  process.exit(1)
}

/** A story by id (a file in data/activity-stories/stories/) or by path. */
function loadStory(ref: string | undefined): Story {
  if (!ref) fail('name a story: an id such as garden-bbq, or a path to a story .json file')
  const file = fs.existsSync(ref) ? ref : path.join(STORIES_DIR, `${ref}.json`)
  if (!fs.existsSync(file)) fail(`no story "${ref}". Stories: ${Object.keys(STORY_FILES).join(', ')}`)
  let raw: unknown
  try {
    raw = JSON.parse(fs.readFileSync(file, 'utf8'))
  } catch (e) {
    fail(`${file} is not valid JSON: ${(e as Error).message}`)
  }
  const story = cleanStory(raw)
  if (!story) fail(`${file} is not a story (it needs at least an "id" in lower-case-kebab)`)
  return story
}

/** The file on disk behind a library URL: a pack under art/drafts/, a /activity-stories/ file in public/, or an archived /keeper-review/ path. */
let archive: Record<string, { object: string }> | null = null
function fileFor(url: string): string | null {
  if (url.startsWith(REPO_PREFIX)) return path.join(ROOT, url.slice(REPO_PREFIX.length))
  if (url.startsWith('/activity-stories/')) return path.join(ROOT, 'public', url)
  archive ??= JSON.parse(fs.readFileSync(path.join(ROOT, 'review-archive/index.json'), 'utf8')).legacyPaths as Record<string, { object: string }>
  const entry = archive[url]
  return entry ? path.join(ROOT, entry.object) : null
}

function pictures(search?: string) {
  const needle = search?.toLowerCase()
  let shown = 0
  for (const g of groupPictures(LIBRARY)) {
    const list = needle ? g.pictures.filter(([id, p]) => id.includes(needle) || p.label.toLowerCase().includes(needle) || g.label.toLowerCase().includes(needle)) : g.pictures
    if (!list.length) continue
    console.log(`\n${g.label} (${list.length})`)
    const w = Math.max(...list.map(([id]) => id.length))
    for (const [id, p] of list) {
      const versions = p.versions.length > 1 ? `v${p.current} of ${p.versions.length}` : `v${p.current}`
      console.log(`  ${id.padEnd(w)}  ${p.label} · ${p.kind} · ${versions}${p.review?.status === 'rework-requested' ? ' · rework asked' : ''}`)
    }
    shown += list.length
  }
  console.log(`\n${shown} of ${Object.keys(LIBRARY.pictures).length} pictures. A story's cast names a picture by its id.`)
}

function summary(story: Story) {
  const c = compileStory(story, LIBRARY)
  const errors = c.issues.filter((i) => i.level === 'error').length
  const problems = c.issues.length ? `${errors ? `${errors} cannot play, ` : ''}${c.issues.length - errors} warning${c.issues.length - errors === 1 ? '' : 's'}` : 'no problems'
  return { c, line: `${c.seconds.toFixed(1)} s, ${playsText(c.tellings)} in a 20–30 s activity, ${problems}` }
}

function list() {
  for (const id of Object.keys(STORY_FILES)) {
    const story = loadStory(id)
    console.log(`${id.padEnd(18)} ${story.label} · ${story.steps.length} steps · ${summary(story).line}`)
  }
}

function check(ref?: string) {
  const story = loadStory(ref)
  const { c, line } = summary(story)
  console.log(`${story.label} (${story.id}): ${line}`)
  console.log(`Flow ${story.flow}, ${story.afterStory === 'loop' ? `retells from step ${story.loopFrom ?? 1}` : story.afterStory}, pace ${story.pace}. Frames 1–${c.intro.length} open the bubble, then ${c.storyFrames} story frames at ${FPS} fps (numbered as in the studio and render).`)
  for (const [i, s] of story.steps.entries()) {
    const w = c.windows[i]
    console.log(`  ${String(i + 1).padStart(2)}. ${describeStep(LIBRARY, story, s).padEnd(52)} frames ${c.intro.length + w.start + 1}–${c.intro.length + w.end}`)
  }
  for (const issue of c.issues) console.log(`${issue.level === 'error' ? '⛔' : '⚠️ '} ${issue.step ? `step ${issue.step}: ` : ''}${issue.text}`)
  if (c.issues.some((i) => i.level === 'error')) process.exit(1)
}

function chrome(): string {
  const candidates = [
    process.env.CHROME_PATH,
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium',
  ]
  const cache = path.join(process.env.HOME ?? '', 'Library/Caches/ms-playwright')
  if (fs.existsSync(cache))
    for (const dir of fs.readdirSync(cache).filter((d) => d.startsWith('chromium_headless_shell-')).sort().reverse())
      for (const sub of fs.readdirSync(path.join(cache, dir))) candidates.push(path.join(cache, dir, sub, 'chrome-headless-shell'))
  const found = candidates.find((c) => c && fs.existsSync(c))
  if (!found) fail('no Chrome found to draw with: install Google Chrome, or set CHROME_PATH')
  return found
}

function render(ref?: string) {
  const story = loadStory(ref)
  const c = compileStory(story, LIBRARY)
  const reduced = has('reduced')
  const frames: Frame[] = [...(reduced ? c.introReduced : c.intro), ...(reduced ? c.reduced : c.full)]
  const from = Math.max(1, Number(flag('from') ?? 1))
  const to = Math.min(frames.length, Number(flag('to') ?? frames.length))
  const every = Math.max(1, Number(flag('every') ?? Math.ceil((to - from + 1) / 36)))
  const picked: number[] = []
  const intro = (reduced ? c.introReduced : c.intro).length
  // --restart: the end of a telling, then the start of the retelling it jumps back to, frame by frame.
  const restart = has('restart')
  if (restart) {
    const back = c.afterStory === 'loop' ? intro + c.loopStart : intro
    for (let f = Math.max(intro, frames.length - 9); f < frames.length; f++) picked.push(f)
    for (let f = back; f < Math.min(frames.length, back + 9); f++) picked.push(f)
  } else {
    for (let f = from - 1; f < to; f += every) picked.push(f)
    if (picked[picked.length - 1] !== to - 1) picked.push(to - 1)
  }

  const missing = new Set<string>()
  const src = (url: string) => {
    const file = fileFor(url)
    if (!file || !fs.existsSync(file)) {
      missing.add(url)
      return ''
    }
    return pathToFileURL(file).href
  }
  const esc = (s: string) => s.replace(/[&<>"]/g, (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[ch]!)
  const rear = LIBRARY.keeper.rearWork
  const cells = picked.map((f, k) => {
    const fr = frames[f]
    const body = rear[Math.floor((f / FPS) * 4) % rear.length]
    const rings = fr.bubble.rings ?? [fr.bubble.opacity, fr.bubble.opacity]
    const items = fr.items
      .map((i) => `<img class="piece${i.kind === 'mark' ? ' mark' : ''}" src="${src(i.url)}" style="opacity:${i.opacity};z-index:${i.z};transform:${itemTransform(i)}">`)
      .join('')
    const what = (restart && k === 9 ? '↻ retelling: ' : '') + (fr.step === 0 ? 'the bubble opens' : `step ${fr.step}: ${describeStep(LIBRARY, story, story.steps[fr.step - 1])}${fr.phase === 'quiet' ? ' · quiet' : fr.phase === 'clear' ? ' · clearing' : ''}`)
    return `<figure><div class="clip"><div class="stage"><img class="actor" src="${src(body.url)}"><div class="cloud"><svg class="bubble" viewBox="0 0 360 230" style="opacity:${fr.bubble.opacity}"><path d="${bubbleOutline(f, fr.bubble.scale)}"/></svg><div class="ring r1" style="opacity:${rings[0]}"></div><div class="ring r2" style="opacity:${rings[1]}"></div>${items}</div></div></div><figcaption><b>${f + 1}</b> ${esc(what)}</figcaption></figure>`
  })
  if (missing.size) fail(`these pictures are not on disk:\n  ${[...missing].join('\n  ')}`)

  const COLS = 6
  const CELL_W = 285
  const CELL_H = 248 + 34
  const width = COLS * CELL_W + (COLS + 1) * 8
  const height = 44 + Math.ceil(cells.length / COLS) * (CELL_H + 8) + 8
  // The stage copies the studio's BubbleStage (stories.css), drawn at 0.75 size.
  const html = `<!doctype html><meta charset="utf-8"><style>
body{margin:0;background:#0f1d23;font:12px -apple-system,system-ui,sans-serif;color:#e6edf6}
h1{font-size:15px;margin:0;padding:12px 8px 8px}
main{display:grid;grid-template-columns:repeat(${COLS},${CELL_W}px);gap:8px;padding:0 8px 8px}
figure{margin:0;width:${CELL_W}px}
.clip{width:${CELL_W}px;height:248px;overflow:hidden;border-radius:4px}
.stage{position:relative;width:380px;height:330px;overflow:hidden;background:linear-gradient(#24414c 0 73%,#1b333b 73%);transform:scale(.75);transform-origin:top left}
.actor{position:absolute;left:62px;top:250px;width:256px;height:320px;object-fit:contain}
.cloud{position:absolute;left:10px;top:4px;width:360px;height:230px}
.bubble{position:absolute;inset:0;width:360px;height:230px;overflow:visible;filter:drop-shadow(0 5px 0 rgba(9,25,34,.24))}
.bubble path{fill:rgba(246,239,211,.22);stroke:rgba(239,246,245,.84);stroke-width:3;stroke-linejoin:round}
.ring{position:absolute;border:3px solid rgba(239,246,245,.72);border-radius:50%;background:rgba(246,239,211,.16)}
.r1{width:22px;height:18px;left:169px;top:214px}.r2{width:12px;height:10px;left:174px;top:236px}
.piece{position:absolute;left:50%;top:50%;width:140px;height:140px;object-fit:contain;filter:drop-shadow(0 5px 4px rgba(2,10,15,.24))}
.mark{width:92px;height:92px;filter:drop-shadow(0 0 1.5px rgba(255,255,255,.85))}
figcaption{height:30px;padding-top:4px;line-height:1.25;overflow:hidden}
figcaption b{color:#f0c24f}
</style><h1>${esc(story.label)}${reduced ? ' · reduced motion' : ''} · ${restart ? 'the restart: last 9 frames, then the retelling' : `frames ${from}–${to} of ${frames.length}, every ${every}`} · ${c.seconds.toFixed(1)} s · ${playsText(c.tellings)} in 20–30 s</h1><main>${cells.join('')}</main>`

  const out = path.resolve(flag('out') ?? OUT_DIR)
  fs.mkdirSync(out, { recursive: true })
  const base = `${story.id}${reduced ? '-reduced' : ''}${restart ? '-restart' : from > 1 || to < frames.length ? `-${from}-${to}` : ''}`
  const htmlFile = path.join(out, `${base}.html`)
  const png = path.join(out, `${base}.png`)
  fs.writeFileSync(htmlFile, html)
  const run = spawnSync(chrome(), ['--headless', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files', '--force-device-scale-factor=1', `--window-size=${width},${height}`, '--virtual-time-budget=15000', `--screenshot=${png}`, pathToFileURL(htmlFile).href], { encoding: 'utf8' })
  if (!fs.existsSync(png) || run.status !== 0) fail(`Chrome could not draw the sheet:\n${run.stderr}`)
  console.log(`✓ ${picked.length} frames drawn: ${png}`)
}

function create(id?: string) {
  if (!id || !/^[a-z0-9][a-z0-9-]{0,59}$/.test(id)) fail('give the new story an id in lower-case-kebab, e.g. sweep-floor')
  const label = flag('label')
  if (!label) fail('give it a name with --label "Sweeping the floor"')
  const file = path.join(STORIES_DIR, `${id}.json`)
  if (fs.existsSync(file)) fail(`${path.relative(ROOT, file)} already exists`)
  const like = flag('like')
  const base: Story = like
    ? { ...loadStory(like), id, label, notes: `Started from ${like}.` }
    : cleanStory({ schema: STORY_SCHEMA, id, label, appliesTo: { assetId: '', label: '' }, flow: 'left-to-right', cast: { hero: { picture: 'washing-plate', role: 'hero' } }, steps: [{ do: 'arrive', who: 'hero' }, { do: 'settle' }] })!
  fs.writeFileSync(file, JSON.stringify(base, null, 2) + '\n')

  // List it in drafts.ts so the studio and the tests pick it up.
  const name = id.replace(/-([a-z0-9])/g, (_, ch: string) => ch.toUpperCase())
  let ts = fs.readFileSync(DRAFTS_TS, 'utf8')
  const imports = [...ts.matchAll(/^import \w+ from '\.\.\/\.\.\/data\/activity-stories\/stories\/[^']+'\n/gm)]
  const last = imports[imports.length - 1]
  const at = last.index! + last[0].length
  ts = ts.slice(0, at) + `import ${name} from '../../data/activity-stories/stories/${id}.json'\n` + ts.slice(at)
  ts = ts.replace(/(export const STORY_FILES = \{\n(?:  .+\n)*)/, `$1  '${id}': ${name},\n`)
  fs.writeFileSync(DRAFTS_TS, ts)
  console.log(`✓ ${path.relative(ROOT, file)} started and listed in the studio. Edit it, then: npm run stories -- check ${id}`)
}

switch (command) {
  case 'pictures':
    pictures(target)
    break
  case 'list':
    list()
    break
  case 'check':
    check(target)
    break
  case 'render':
    render(target)
    break
  case 'new':
    create(target)
    break
  default:
    console.log(HELP)
    if (command && command !== 'help') process.exit(1)
}
