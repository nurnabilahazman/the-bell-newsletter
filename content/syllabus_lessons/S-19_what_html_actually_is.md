# What is HTML

## The idea
Think of a Word document before you style it. You've marked which line is the title, which lines are paragraphs, and which lines are bullet points. Nothing is coloured yet, but the structure is clear: what each piece of text *is*.

**HTML**, short for HyperText Markup Language, does exactly that for web pages. It's not a programming language like Python; it doesn't calculate anything. It's a way of labelling content so the browser knows what each part is. The labels are called **tags**, written in angle brackets like `<h1>`. Most tags come in pairs: an opening tag like `<p>` and a closing tag like `</p>`, with the content in between.

## The project: Build a one-page 'About Me' site
We'll build a simple About Me page with a heading, a paragraph, a bullet list and a link. It's the unstyled Word document idea: we only label what each piece is. Making it look nice comes next lesson.

## Building it
Save this in a file called `about.html`, then double click the file to open it in your browser:
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>About Me</title>
  </head>
  <body>
    <h1>Hi, I'm Nabilah</h1>
    <p>I work in finance and I'm learning to code.</p>
    <ul>
      <li>Excel automation</li>
      <li>Python</li>
    </ul>
    <a href="https://www.linkedin.com">Find me on LinkedIn</a>
  </body>
</html>
```
Here is what each part does:
1. `<!DOCTYPE html>` tells the browser "this is a modern HTML page". It always goes on the very first line.
2. `<html lang="en">` wraps the whole page. `lang="en"` says the page is in English, which helps screen readers.
3. `<head>` holds information *about* the page that isn't shown in the page itself. `<meta charset="UTF-8">` makes sure every character, including symbols like RM or é, displays correctly. `<title>` sets the text on the browser tab.
4. `<body>` holds everything you actually see.
5. `<h1>` is the main heading. `<p>` is a paragraph.
6. `<ul>` starts a bullet list, and each `<li>` is one item in it ("list item").
7. `<a href="...">` makes a link. `href` holds the address it goes to, and the text between the tags is what people click.

Notice how tags sit inside other tags, like boxes in boxes. `<li>` sits inside `<ul>`, which sits inside `<body>`. Indenting each level makes that easy to see.

Change the words below and watch the real page update. Only the content changes; the tags stay the same:

[[widget:about-preview]]

## Why this matters
Every web page, including every tool on this site, is HTML underneath. Knowing the structure lets you read and fix pages, and it's the base for the styling (CSS) and interaction (JavaScript) in the next two lessons.

## The mistake beginners make here
The common slip is forgetting a closing tag. Browsers try to guess where you meant it to end, and they often guess wrong. Leave out `</a>` and everything after the link can turn into part of the link. The page doesn't crash, it just looks broken in confusing ways. Every time you open a tag that needs closing, write the closing tag straight away, then fill in the middle.

## What's next
Next, we'll learn about **CSS**, which controls how the page looks: colours, fonts, spacing and layout.
