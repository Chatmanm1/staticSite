const fs = require("fs");
const path = require("path");

const sourceDir = "blogposts";
const outDir = "dist";

fs.mkdirSync(outDir, { recursive: true });

// copy blogposts into dist
fs.cpSync(sourceDir, path.join(outDir, sourceDir), { recursive: true });

const files = fs.readdirSync(sourceDir)
  .filter(f => fs.statSync(path.join(sourceDir, f)).isFile());

const links = files.map(f =>
  `<li><a href="/blogposts/${f}">${f}</a></li>`
).join("\n");

const html = `<!doctype html>
<html>
<body>
<h1>Blog Posts</h1>
<ul>
${links}
</ul>
</body>
</html>`;

fs.writeFileSync(path.join(outDir, "index.html"), html);
