const { chromium } = require("playwright");
const path = require("path");

(async () => {
  const browser = await chromium.launch({ headless: true });
  const targets = [
    "index.html",
    "business/tourism/index.html",
    "column/tourism/index.html",
  ];
  const results = [];
  for (const target of targets) {
    for (const width of [375, 1440]) {
      const page = await browser.newPage({ viewport: { width, height: 900 } });
      const failed = [];
      page.on("response", response => {
        if (response.status() >= 400 && response.url().startsWith("http://127.0.0.1:4173/")) {
          failed.push({ status: response.status(), url: response.url() });
        }
      });
      await page.goto(`http://127.0.0.1:4173/${target}`, { waitUntil: "networkidle" });
      await page.addStyleTag({ content: ".reveal-item{opacity:1!important;transform:none!important}" });
      await page.evaluate(async () => {
        window.scrollTo(0, document.body.scrollHeight);
        await new Promise(resolve => setTimeout(resolve, 800));
      });
      const metrics = await page.evaluate(() => ({
        h1: document.querySelectorAll("h1").length,
        scrollWidth: document.documentElement.scrollWidth,
        clientWidth: document.documentElement.clientWidth,
        brokenImages: [...document.images].filter(image => !image.complete || image.naturalWidth === 0).map(image => image.getAttribute("src")),
        header: Boolean(document.querySelector("header")),
        footer: Boolean(document.querySelector("footer")),
      }));
      results.push({ target, width, failed, ...metrics });
      if (width === 1440) {
        await page.screenshot({
          path: path.join("tools", "qa", `current-${target.replaceAll("/", "-").replace(".html", "")}.png`),
          fullPage: true,
        });
      }
      await page.close();
    }
  }
  await browser.close();
  const failures = results.filter(result =>
    result.failed.length ||
    result.h1 !== 1 ||
    result.scrollWidth > result.clientWidth ||
    result.brokenImages.length ||
    !result.header ||
    !result.footer
  );
  console.log(JSON.stringify({ failures, results }, null, 2));
  process.exit(failures.length ? 1 : 0);
})().catch(error => {
  console.error(error);
  process.exit(1);
});
