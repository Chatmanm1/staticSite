const fs = require("fs");
const path = require("path");

const sourceDir = "blogposts";      // source blogposts
const partialsDir = "partials";     // header/footer/recent
const outDir = "dist";              // output folder
const styleFile = "style.css";      // main CSS
const outFile = path.join(outDir, "index.html");

// 1. Ensure dist folder exists
fs.mkdirSync(outDir, { recursive: true });

// 2. Copy blogposts and fix CSS link
fs.mkdirSync(path.join(outDir, sourceDir), { recursive: true });
const files = fs.readdirSync(sourceDir)
  .filter(f => fs.statSync(path.join(sourceDir, f)).isFile());

files.forEach(file => {
  const content = fs.readFileSync(path.join(sourceDir, file), "utf8");

  // Replace or inject link to /style.css
  const fixedContent = content.replace(
    /<link\s+rel=["']stylesheet["'][^>]*>/i,
    '<link rel="stylesheet" href="/style.css">'
  );

  fs.writeFileSync(path.join(outDir, sourceDir, file), fixedContent);
});

// 3. Copy partials folder
fs.cpSync(partialsDir, path.join(outDir, partialsDir), { recursive: true });

// 4. Copy style.css to dist/
fs.copyFileSync(styleFile, path.join(outDir, styleFile));

// 5. Generate blog list for index.html
const links = files.map(f =>
  `<li><a href="/${sourceDir}/${f}">${f}</a></li>`
).join("\n");

// 6. Generate index.html with header/footer/recent scripts
const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Blog Posts</title>
  <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/style.css" />
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
    fetch('/partials/header.html').then(r=>r.text()).then(html=>document.getElementById('header').innerHTML=html);
    fetch('/partials/footer.html').then(r=>r.text()).then(html=>document.getElementById('footer').innerHTML=html);
      </script>

</body>
</html>`;

// 7. Write index.html
fs.writeFileSync(outFile, html);

console.log(`Generated index.html and fixed ${files.length} blogposts with CSS links.`);
