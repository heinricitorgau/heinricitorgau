"""Fail if any GitHub-hosted image or link in README.md no longer resolves.

Every project banner on the profile is served from *another* repository's
`main` branch, so renaming a repo, a branch or an asset breaks this page
silently: GitHub just draws an empty image. This script requests each
github.com / raw.githubusercontent.com URL in the README and lists every
one that does not answer with HTTP 200 after redirects.

Third-party badges (shields.io, Streamlit, Zenodo) are deliberately left
out: they rate-limit CI runners and their outages are not ours to fix.

Usage: python .github/scripts/check_links.py [README.md]
"""
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

HOSTS = ("https://github.com/", "https://raw.githubusercontent.com/")
URL = re.compile(r"https://[^\s\"'<>()\]]+")


def github_urls(text):
    """Return the distinct GitHub URLs in ``text``, in order of appearance.

    >>> github_urls('<img src="https://raw.githubusercontent.com/a/b/main/x.svg"> '
    ...             '[t](https://github.com/a/b) https://img.shields.io/x '
    ...             '[t](https://github.com/a/b)')
    ['https://raw.githubusercontent.com/a/b/main/x.svg', 'https://github.com/a/b']
    """
    seen = []
    for url in URL.findall(text):
        if url.startswith(HOSTS) and url not in seen:
            seen.append(url)
    return seen


def status(url):
    req = urllib.request.Request(url, headers={"User-Agent": "profile-link-check"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except (urllib.error.URLError, TimeoutError) as exc:
        return f"unreachable ({exc})"


def main(path="README.md"):
    urls = github_urls(Path(path).read_text(encoding="utf-8"))
    broken = [(url, code) for url in urls if (code := status(url)) != 200]
    for url, code in broken:
        print(f"BROKEN {code}  {url}")
    print(f"{len(urls) - len(broken)}/{len(urls)} GitHub URLs in {path} resolve")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
