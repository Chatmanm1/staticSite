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
<html lang="en">
<head>
  <div id="header"></div>
 <script>
    // Load header
    fetch('/partials/header.html')
      .then(res => res.text())
      .then(html => document.getElementById('header').innerHTML = html);

    // Load footer
    fetch('/partials/footer.html')
      .then(res => res.text())
      .then(html => document.getElementById('footer').innerHTML = html);
  </script>
  <script>
  // Load recent
    fetch('/partials/Recent.html')
      .then(res => res.text())
      .then(html => document.getElementById('recent').innerHTML = html);
  </script>
  <meta charset="UTF-8" />
  <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://matchamakes.net/style.css" />
</head>

<body>
<h1>Blog Posts</h1>
<ul>
${links}
</ul>
<!-- 100% privacy-first analytics -->
<script async src="https://scripts.simpleanalyticscdn.com/latest.js"></script>

</body>

  <!-- Footer -->
  <div id="footer"></div>
</html>`;

fs.writeFileSync(path.join(outDir, "index.html"), html);
