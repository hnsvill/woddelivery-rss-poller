import unittest

# Dummy test for now - to run as part of the deployment pipeline

class hellotest(unittest.TestCase):
    def testhello(self):
        self.assertEqual('hello, world', 'hello, world')

if __name__ == '__main__':
    unittest.main()