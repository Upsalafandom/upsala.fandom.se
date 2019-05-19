#!/usr/bin/env python3

import os
import sys
from lxml import etree
import re


URL_RE = re.compile(r"https?://upp?sala\.fandom\.se")
MORE_RE = re.compile(r"<!-- *more *-->\r?")
CLASS_RE = re.compile(r'class="[^"]*"')
EMPTY_ALT_RE = re.compile(r'alt=""')


def clean_content(content):
    content = URL_RE.sub("__FIXME__", content)
    content = MORE_RE.sub("<!-- more -->", content)
    content = CLASS_RE.sub("", content)
    content = EMPTY_ALT_RE.sub("", content)
    return content


namespaces = {
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "wfw": "http://wellformedweb.org/CommentAPI/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "wp": "http://wordpress.org/export/1.2/",
}

root = etree.parse(sys.argv[1])

channel = root.xpath("./channel")[0]

# Get authors
authors = {
    e.xpath("./wp:author_login/text()", namespaces=namespaces)[0]: e.xpath(
        "./wp:author_display_name/text()", namespaces=namespaces
    )[0]
    for e in channel.xpath("./wp:author", namespaces=namespaces)
}
authors.update(
    {
        "anglemark": "Anglemark",
        "wahlbom": "Wahlbom",
        "sten": "Sten",
        "ante": "Ante",
        "kjn": "Karl-Johan",
        "wokka": "Åka",
        "bkhl": "Björn",
        "zrajm": "Zrajm",
        "luna": "Luna",
        "toblo": "Torbjörn",
        "marie": "Marie",
        "nicklas": "Nicklas",
        "autumnfrost": "Nahal",
        "Svensson": "Lennart Svensson",
        "Johan J.": "Johan J.",
        "jesper": "Jesper",
        "Katrin_Enkel": "Katrin",
        "nea": "Nea",
        "Bellis": "Bellis",
        "george": "George",
        "LennartJansson": "Lennart Jansson",
    }
)

# Create output directories.
for d in ("content", "content/blogg"):
    try:
        os.mkdir(d)
    except FileExistsError:
        pass

# Get pages
pages = channel.xpath('./item[wp:post_type = "page"]', namespaces=namespaces)
for page in pages:
    # Extract data
    title = page.xpath("./title/text()")[0]
    slug = page.xpath("./wp:post_name/text()", namespaces=namespaces)[0].replace(
        "-", "_"
    )

    if slug in ("blogg", "riktlinjer"):
        continue

    if slug == "e_postlista":
        slug = "epostlista"

    content = clean_content(
        page.xpath("./content:encoded/text()", namespaces=namespaces)[0].rstrip()
    )

    # Write file
    with open(f"content/sidor/{slug}.md", "w") as f:
        f.write(
            f"""+++
title = "{title}"
path = "{slug}"
+++

{content}
"""
        )
