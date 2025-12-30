const fs = require("fs");
const path = require("path");

const sourceDir = "blogposts";      // folder with blog files
const partialsDir = "partials";     // folder with header/footer/recent
const outDir = "dist";              // output folder
const outFile = path.join(outDir, "index.html");

// 1. Create dist folder
fs.mkdirSync(outDir, { recursive: true });

// 2. Copy blogposts folder
fs.cpSync(sourceDir, path.join(outDir, sourceDir), { recursive: true });

// 3. Copy partials folder
fs.cpSync(partialsDir, path.join(outDir, partialsDir), { recursive: true });

// 4. Generate blog list
const files = fs.readdirSync(sourceDir)
  .filter(f => fs.statSync(path.join(sourceDir, f)).isFile());

const links = files.map(f =>
  `<li><a href="/${sourceDir}/${f}">${f}</a></li>`
).join("\n");

// 5. Generate full HTML
const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Blog Posts</title>
  <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://matchamakes.net/style.css" />
</head>
<body>

  <div id="header"></div>


  <h1>Blog Posts</h1>
  <ul>
    ${links}
  </ul>

  <div id="footer"></div>

  <script>
    fetch('/partials/header.html').then(r=>r.text()).then(html=>document.getElementById('header').innerHTML=html);
    fetch('/partials/footer.html').then(r=>r.text()).then(html=>document.getElementById('footer').innerHTML=html);
    fetch('/partials/Recent.html').then(r=>r.text()).then(html=>document.getElementById('recent').innerHTML=html);
  </script>

</body>
</html>`;

// 6. Write index.html
fs.writeFileSync(outFile, html);

console.log(`Generated index.html with ${files.length} blogposts.`);
