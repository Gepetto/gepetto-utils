import unittest

import example_robot_data


class TestPinocchio(unittest.TestCase):
    def test_trivial(self):
        self.assertEqual(example_robot_data.load('talos').model.nq, 39)


if __name__ == '__main__':
    unittest.main()
