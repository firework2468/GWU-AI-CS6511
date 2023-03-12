import unittest
from main import CSP


class Test(unittest.TestCase):
    def test1(self):
        result, f = CSP("input2.txt")
        if f:
            for key in result.keys().__reversed__():
                print('', key, "and this node is:", '', result[key])
        else:
            print("There is no solution.")

    def test2(self):
        result, f = CSP("input3.txt")
        if f:
            for key in result.keys().__reversed__():
                print('', key, "and this node is:", '', result[key])
        else:
            print("There is no solution.")

    def test3(self):
        result, f = CSP("input4.txt")
        if f:
            for key in result.keys().__reversed__():
                print('', key, "and this node is:", '', result[key])
        else:
            print("There is no solution.")

    def test4(self):
        result, f = CSP("input5.txt")
        if f:
            for key in result.keys().__reversed__():
                print('', key, "and this node is:", '', result[key])
        else:
            print("There is no solution.")

    def test5(self):
        result, f = CSP("input6.txt")
        if f:
            for key in result.keys().__reversed__():
                print('', key, "and this node is:", '', result[key])
        else:
            print("There is no solution.")

    def test6(self):
        result, f = CSP("input7.txt")
        if f:
            for key in result.keys().__reversed__():
                print('', key, "and this node is:", '', result[key])
        else:
            print("There is no solution.")


if __name__ == '__main__':
    unittest.main()
