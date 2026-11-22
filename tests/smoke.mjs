import { runSmoke, assert } from "./smoke-lib.mjs";

await runSmoke("Essay Pulse", async (page) => {
  assert((await page.title()).includes("Essay Pulse"), "unexpected page title");
  await page.locator("#urlForm").waitFor({ state: "visible" });
  // The SheetJS CDN bundle must load for spreadsheet uploads to work.
  await page.waitForFunction(() => typeof window.XLSX === "object", null, { timeout: 15000 });
  // Load the built-in demo dataset and confirm a ranked board renders.
  await page.click("#demoBoardButton");
  await page.locator("#resultsPanel").waitFor({ state: "visible", timeout: 10000 });
  await page.locator("#boardView").waitFor({ state: "visible" });
  const text = await page.locator("#resultsPanel").innerText();
  assert(text.trim().length > 50, "results panel rendered no content");
});
