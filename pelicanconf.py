AUTHOR = "ACBB Canoë-Kayak et SUP"
SITENAME = "ACBB Canoë-Kayak et SUP"
SITESUBTITLE = "Club de canoë-kayak et stand up paddle, Sèvres"
SITEURL = ""

PATH = "content"
STATIC_PATHS = ["images", "files"]

# Site content is authored in Markdown. Raw HTML is used inline for the
# multi-column/CTA/price-table/etc. layout regions the theme's CSS
# expects (see themes/acbb/static/css/theme.css) - standard Markdown has
# no syntax for that, and falling back to raw HTML for it is itself
# standard Markdown practice. `md_in_html` lets **bold**/*em*/[links]
# still work inside a wrapping `<div markdown="1">`.
MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.extra": {},
        "markdown.extensions.md_in_html": {},
    },
    "output_format": "html5",
}

TIMEZONE = "Europe/Paris"
DEFAULT_LANG = "fr"

THEME = "themes/acbb"

DEFAULT_PAGINATION = 10

# The homepage is a real content page (content/pages/accueil.md, saved
# as index.html by its own `Save_as` metadata) rather than the blog
# listing. Move the article index out of the way to /blog/ instead.
INDEX_SAVE_AS = "blog/index.html"
INDEX_URL = "blog/"
ARTICLE_URL = "blog/{slug}.html"
ARTICLE_SAVE_AS = "blog/{slug}.html"

# Year/month archive pages for the blog sidebar's "Archives" links
# (rendered by themes/acbb/templates/period_archives.html).
YEAR_ARCHIVE_SAVE_AS = "blog/{date:%Y}/index.html"
MONTH_ARCHIVE_SAVE_AS = "blog/{date:%Y}/{date:%m}/index.html"

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

# --- Blog sidebar helpers (index.html: "Articles récents" / "Archives") ---
# A static site has no live "now" - RECENT_ARTICLES_SINCE is fixed at build
# time, so the "last 6 months" window reflects whenever the site was last
# generated, same as everything else here (e.g. the Instagram grid).
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

RECENT_ARTICLES_SINCE = datetime.now(ZoneInfo(TIMEZONE)) - timedelta(days=182)

FR_MONTHS = [
    "", "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
]


def month_name(month_number):
    return FR_MONTHS[month_number]


def archive_groups(articles):
    """Group articles by year -> month (most recent first) for the blog
    sidebar's Archives list."""
    years = {}
    for article in articles:
        months = years.setdefault(article.date.year, {})
        months[article.date.month] = months.get(article.date.month, 0) + 1
    groups = []
    for year in sorted(years, reverse=True):
        months = years[year]
        groups.append({
            "year": year,
            "months": [
                {"num": m, "name": month_name(m), "count": months[m]}
                for m in sorted(months, reverse=True)
            ],
        })
    return groups


JINJA_GLOBALS = {"recent_articles_since": RECENT_ARTICLES_SINCE}
JINJA_FILTERS = {"archive_groups": archive_groups, "month_name": month_name}
