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

# Articles live in two independent content streams that share the same
# Pelican `Article` machinery but must not mix: content/blog/ (Category:
# Sorties, the pre-existing "Blog" section) and content/actualites/
# (Category: Actualités, the news section). `{path}` resolves to each
# article's source subdirectory, so the URL prefix always matches the
# directory it was authored in without hardcoding either one here.
# `path` metadata defaults to the full relative *file* path (dir + name),
# not just the directory - PATH_METADATA overrides it to the top-level
# content subdirectory only (e.g. "blog", "actualites"). Pelican applies
# PATH_METADATA to every file it reads, including STATIC_PATHS content
# (content/images/, content/files/) - the pattern is scoped to just the
# two article directories so it doesn't also rewrite `path` for static
# assets (which would collapse them all to output/images, output/files).
PATH_METADATA = r"(?P<path>blog|actualites)/.*"
ARTICLE_URL = "{path}/{slug}.html"
ARTICLE_SAVE_AS = "{path}/{slug}.html"

# Pelican's own YEAR_ARCHIVE_SAVE_AS/MONTH_ARCHIVE_SAVE_AS group *all*
# articles by date regardless of category, which would mix Sorties and
# Actualités into one archive tree. Deliberately left unset - the
# category_period_archives plugin (see plugins/) generates a separate,
# category-scoped year/month archive tree for each entry below instead.
CATEGORY_ARCHIVES = {
    "Sorties": "blog",
    "Actualités": "actualites",
}
PLUGIN_PATHS = ["plugins"]
PLUGINS = ["category_period_archives"]

# The Actualités index (like the blog's, listing its own articles plus
# a "this month" / archive-tree sidebar) is a template-driven listing
# page, not a Pelican Page, same mechanism as the built-in "index".
DIRECT_TEMPLATES = ["index", "tags", "categories", "authors", "archives", "actualites"]
ACTUALITES_SAVE_AS = "actualites/index.html"
ACTUALITES_URL = "actualites/"

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

# --- Blog/Actualités sidebar helpers ---
# A static site has no live "now" - these are fixed at build time, so
# "recent"/"this month" reflect whenever the site was last generated,
# same as everything else here (e.g. the Instagram grid).
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

BUILD_NOW = datetime.now(ZoneInfo(TIMEZONE))
RECENT_ARTICLES_SINCE = BUILD_NOW - timedelta(days=182)


def by_category(articles, category_name):
    """Filter a (multi-category) article list down to one category - used
    by the Actualités templates, which otherwise share the same global
    `articles`/`dates` context as the Sorties blog."""
    return [a for a in articles if a.category == category_name]

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


JINJA_GLOBALS = {
    "recent_articles_since": RECENT_ARTICLES_SINCE,
    "build_now": BUILD_NOW,
}
JINJA_FILTERS = {
    "archive_groups": archive_groups,
    "month_name": month_name,
    "by_category": by_category,
}
