#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script builds the presentation by filling the boilerplate with content
"""

import codecs
import configparser
import glob
import re
from itertools import zip_longest
from math import ceil


IGNORED_DOCS = [
    "CHANGELOG.md",
    "README.md",
    "README-remarkjs.md",
    "handout.md",
    "labs.md",
]
"""
IGNORED_DOCS: documents that will never be imported
"""

SLIDE_DIVIDER = "\n---\n"
POINTS_PER_AGENDA_SLIDE = 9
AGENDA_TEMPLATE = """
# Agenda {counter}
{points}

"""


def main():
    """
    Main function, starts the logic based on parameters.
    """
    config = read_config("settings.ini")
    slides = render_slides(read_slides(), config)

    template = read_template("template.html")

    rendered_template = render_metadata(template, config)
    rendered_template = rendered_template.replace("{{ content }}", slides)

    write_file("presentation.html", rendered_template)


def read_config(filename: str):
    "Read the config from `filename` and return it"
    config = configparser.ConfigParser()
    config.read(filename, encoding="utf-8")
    return config


def read_template(filename: str):
    "Read the content of the template at `filename` and return it"
    with open(filename) as file_:
        return file_.read()


def read_slides():
    "Read all slides from the given files"

    def create_stripped_slides(content):
        "Return a list of slides with no leading or trailing whitespace"
        return [slide.strip() for slide in content.split(SLIDE_DIVIDER)]

    slides = []
    for file in sorted(glob.iglob("*.md")):
        if file not in IGNORED_DOCS:
            with open(file, "r", encoding="utf-8") as slide_file:
                content = slide_file.read()

            slides.extend(create_stripped_slides(content))

    if not slides:
        raise RuntimeError(
            "No slides loaded. Please add some slides or adjust IGNORED_DOCS."
        )

    return slides


def render_slides(slides, config: dict) -> list:
    "Render the given files by filling the placeholders"
    agenda = create_agenda(slides)
    print("On our agenda: {}".format(", ".join(agenda)))
    rendered_agenda = render_agenda(agenda)

    combined_slides = SLIDE_DIVIDER.join(slides)

    rendered_slides = render_metadata(combined_slides, config)
    rendered_slides = rendered_slides.replace("{{ agenda }}", rendered_agenda)

    return rendered_slides


def create_agenda(slides):
    "Collect agenda points from all slides"
    agenda = []
    for slide in slides[1:]:  # ignore title slide
        title = get_title(slide)
        if not title:
            continue

        if title not in agenda:
            agenda.append(title)

    return agenda


def get_title(slide):
    "Get the title of a slide"
    match = re.match(
        r"^(class: .*\n+){0,1}#\s+(?P<title>.*)$", slide, flags=re.MULTILINE
    )
    if match:
        title = match.group("title").strip()
        return title

    return None


def render_agenda(agenda: list) -> str:
    "Render slides meant for an agenda"

    if not agenda:
        # Avoid having an empty slide.
        return (
            "Unable to detect agenda. "
            "Please add at least one first-level heading (`# Title`) "
            "or remove the `{{ agenda }}` tag from your slides."
        )

    slide_count = ceil(len(agenda) / POINTS_PER_AGENDA_SLIDE)
    agenda_points_per_slide = chunks(agenda, POINTS_PER_AGENDA_SLIDE)
    counter_template = "{index}/{count}"

    filled_agenda = []
    for index, agenda_points in enumerate(agenda_points_per_slide):
        if slide_count < 2:
            count = ""
        else:
            count = counter_template.format(index=index + 1, count=slide_count)

        topics = ["- %s" % t for t in agenda_points if t is not None]
        points = "\n".join(topics)

        formatted_slide = AGENDA_TEMPLATE.format(counter=count, points=points)
        filled_agenda.append(formatted_slide)

    return SLIDE_DIVIDER.join(filled_agenda)


def chunks(iterable, count):
    "Collect data into fixed-length chunks or blocks"
    # chunks('ABCDEFG', 3) --> ABC DEF Gxx"
    args = [iter(iterable)] * count
    return zip_longest(*args)


def render_metadata(slides: str, metadata: dict) -> str:
    "Fill the placeholders in a slide with real values"
    rendered = slides.replace("{{ title }}", metadata["meta"]["title"])
    customer = metadata["meta"].get("customer", "")
    rendered = rendered.replace("{{ customer }}", customer)
    rendered = rendered.replace("{{ ratio }}", metadata["layout"]["ratio"])

    if customer:
        slide_format = f"%current% | %total% - KOPIE: {customer}"
    else:
        slide_format = "%current% | %total%"

    rendered = rendered.replace("{{ slideNumberFormat }}", slide_format)

    return rendered


def write_file(filename, content):
    "Write the `content` to `filename`"
    with codecs.open(filename, "w", "utf-8") as file_:
        file_.write(content)


if __name__ == "__main__":
    main()
