# What is CSS

## The idea
Go back to the Word document from last lesson, the one where you'd only marked what each line is: title, paragraph, bullet list. Now you open the styles panel. You decide every title is navy and bold, the page has a cream background, and the text sits in a neat column down the middle. You haven't changed a single word. You've only changed how it looks.

That's **CSS**, short for Cascading Style Sheets. HTML says what each part of the page *is*. CSS says how it *looks*: colours, fonts, sizes, spacing, and **layout**, meaning where things sit on the page. A piece of CSS is a set of **rules**. Each rule picks some HTML tags and says how they should look.

## The project: Style the About Me page in Bell brand colors
We'll take the About Me page from lesson 19 and give it The Bell's brand: a cream background, navy text, gold accents, and a tidy centred column. Exactly like the styles panel, the HTML content stays the same. We only add CSS.

## Building it
Add a `<style>` block inside the `<head>` of your `about.html`, so the head looks like this:
```html
<head>
  <meta charset="UTF-8">
  <title>About Me</title>
  <style>
    body {
      background-color: #F5F0E8;
      color: #1A1A2E;
      font-family: Arial, sans-serif;
      max-width: 600px;
      margin: 0 auto;
      padding: 24px;
    }
    h1 {
      border-bottom: 3px solid #C9A84C;
    }
  </style>
</head>
```
Here is what each part does:
1. `<style>` holds your CSS rules. Putting it in the `<head>` applies them to the whole page.
2. `body { ... }` is a rule. The word before the curly brackets, `body`, is the **selector**: it picks which tags the rule applies to. Each line inside is a **property** and a **value**, ending with a semicolon.
3. `background-color: #F5F0E8;` sets the cream background. Colours are written as a `#` followed by six characters, called a hex code.
4. `color: #1A1A2E;` makes the text navy. Navy on cream is very easy to read.
5. `font-family: Arial, sans-serif;` uses Arial, or a similar plain font if Arial isn't available.
6. `max-width: 600px;` and `margin: 0 auto;` are layout. They stop the text stretching across a wide screen, and centre the column. `padding: 24px;` adds breathing room inside it.
7. `h1 { border-bottom: 3px solid #C9A84C; }` puts a gold line under the main heading.

Why is gold a line and not the text colour? Gold on cream is hard to read, because the two colours are too close in brightness. Using gold for accents and navy for words keeps the brand and keeps it readable.

Toggle one change at a time and watch the real page. The first shows the typo from the mistake section below; the second switches the layout on and off:

[[widget:css-preview]]

## Why this matters
Change one rule and every matching tag on the page updates. That's how the whole Bell site keeps one consistent look: shared CSS rules, not hand-coloured pages. The same idea, one rule applied everywhere, is why Excel cell styles beat formatting cells one by one.

## The mistake beginners make here
The sneaky slip is a typo. CSS doesn't show an error. If you write `colour: #1A1A2E;` (British spelling), the browser quietly ignores that line and moves on. Your text just stays black and you're left wondering why. A missing semicolon is sneakier still: the line runs into the next one, and the browser ignores both. When a style doesn't apply, check the spelling of the property first. CSS uses American spelling: `color`, `center`.

## What's next
Next, we'll learn about **JavaScript**, which makes a page respond when you click or type, like a copy button that works without reloading the page.
