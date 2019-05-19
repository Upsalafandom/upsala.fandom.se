#!/usr/bin/env python3

import os
import sys
from lxml import etree
import re


URL_RE = re.compile(r"https?://upp?sala\.fandom\.se")
MORE_RE = re.compile(r"<!-- *more *-->\r?")
CLASS_RE = re.compile(r'class="[^"]*"')
EMPTY_ALT_RE = re.compile(r'alt=""')
LINK_RE = re.compile(
    r'<a[^>]+href="(?:__FIXME__)?(?:/)?(?P<url>[^"]*[^/])/?"[^>]*>(?P<text>[^<]+)</a>'
)
HAS_IMG_RE = re.compile(r"<img\b")


def clean_content(content):
    content = URL_RE.sub("__FIXME__", content)
    content = MORE_RE.sub("<!-- more -->", content)
    content = CLASS_RE.sub("", content)
    content = EMPTY_ALT_RE.sub("", content)
    content = LINK_RE.sub("[\g<text>](\g<url>)", content)
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

# Get posts
posts = channel.xpath('./item[wp:post_type = "post"]', namespaces=namespaces)
for post in posts:
    # Extract data
    title = post.xpath("./title/text()")[0].replace('"', '\\"')
    slug = post.xpath("./wp:post_name/text()", namespaces=namespaces)[0].replace(
        "-", "_"
    )
    author = post.xpath("./dc:creator/text()", namespaces=namespaces)[0]
    date = post.xpath("./wp:post_date/text()", namespaces=namespaces)[0][:10]
    content = clean_content(
        post.xpath("./content:encoded/text()", namespaces=namespaces)[0]
    )

    categories = {
        e.xpath("./text()")[0]
        for e in post.xpath('./category[@domain="category"]', namespaces=namespaces)
    }
    categories_list = ", ".join(f'"{c}"' for c in sorted(categories))
    tags = {
        e.xpath("./text()")[0]
        for e in post.xpath('./category[@domain="post_tag"]', namespaces=namespaces)
    }
    tag_list = ", ".join(f'"{t}"' for t in sorted(tags))

    if "<img" in content:
        try:
            os.mkdir(f"content/blogg/{slug}")
        except FileExistsError:
            pass
        filename = f"content/blogg/{slug}/index.md"
    else:
        filename = f"content/blogg/{slug}.md"

    # Write file
    with open(filename, "w") as f:
        f.write(
            f"""+++
title = "{title}"
slug = "{slug}"
date = {date}

[taxonomies]
forfattare = ["{authors[author]}"]
kategorier = [{categories_list}]
taggar = [{tag_list}]
+++

{content}
"""
        )
