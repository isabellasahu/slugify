import unittest

from slugify import slugify, slugify_many


class SlugifyTests(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_multiple_spaces(self):
        self.assertEqual(slugify("Hello   World"), "hello-world")

    def test_leading_trailing_whitespace(self):
        self.assertEqual(slugify("  Hello World  "), "hello-world")

    def test_punctuation_only(self):
        self.assertEqual(slugify("!!!"), "")

    def test_accents(self):
        self.assertEqual(slugify("Café déjà vu"), "cafe-deja-vu")

    def test_uppercase_default_lowered(self):
        self.assertEqual(slugify("HELLO"), "hello")

    def test_no_lower(self):
        self.assertEqual(slugify("Hello World", lower=False), "Hello-World")

    def test_custom_separator(self):
        self.assertEqual(slugify("Hello World", separator="_"), "hello_world")

    def test_separator_in_text_collapses(self):
        self.assertEqual(slugify("a---b"), "a-b")

    def test_collapse_runs_with_custom_separator(self):
        self.assertEqual(slugify("a   b", separator="_"), "a_b")

    def test_non_string_raises_typeerror(self):
        with self.assertRaises(TypeError):
            slugify(123)

    def test_empty_separator_raises(self):
        with self.assertRaises(ValueError):
            slugify("hi", separator="")

    def test_multichar_separator_raises(self):
        with self.assertRaises(ValueError):
            slugify("hi", separator="--")

    def test_non_ascii_separator_raises(self):
        with self.assertRaises(ValueError):
            slugify("hi", separator="–")

    def test_ligature_normalisation(self):
        self.assertEqual(slugify("oﬃce"), "office")

    def test_non_ascii_separator_lowered_with_lower_false(self):
        # '–' is non-ASCII and must be rejected even when lower=False.
        with self.assertRaises(ValueError):
            slugify("hi", separator="–", lower=False)

    def test_slugify_many(self):
        self.assertEqual(
            slugify_many(["Hello World", "Café Déjà Vu"]),
            ["hello-world", "cafe-deja-vu"],
        )

    def test_slugify_many_custom_separator(self):
        self.assertEqual(
            slugify_many(["Hello World", "Foo Bar"], separator="_"),
            ["hello_world", "foo_bar"],
        )

    def test_slugify_many_rejects_non_list(self):
        with self.assertRaises(TypeError):
            slugify_many("not a list")

    def test_slugify_many_rejects_non_string_item(self):
        with self.assertRaises(TypeError):
            slugify_many(["ok", 42])


if __name__ == "__main__":
    unittest.main()
