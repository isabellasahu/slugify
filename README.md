# slugify

A tiny, dependency-free Python library that turns arbitrary text into URL-safe slugs.

## Usage

```python
from slugify import slugify, slugify_many

slugify("Café déjà vu!")          # -> "cafe-deja-vu"
slugify("Hello World", separator="_")   # -> "hello_world"
slugify_many(["A B", "Café"])     # -> ["a-b", "cafe"]
```

## Why

The standard library does not ship with a slug function, and pulling in a
third-party package for three lines of normalisation is overkill when you
already control the environment. This library exists to cover the common
case — lowercase, strip accents, collapse punctuation — without adding a
dependency to a minimal container.

The trade-off: this is opinionated and deliberately limited. It always
NFKD-normalises and strips diacritics, so `É` becomes `e` rather than
`E`. Use something heavier if you need locale-aware transliteration or
need to preserve case by default.

## Edge cases

A title that is pure punctuation (`!!!`) yields an empty string, not a
stray dash. Leading and trailing separators are stripped. The separator
must be a single ASCII character; a multi-character or non-ASCII
separator raises `ValueError` because the normalisation pipeline would
otherwise mangle it silently.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

## Limitations

Values are coerced to floats, so very large integers lose precision. If you need
exact integer aggregates over a window, this is the wrong tool.

