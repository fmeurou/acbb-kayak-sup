"""Per-category year/month archive pages (e.g. /blog/2026/08/,
/actualites/2026/08/).

Pelican's built-in YEAR_ARCHIVE_SAVE_AS / MONTH_ARCHIVE_SAVE_AS settings
group *all* articles by date regardless of category - fine when the site
has a single article stream, but the "Sorties" blog and the "Actualités"
news section are meant to be two independent streams, each with its own
uncontaminated archive tree. pelicanconf.py leaves those two settings
unset and instead sets CATEGORY_ARCHIVES (category name -> URL prefix);
this generator does the equivalent of Pelican's own period-archive
generation, once per category, reusing the theme's period_archives.html
template.
"""

import calendar
from itertools import groupby
from operator import attrgetter

from pelican import signals
from pelican.generators import Generator


class CategoryPeriodArchivesGenerator(Generator):
    def generate_context(self):
        pass

    def generate_output(self, writer):
        category_prefixes = self.settings.get("CATEGORY_ARCHIVES") or {}
        if not category_prefixes:
            return

        try:
            template = self.get_template("period_archives")
        except Exception:
            template = self.get_template("archives")

        all_articles = self.context.get("articles", [])
        newest_first = self.settings["NEWEST_FIRST_ARCHIVES"]
        relative_urls = self.settings["RELATIVE_URLS"]

        for category_name, prefix in category_prefixes.items():
            articles = [a for a in all_articles if a.category == category_name]
            if not articles:
                continue

            dates = sorted(articles, key=attrgetter("date"), reverse=newest_first)

            for year, group in groupby(dates, key=attrgetter("date.year")):
                self._write_period(
                    writer,
                    template,
                    relative_urls,
                    save_as=f"{prefix}/{year}/index.html",
                    url=f"{prefix}/{year}/",
                    period_num=(year,),
                    period_label=(year,),
                    articles=list(group),
                )

            for (year, month), group in groupby(
                dates, key=attrgetter("date.year", "date.month")
            ):
                self._write_period(
                    writer,
                    template,
                    relative_urls,
                    save_as=f"{prefix}/{year}/{month:02d}/index.html",
                    url=f"{prefix}/{year}/{month:02d}/",
                    period_num=(year, month),
                    period_label=(year, calendar.month_name[month]),
                    articles=list(group),
                )

    def _write_period(
        self,
        writer,
        template,
        relative_urls,
        *,
        save_as,
        url,
        period_num,
        period_label,
        articles,
    ):
        context = self.context.copy()
        context["period"] = period_label
        context["period_num"] = period_num
        writer.write_file(
            save_as,
            template,
            context,
            articles=articles,
            dates=articles,
            template_name="period_archives",
            blog=True,
            url=url,
            relative_urls=relative_urls,
        )


def get_generators(sender):
    return CategoryPeriodArchivesGenerator


def register():
    signals.get_generators.connect(get_generators)
