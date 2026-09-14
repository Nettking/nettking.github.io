#!/usr/bin/env python3
"""Offline structural and curated-publication checks; not proof of publication."""
from __future__ import annotations
import json
import re
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "cv.html", "404.html")


class Document(HTMLParser):
    def __init__(self, path: Path):
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.links: list[str] = []
        self.assets: list[str] = []
        self.publications: list[str] = []
        self.h1_count = 0
        self.main_count = 0
        self.language = None
        self.title_found = False
        self.viewport = False
        self.description = False
        self.images: list[dict[str, str | None]] = []
        self.forbidden_tags: list[str] = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if a.get("id"):
            self.ids.append(a["id"])
        if a.get("data-publication-id"):
            self.publications.append(a["data-publication-id"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag in ("script", "img", "source") and a.get("src"):
            self.assets.append(a["src"])
        if tag == "link" and a.get("rel") in ("stylesheet", "icon"):
            self.assets.append(a["href"])
        if tag == "h1":
            self.h1_count += 1
        if tag == "main":
            self.main_count += 1
        if tag == "html":
            self.language = a.get("lang")
        if tag == "title":
            self.title_found = True
        if tag == "meta" and a.get("name") == "viewport":
            self.viewport = True
        if tag == "meta" and a.get("name") == "description":
            self.description = bool(a.get("content"))
        if tag == "img":
            self.images.append(a)
        if tag in ("iframe", "form", "object", "embed"):
            self.forbidden_tags.append(tag)


def local_target(value: str, page: str) -> Path:
    path = unquote(urlsplit(value).path)
    target = ROOT / path.lstrip("/") if path.startswith("/") else ROOT / Path(page).parent / path
    if not path:
        target = ROOT / page
    if target.is_dir():
        target /= "index.html"
    return target.resolve()


class SiteChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.documents = {page: Document(ROOT / page) for page in PAGES}
        cls.registry = json.loads((ROOT / "content/publications.json").read_text(encoding="utf-8"))

    def test_accessible_structure(self):
        for page, doc in self.documents.items():
            with self.subTest(page=page):
                self.assertEqual(doc.language, "en")
                self.assertEqual(doc.h1_count, 1)
                self.assertEqual(doc.main_count, 1)
                self.assertEqual(len(doc.ids), len(set(doc.ids)))
                self.assertTrue(doc.viewport and doc.description and doc.title_found)
                self.assertIn("#main", doc.links)
                self.assertFalse(doc.forbidden_tags)
                for image in doc.images:
                    self.assertIn("alt", image)

    def test_links_assets_and_fragments(self):
        for page, doc in self.documents.items():
            for value in doc.links + doc.assets:
                with self.subTest(page=page, link=value):
                    url = urlsplit(value)
                    if url.scheme or url.netloc:
                        self.assertIn(url.scheme, ("https", "mailto"))
                        continue
                    target = local_target(value, page)
                    self.assertTrue(target.is_relative_to(ROOT))
                    self.assertTrue(target.is_file(), str(target))
                    if url.fragment and target.suffix == ".html":
                        self.assertIn(unquote(url.fragment), Document(target).ids)

    def test_no_remote_dependencies(self):
        for doc in self.documents.values():
            for value in doc.assets:
                self.assertFalse(urlsplit(value).scheme or urlsplit(value).netloc)
        css = (ROOT / "assets/style.css").read_text(encoding="utf-8")
        js = (ROOT / "assets/site.js").read_text(encoding="utf-8")
        self.assertNotIn("@import", css)
        self.assertNotRegex(css, r"url\(\s*['\"]?(?:https?:)?//")
        self.assertNotRegex(js, r"\b(?:fetch|XMLHttpRequest|sendBeacon)\s*\(")
        self.assertFalse((ROOT / ".github/workflows").exists())

    def test_published_allowlist_matches_pages(self):
        publications = self.registry["publications"]
        ids = [pub["id"] for pub in publications]
        self.assertTrue(ids)
        self.assertEqual(len(ids), len(set(ids)))
        for pub in publications:
            self.assertEqual(pub["status"], "published")
            self.assertRegex(pub["doi"], r"^10\.\d{4,9}/\S+$")
            self.assertTrue(pub["publication_evidence"].startswith("https://"))
            self.assertIn("Martin Arthur Andersen", pub["authors"])
            for page in ("index.html", "cv.html"):
                html = (ROOT / page).read_text(encoding="utf-8")
                self.assertIn(pub["title"], html)
                self.assertIn("https://doi.org/" + pub["doi"], html)
                for author in pub["authors"]:
                    self.assertIn(author, html)
            self.assertIn(pub["doi"], (ROOT / "assets/publications.bib").read_text(encoding="utf-8"))
        for page in ("index.html", "cv.html"):
            self.assertCountEqual(ids, self.documents[page].publications)
        for page in PAGES:
            text = (ROOT / page).read_text(encoding="utf-8")
            self.assertNotRegex(text.lower(), r"\b(?:under review|in preparation|forthcoming|submission planned|unpublished manuscript)\b")

    def test_profile_portrait(self):
        portraits = [image for image in self.documents["index.html"].images
                     if image.get("src") == "assets/portrait.webp"]
        self.assertEqual(len(portraits), 1)
        portrait = portraits[0]
        self.assertEqual(portrait["alt"], "Portrait of Martin Arthur Andersen")
        self.assertEqual((portrait["width"], portrait["height"]), ("512", "512"))
        self.assertNotEqual(portrait.get("loading"), "lazy")
        image_bytes = (ROOT / "assets/portrait.webp").read_bytes()
        self.assertEqual(image_bytes[:4], b"RIFF")
        self.assertEqual(image_bytes[8:12], b"WEBP")
        self.assertLess(len(image_bytes), 100_000)
        self.assertIn("assets/portrait.css", self.documents["index.html"].assets)

    def test_approved_background_and_service(self):
        for page in ("index.html", "cv.html"):
            text = (ROOT / page).read_text(encoding="utf-8")
            for expected in (
                "2025–present", "Research Assistant", "2022–2024", "2019–2022",
                "Machine Learning &amp; Cyber-Physical Systems",
                "Computer Security &amp; Cyber-Physical Systems",
                "Faculty of Computer Science, Engineering and Economics (IIØ)",
                "Department of Computer Science and Communication (ITK)",
                "Social committee member", "Student Leader", "2024–2025",
            ):
                with self.subTest(page=page, expected=expected):
                    self.assertIn(expected, text)
            self.assertIn("assets/background.css", self.documents[page].assets)
        cv = (ROOT / "cv.html").read_text(encoding="utf-8")
        for expected in (
            "Fakultet for informasjonsteknologi, ingeniørfag og økonomi",
            "Institutt for informasjonsteknologi og kommunikasjon",
            "Klagenemnda", "Utdanningskvalitetsutvalget", "Sentralt Forskningsutvalg",
            "2018–2021", "Elkjøp Halden", "2015–2016", "Evry",
        ):
            self.assertIn(expected, cv)
        self.assertEqual(cv.count('data-service-id="education-deputy"'), 1)
        self.assertIn("Current · Social committee member", cv)
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("Elkjøp Halden", home)
        self.assertNotIn("Evry", home)
        self.assertFalse(list(ROOT.rglob("*.pdf")), "Do not publish the supplied CV attachment")

    def test_metadata_and_hosting(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        matches = re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', html, re.S)
        self.assertTrue(matches)
        data = json.loads(matches[0])
        self.assertEqual(data["name"], "Martin Arthur Andersen")
        self.assertEqual(data["email"], "mailto:martin.a.andersen@hiof.no")
        self.assertTrue((ROOT / ".nojekyll").exists())
        tree = ElementTree.parse(ROOT / "sitemap.xml")
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locations = [entry.text for entry in tree.findall("s:url/s:loc", ns)]
        self.assertEqual(set(locations), {"https://nettking.github.io/", "https://nettking.github.io/cv.html"})
        self.assertIn("Sitemap: https://nettking.github.io/sitemap.xml", (ROOT / "robots.txt").read_text())


if __name__ == "__main__":
    unittest.main(verbosity=2)
