import unittest

from pwcheck import check, entropy_bits, has_repeats, has_sequence


class TestPwcheck(unittest.TestCase):
    def test_common_password_is_zero(self):
        score, label, _ = check("password")
        self.assertEqual(score, 0)
        self.assertEqual(label, "Very weak")

    def test_empty_password(self):
        score, _, _ = check("")
        self.assertEqual(score, 0)

    def test_strong_password(self):
        score, _, tips = check("t7#Kq!9vLm2$Zx8p")
        self.assertGreaterEqual(score, 80)
        self.assertEqual(tips, [])

    def test_longer_is_better(self):
        self.assertGreater(entropy_bits("Abcdef1!Abcdef1!"), entropy_bits("Abcdef1!"))

    def test_sequences(self):
        self.assertTrue(has_sequence("xx1234xx"))
        self.assertTrue(has_sequence("myqwerty"))
        self.assertFalse(has_sequence("t7#Kq!9v"))

    def test_repeats(self):
        self.assertTrue(has_repeats("helloooo"))
        self.assertFalse(has_repeats("hello"))


if __name__ == "__main__":
    unittest.main()
