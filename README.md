# Martin Arthur Andersen — personal academic website

Static personal website for **Martin Arthur Andersen**, PhD Research Fellow at Østfold University College.

**Website:** https://nettking.github.io/

## Content boundary

**Do not add unpublished work.** This applies to every tracked file, not only visible pages: HTML comments, metadata, structured data, citations, attachments, documentation, and commit messages are public too. Do not import research repositories or automatically populate a projects/publications feed.

Only verified, formally published research is listed. An author-hosted version may be linked when it is the counterpart of a verified published paper, not as a separate publication. A public repository, submitted manuscript, acceptance notice, or standalone preprint is not sufficient clearance. Keep private contact details and personal information out.

Read [AGENTS.md](AGENTS.md) before editing. Public-source provenance is in [SOURCES.md](SOURCES.md). The reviewed publication allowlist is [content/publications.json](content/publications.json).

## Structure

- `index.html`: profile, research interests, published research, education, service, contact.
- `cv.html`: short academic CV with browser print / save-as-PDF support.
- `assets/`: local CSS, progressive-enhancement JavaScript, monogram favicon, and publication BibTeX.
- `404.html`, `robots.txt`, `sitemap.xml`, `.nojekyll`: static hosting and discovery.
- `tests/check_site.py`: dependency-free structural and publication-consistency checks.

No build step, package manager, external font service, analytics, tracking cookie, third-party embed, or custom Actions workflow is required. The only stored browser preference is the selected light/dark theme (`ma-theme` in local storage). External sites are contacted only when visitors follow links.

## Preview and check

From this directory, with Python 3:

```sh
python tests/check_site.py
python -m http.server 8000 --bind 127.0.0.1
```

Open `http://localhost:8000`. Stop the local server with Ctrl+C. The main page also opens directly from disk; clipboard enhancement requires a secure browser context, such as localhost or HTTPS.

## GitHub Pages

Publish the existing `main` branch, folder `/(root)`, using **Settings → Pages → Build and deployment → Deploy from a branch**. `.nojekyll` keeps the source as plain static files. GitHub manages its standard Pages deployment; this repository adds no custom runner jobs or CI workflow.

Official instructions: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## Maintenance

Update the relevant HTML and, for publications, the reviewed JSON allowlist and BibTeX together. Preserve author order, venue, DOI, and the distinction between conference and companion proceedings. Record the public source and review date in `SOURCES.md`. Update the CV date and sitemap only when their content changes. Run the checks and visually review desktop, mobile, keyboard navigation, dark mode, and print layout before publishing.

Automated checks test structure and consistency, **not** whether a research contribution is genuinely published or whether new text is safe to disclose. Human source review remains necessary. Do not store rejected or excluded research items in this repository.

The page uses a typographic design; no third-party portrait or institutional logo has been copied. Published papers are linked rather than redistributed.
