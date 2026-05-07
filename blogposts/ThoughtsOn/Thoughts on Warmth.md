
<html lang="en">
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
  <meta charset="UTF-8" />
  <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://matchamakes.net/style.css" />
  <meta charset="UTF-8">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

</head>
<body>
 <div id="markdown-content" style="display:none;">

# Thoughts on Warmth.

One always seeks it. 
Saves lives, and gives it meaning
Physical and Love


[Thoughts On Main](https://matchamakes.net/blogposts/thoughtson/thoughtsonmain)

</div>

  <div id="rendered"></div>


  
<!-- markdown rendering-->
 <script>
    const md = document.getElementById('markdown-content').innerText;
    document.getElementById('rendered').innerHTML = marked.parse(md);
  </script>
<!-- 100% privacy-first analytics -->
<script async src="https://scripts.simpleanalyticscdn.com/latest.js"></script>
</body>
  <!-- Footer -->
  <div id="footer"></div>
</html>