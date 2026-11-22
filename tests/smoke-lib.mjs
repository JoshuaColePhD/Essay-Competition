// Headless browser smoke test: serve the repo root, load index.html, fail on
// uncaught page errors or console errors, then run page-specific checks.
import http from "node:http";
import { readFile } from "node:fs/promises";
import { extname, join, normalize } from "node:path";
import { chromium } from "playwright";

const ROOT = process.cwd();
const TYPES = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".png": "image/png", ".svg": "image/svg+xml", ".json": "application/json" };

export async function runSmoke(name, checks) {
  const server = http.createServer(async (req, res) => {
    const path = normalize(decodeURIComponent(new URL(req.url, "http://x").pathname)).replace(/^\/+/, "") || "index.html";
    try {
      const body = await readFile(join(ROOT, path));
      res.writeHead(200, { "content-type": TYPES[extname(path)] ?? "application/octet-stream" });
      res.end(body);
    } catch {
      res.writeHead(404).end();
    }
  });
  await new Promise((r) => server.listen(0, "127.0.0.1", r));
  const url = `http://127.0.0.1:${server.address().port}/index.html`;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(`pageerror: ${e.message}`));
  page.on("console", (m) => {
    if (m.type() === "error" && !/favicon/i.test(m.text())) errors.push(`console: ${m.text()}`);
  });
  let failed = false;
  try {
    await page.goto(url, { waitUntil: "load" });
    await checks(page);
    if (errors.length) throw new Error(`Browser errors:\n${errors.join("\n")}`);
    console.log(`✅ ${name} smoke test passed`);
  } catch (e) {
    failed = true;
    console.error(`❌ ${name} smoke test failed: ${e.message}`);
  } finally {
    await browser.close();
    server.close();
  }
  process.exit(failed ? 1 : 0);
}

export function assert(cond, msg) {
  if (!cond) throw new Error(msg);
}
