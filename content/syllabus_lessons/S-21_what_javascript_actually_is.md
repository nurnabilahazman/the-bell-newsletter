# What is JavaScript

## The idea
Think of a room in a house. The walls and doors are the structure, that's HTML. The paint and furniture are the decoration, that's CSS. But when you press the light switch, something happens. That's the wiring behind the wall, waiting for you to do something and then reacting.

**JavaScript** is the wiring of a web page. It's a programming language, like Python, but it runs inside your web browser. It waits for things you do, like a click or a key press, and responds straight away, without reloading the page. Something you do on the page is called an **event**.

## The project: Add a working copy-button to the About Me page
We'll add a button to the About Me page that copies your email address with one click. It's the light switch idea exactly: the button is the switch, and JavaScript is the wiring that does the copying when it's pressed. Every tool on this site uses the same pattern for its copy buttons.

## Building it
Add these lines to `about.html`, just before the closing `</body>` tag:
```html
<p>Email me: nabilah@example.com</p>
<button id="copy-btn">Copy my email</button>

<script>
  const button = document.getElementById("copy-btn");

  button.addEventListener("click", function () {
    navigator.clipboard.writeText("nabilah@example.com");
    button.textContent = "Copied!";
  });
</script>
```
Here is what each part does:
1. `<button id="copy-btn">` is an ordinary HTML button. The `id` gives it a unique name so JavaScript can find it.
2. `<script>` marks where the JavaScript starts. The browser runs what's inside it.
3. `const button = document.getElementById("copy-btn");` finds the button by its `id` and stores it in a variable called `button`. `const` is how JavaScript creates a variable that won't be swapped for something else, a bit like `button = ...` in Python.
4. `button.addEventListener("click", function () { ... });` connects the wiring: "when this button is clicked, run the code inside the curly brackets". The code inside is a function, the JavaScript version of a Python `def`.
5. `navigator.clipboard.writeText("nabilah@example.com");` puts the email onto your clipboard, ready to paste.
6. `button.textContent = "Copied!";` changes the button's label, so you can see it worked. No page reload needed.

JavaScript looks different from Python: lines end with `;`, and blocks use `{ }` instead of indentation. The ideas, variables, functions and responding to events, are the same ones you already know.

## Why this matters
Every interactive thing on a website, a copy button, a form that checks your input, a menu that opens, is JavaScript. It's what turns a page you read into a page you use.

## The mistake beginners make here
The classic slip is putting the `<script>` above the button. The browser reads the page top to bottom, so the script runs before the button exists. `getElementById` finds nothing, and the browser's console shows `Cannot read properties of null (reading 'addEventListener')`. Nothing happens when you click. Keep your `<script>` at the bottom of the `<body>`, after the HTML it uses. Try it below: move the script above the button and look at the browser console line.

[[widget:script-order]]

## What's next
Next, we'll learn about **secrets and environment variables**: how to keep passwords and API keys out of your code, so they never end up online.
