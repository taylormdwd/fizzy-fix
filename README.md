# Fizzy Fix

A single-page demo website for Fizzy Fix, Arizona's retro mobile dirty soda trailer based in Gilbert, AZ. Owner: Shara.

This is a portfolio demo for a pitch. It replaces a stalled Squarespace "Coming Soon" page.

## Tech stack

- Plain HTML, CSS, vanilla JavaScript (no frameworks)
- Single `index.html`
- Mobile-first responsive (breakpoints: 360px, 768px, 1280px)
- GSAP loaded from CDN for hero animations
- Google Fonts loaded from CDN (Smokum, Rye, IM Fell DW Pica SC, Inter)
- No build step
- Hosted on GitHub Pages

## Run locally

Open `index.html` in any modern browser. That's it.

```
cd fizzy-fix
start index.html
```

Or use a tiny static server if you want clean URLs:

```
npx serve .
```

## Deploy to GitHub Pages

1. Push the `fizzy-fix/` folder to a GitHub repo.
2. In the repo go to **Settings → Pages**.
3. Under "Build and deployment" set Source to **Deploy from a branch**.
4. Pick the `main` branch and the `/` (root) folder. Save.
5. GitHub gives you a live URL like `https://<username>.github.io/<repo>/`.

If you put the site files inside a subfolder (e.g. `fizzy-fix/`), point GitHub Pages at `/fizzy-fix` instead of `/`, or move the files to the repo root.

## Folder layout

```
fizzy-fix/
  index.html
  styles.css
  script.js
  README.md
  images/
    trailer/      hero shots of the pink trailer
    drinks/       drink card photos
    events/       past events gallery
    shara/        owner photos
    mascot/       smiling soda-cup character art
    backgrounds/  gingham, sparkle, ribbon assets
```

Image folders are empty placeholders. The site renders solid color blocks where photos go. HTML comments mark every spot a real photo should be swapped in.

## Next steps for production

- [ ] Drop real trailer hero photo into `images/trailer/`
- [ ] Drop real drink photos into `images/drinks/` (six drinks for spring)
- [ ] Drop real event photos into `images/events/` (eight tiles)
- [ ] Drop real Shara portrait into `images/shara/`
- [ ] Real soda-cup mascot artwork (commissioned)
- [ ] Wire the inquiry form to a real backend — Formspree or a Google Form embed (no Netlify per project rules)
- [ ] Embed real Calendly link on every "Book" CTA
- [ ] Point a custom domain at GitHub Pages (DNS instructions in GitHub Pages docs)
- [ ] Replace placeholder testimonials with real quotes (get permission first)
- [ ] Fill in real pricing for all three packages
- [ ] Add an Instagram feed or static social proof gallery
- [ ] Add OG / Twitter card meta tags + favicon
