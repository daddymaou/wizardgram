# wizardgram static docs

This folder contains a static documentation site for the wizardgram project. It is designed to work as a GitHub Pages project site under `/wizardgram/` and also when opened locally from disk.

## Local preview

From the project root, run:

```bash
python -m http.server 8000
```

Then open:

- http://localhost:8000/
- http://localhost:8000/docs/install.html

## Deploy to GitHub Pages

1. Commit the site files to your repository.
2. In GitHub, open the repository settings.
3. Go to Pages.
4. Set the source to the branch that contains the static site files, or use the GitHub Actions workflow if you prefer automation.
5. Publish the site.

The project uses relative links and includes `.nojekyll` so the site works cleanly when published under a project path such as `/wizardgram/`.

## Add a new page

1. Add the new HTML page in the root or `docs/` folder.
2. Add a matching entry to the manifest in `assets/js/pages.js`.
3. Use the same shell pattern as the existing pages and keep a `noscript` fallback list.
4. Verify the relative links and page titles before publishing.

## Notes

- The site is static HTML, CSS, and vanilla JavaScript only.
- The design uses warm parchment tones, a handwritten display style, and responsive layouts.
- Font files are referenced in `assets/css/tokens.css`; add the matching `.woff2` files to `assets/fonts/` before publishing if you want the self-hosted display typography to render immediately.
