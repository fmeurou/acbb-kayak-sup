import sys

sys.path.append(".")
from pelicanconf import *  # noqa

# Demo deployment target for validating the GitHub Actions pipeline (see
# .github/workflows/deploy.yml) - a GitHub Pages project site, not the
# club's real domain. Swap back to "https://www.acbb-canoe-kayak.fr" (the
# real production target CLAUDE.md assumes) before this is ever used for
# an actual go-live; a GH Pages project site is served under a
# /acbb-kayak-sup/ subpath, and this codebase's content-authored links/
# images use hardcoded root-absolute paths (e.g. /images/..., /pages/...)
# rather than SITEURL-templated ones, so they'll 404 under that subpath
# regardless of this setting - only the theme's own templated links
# (nav, footer, static assets) resolve correctly here.
SITEURL = "https://fmeurou.github.io/acbb-kayak-sup"
RELATIVE_URLS = False

FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"

DELETE_OUTPUT_DIRECTORY = True
