// Entry program for gta6-meme-x-01 ("Post a GTA 6 meme on X").
//
// The entry is the X post named in POST.json; the house reads the post itself
// (its first picture and its text) from X. All this program has to do is hand
// POST.json to the grader: copy it from the bot directory (the repository
// root locally) into the output directory. Before copying, it validates the
// file it is about to hand over — POST.json must be JSON naming one public
// http(s) post address on x.com or twitter.com — and it logs the address it
// submitted, so a bad hand-off fails loudly here instead of at the gate.
//
// Local run (MAKEFUN_BOT_DIR / MAKEFUN_OUTPUT_DIR stand in for /bot and
// /output outside the grader's container):
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const POST_FILE = 'POST.json';

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

// Read and validate the post pointer before anything is copied.
let post: { url?: unknown };
try {
  post = JSON.parse(readFileSync(join(BOT_DIR, POST_FILE), 'utf8'));
} catch (err) {
  fail(`${POST_FILE} is not readable JSON in ${BOT_DIR}: ${(err as Error).message}`);
}

const url = post.url;
if (typeof url !== 'string' || !/^https?:\/\/(x\.com|twitter\.com)\/[^/]+\/status\/\d+/.test(url)) {
  fail(`${POST_FILE} must name one post address like https://x.com/<handle>/status/<id>; got ${JSON.stringify(url)}`);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  copyFileSync(join(BOT_DIR, POST_FILE), join(OUTPUT_DIR, POST_FILE));
} catch (err) {
  fail(`${POST_FILE} could not be copied to ${OUTPUT_DIR}: ${(err as Error).message}`);
}

console.log(`main.ts: handed over ${POST_FILE} naming ${url}`);
