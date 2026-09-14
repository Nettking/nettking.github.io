# Instructions for this public website

## Non-negotiable publication boundary

Martin has explicitly requested that this site contain **no unpublished work**.

1. Include only public professional biography and verified, formally published research. A repository being public is not evidence that its research may be promoted here.
2. Never add manuscripts in preparation, submissions, work under review, proposals, intended venues, future research plans, private discussions, technical roadmaps, preliminary results, or unapproved project descriptions. Do not name excluded work even to explain that it is excluded.
3. Apply the same boundary to all files, comments, metadata, structured data, attachments, documentation, branches, and commit messages. Hiding an item from navigation does not make it private. Do not commit drafts for later publication.
4. Do not read private email, diaries, or research notes to generate public website content. Do not add private email addresses, telephone numbers, home addresses, travel details, finances, or infrastructure information.
5. Keep publications explicitly curated in `content/publications.json`. Require a publisher or institutional publication record establishing formal publication. A DOI alone is insufficient because preprints and deposits can also have DOIs. Preserve full authorship, correct venue, and publication status.
6. Link an author version only as an alternate version of an already verified published paper. Never list it as a second paper. Do not copy publisher PDFs or third-party photographs without reuse permission.
7. When publication status or disclosure permission is uncertain, omit the item and ask Martin privately. Do not put the question or uncertainty into this public repository.

## Engineering

Keep this a small, dependency-free static site. Do not add hosted CI jobs, repository feeds, tracking, external fonts, embedded social widgets, secrets, or a build framework without an explicit need and owner approval. Preserve accessible navigation, responsive layouts, reduced-motion support, no-JavaScript access, and print styling. Maintain `SOURCES.md` and run `python tests/check_site.py` before publishing. These checks do not replace content review.
