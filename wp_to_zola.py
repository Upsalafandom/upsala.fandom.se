#!/usr/bin/env python3

import sys
from lxml import etree
import re


URL_RE = re.compile("https?://upp?sala\.fandom\.se")

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
    content = URL_RE.sub(
        "__FIXME__", post.xpath("./content:encoded/text()", namespaces=namespaces)[0]
    )
    categories = {
        e.xpath("./text()")[0]
        for e in post.xpath('./category[@domain="category"]', namespaces=namespaces)
    }
    categories_list = ", ".join(f'"{c}"' for c in categories)
    tags = {
        e.xpath("./text()")[0]
        for e in post.xpath('./category[@domain="post_tag"]', namespaces=namespaces)
    }
    tag_list = ", ".join(f'"{t}"' for t in tags)

    # Write file
    with open(f"content/blogg/{slug}.md", "w") as f:
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

    content = URL_RE.sub(
        "__FIXME__",
        page.xpath("./content:encoded/text()", namespaces=namespaces)[0].rstrip(),
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
