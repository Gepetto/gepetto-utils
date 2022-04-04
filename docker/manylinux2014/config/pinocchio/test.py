import unittest

import pinocchio


class TestPinocchio(unittest.TestCase):
    def test_trivial(self):
        self.assertEqual(
            str(pinocchio.SE3.Identity().inverse()),
            "  R =\n1 0 0\n0 1 0\n0 0 1\n  p = -0 -0 -0\n",
        )


if __name__ == "__main__":
    unittest.main()
