import unittest
from main import Pitcher, read_file


class Test(unittest.TestCase):
    def test1(self):
        capacities = read_file("input1.txt")
        pitcher = Pitcher()
        result = pitcher.A_star(capacities)
        self.assertEqual(result, 7)

    def test2(self):
        capacities = read_file("input2.txt")
        pitcher = Pitcher()
        result = pitcher.A_star(capacities)
        self.assertEqual(result, -1)

    def test3(self):
        capacities = read_file("input3.txt")
        pitcher = Pitcher()
        result = pitcher.A_star(capacities)
        self.assertEqual(result, -1)

    def test4(self):
        capacities = read_file("input4.txt")
        pitcher = Pitcher()
        result = pitcher.A_star(capacities)
        self.assertEqual(result, 36)


if __name__ == '__main__':
    unittest.main()
