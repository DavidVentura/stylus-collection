import re
import json
from dataclasses import dataclass
from urllib.parse import urlparse
from pathlib import Path

from browser import setup_driver, screenshot_with_styles

meta = re.compile(r'@-moz-document (?P<match_type>[a-z-]+)\("(?P<url>[^"]+)"\) {')


@dataclass(frozen=True)
class Entry:
    match_type: str
    url: str
    source: str
    domain: str


def parse_stylus_entry(entry: str) -> Entry:
    match_type = None
    url = None
    found_meta = False
    source_lines = []
    for line in entry.strip().splitlines():
        line = line.strip()
        if line.startswith("@-moz-document"):
            matches = meta.match(line)
            assert matches is not None, line
            url = matches.group("url")
            match_type = matches.group("match_type")
            found_meta = True
            continue
        if not found_meta:
            continue
        source_lines.append(line)
    assert url
    assert match_type
    assert source_lines[-1] == "}"  # css closing
    source_lines = source_lines[:-1]

    if match_type == "domain":
        url = f"https://{url}"
    domain = urlparse(url).netloc
    return Entry(match_type=match_type, url=url, source="\n".join(source_lines), domain=domain)


def read_stylus_exports(path: Path) -> list[Entry]:
    with path.open() as fd:
        entries = json.load(fd)
    ret = []
    seen_domains = set()
    for entry in entries:
        # why are settings at the same level as items..
        if "settings" in entry:
            continue
        if not entry['enabled']:
            continue
        parsed = parse_stylus_entry(entry["sourceCode"])
        if parsed.domain in seen_domains:
            raise ValueError(f"Duplicated domain {parsed.domain}")
        seen_domains.add(parsed.domain)
        ret.append(parsed)
    return ret


url_to_screenshot = {
    "airbus-seclab.github.io": "https://airbus-seclab.github.io/qemu_blog/pci.html",
    "airs.com": "",
    "claude.ai": "",
    "github.com": "https://github.com/DavidVentura/cam-reverse",
    "kubernetes.io": "https://kubernetes.io/docs/concepts/architecture/controller/",
    "medium.com": "",
    "news.ycombinator.com": "",
    "secure.runescape.com": "https://secure.runescape.com/m=news/colosseum-npc-clickboxes--more?oldschool=1",
    "stackoverflow.com": "https://stackoverflow.com/questions/35741814/how-does-builtin-clear-cache-work",
    "www.apollographql.com": "https://www.apollographql.com/docs/apollo-server/workflow/generate-types/",
    "www.crummy.com": "https://www.crummy.com/software/BeautifulSoup/bs4/doc/",
    "xillybus.com": "https://xillybus.com/tutorials/pci-express-tlp-pcie-primer-tutorial-guide-1",
}

if __name__ == "__main__":
    # main(url, css_to_inject)
    entries = read_stylus_exports(Path("/home/david/Downloads/stylus-2024-08-29.json"))

    driver = setup_driver()
    try:
        for entry in entries:
            example_url = url_to_screenshot[entry.domain]
            if not example_url:
                continue
            screenshot_with_styles(driver, example_url, entry.source, f"screenshots/{entry.domain}")
    finally:
        driver.quit()
