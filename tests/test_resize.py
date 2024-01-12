import unittest
import os
from ScaleCraft import ScaleCraft


class TestMarkdownToHtml(unittest.TestCase):

    def test_scale(self):
        input_path = '../logo-large.png'
        output_path = './output/@0.5x/'

        ScaleCraft(input_path).scale(0.5).saveJPEG(85, output_path)

        self.assertTrue(os.path.exists(output_path))

    def test_resize1(self):
        input_path = '../logo-large.png'
        output_path = './output/resize/'

        ScaleCraft(input_path).resize(400, 300).saveJPEG(85, output_path)

        self.assertTrue(os.path.exists(output_path))


if __name__ == '__main__':
    unittest.main()
