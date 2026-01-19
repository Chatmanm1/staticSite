const fs = require("fs");
const path = require("path");

const sourceDir = "blogposts";
const partialsDir = "partials";
const outDir = "dist";
const styleFile = "style.css";
const outFile = path.join(outDir, "index.html");

fs.mkdirSync(outDir, { recursive: true });

// --- recursive copy + css fix ---
function copyBlogTree(src, dest, collectedFiles = [], base = "") {
  fs.mkdirSync(dest, { recursive: true });

  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    const relativePath = path.join(base, entry.name);

    if (entry.isDirectory()) {
      copyBlogTree(srcPath, destPath, collectedFiles, relativePath);
    } else {
      let content = fs.readFileSync(srcPath, "utf8");

      // force absolute css
      content = content.replace(
        /<link\s+rel=["']stylesheet["'][^>]*>/gi,
        '<link rel="stylesheet" href="/style.css">'
      );

      fs.writeFileSync(destPath, content);
      collectedFiles.push(relativePath);
    }
  }

  return collectedFiles;
}

// copy blogposts recursively
const blogFiles = copyBlogTree(
  sourceDir,
  path.join(outDir, sourceDir)
);

// copy partials
fs.cpSync(partialsDir, path.join(outDir, partialsDir), { recursive: true });

// copy css
fs.copyFileSync(styleFile, path.join(outDir, styleFile));

// build index links (preserve subfolders)
const links = blogFiles.map(f =>
  `<li><a href="/${sourceDir}/${f}">${f}</a></li>`
).join("\n");

// generate index.html
const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Blog Posts</title>
  <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/style.css">
</head>
<body>

<div id="header"></div>
<div id="recent"></div>

<h1>Blog Posts</h1>
<ul>
${links}
</ul>

<div id="footer"></div>

<script>
fetch('/partials/header.html').then(r=>r.text()).then(h=>header.innerHTML=h);
fetch('/partials/footer.html').then(r=>r.text()).then(h=>footer.innerHTML=h);

</script>

</body>
</html>`;

fs.writeFileSync(outFile, html);

console.log(`Indexed ${blogFiles.length} blog files (recursive).`);
