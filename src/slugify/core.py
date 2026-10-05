import re
import unicodedata

__all__ = ["slugify", "slugify_many"]

_RE_NON_SLUG = re.compile(r"[^a-zA-Z0-9]+")
_RE_DASHES = re.compile(r"-+")


def _strip_accents(text: str) -> str:
    """Return *text* with combining marks removed.

    NFKD decomposition splits letters from their diacritics so that
    `unicodedata.combining` can isolate and drop the combining marks.
    This is deliberately lossy: `é` becomes `e`, not `e-acute`.
    Pre-composed ligatures such as `ﬁ` are folded to `fi`, which is
    the desired behaviour for URL slugs.
    """
    return "".join(
        ch for ch in unicodedata.normalize("NFKD", text)
        if not unicodedata.combining(ch)
    )


def slugify(text: str, separator: str = "-", lower: bool = True) -> str:
    """Return a URL-safe slug derived from *text*.

    Parameters
    ----------
    text:
        Arbitrary string. ``None`` is rejected to keep the return type
        predictably ``str``.
    separator:
        Joiner between slug tokens. Must be ASCII so that it survives
        the strip-accents pass unchanged and does not itself get
        collapsed.
    lower:
        When True (the default) the result is lower-cased.

    Edge cases
    ----------
    * Whitespace, punctuation and control characters collapse to the
      separator.
    * Leading and trailing separators are removed, so a title that is
      pure punctuation yields an empty string rather than a stray dash.
    * A non-ASCII separator raises ``ValueError`` because the
      normalisation pipeline would strip its accents, silently
      changing the caller's chosen token.
    """
    if not isinstance(text, str):
        raise TypeError("slugify() requires a str, got %s" % type(text).__name__)
    if not isinstance(separator, str) or not separator:
        raise ValueError("separator must be a non-empty str")
    if not separator.isascii():
        raise ValueError("separator must be ASCII; got %r" % separator)
    if len(separator) > 1:
        raise ValueError("separator must be a single character; got %r" % separator)
    if lower:
        text = text.lower()
        # The separator is ASCII, so lower-casing it is a no-op; we do
        # not re-lower it to avoid shadowing a caller-provided symbol.
    else:
        separator = separator.lower()
    text = _strip_accents(text)
    text = _RE_NON_SLUG.sub(separator, text)
    text = _RE_DASHES.sub(separator, text)
    return text.strip(separator)


def slugify_many(texts, separator: str = "-", lower: bool = True):
    """Return a list of slugs for every string in *texts*.

    Convenience helper so callers do not need to repeat keyword
    arguments across a comprehension. Non-string items raise
    ``TypeError``, matching :func:`slugify`.
    """
    if not isinstance(texts, (list, tuple)):
        raise TypeError("texts must be a list or tuple")
    return [slugify(t, separator=separator, lower=lower) for t in texts]
