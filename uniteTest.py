import unittest
from testing import *


class CurrencyConverterTests(unittest.TestCase):

    def setUp(self):
        self.app = Currency_Converter()
        self.app.geometry('800x720')

    def tearDown(self):
        self.app.destroy()

    def test_start_page_button_click(self):
        self.app.show_frame(PageOne)
        self.app.frames[PageOne].button1.invoke()
        self.assertEqual(self.app.frames[PageOne].button1.cget("text"), "Visite start up page")

    def test_convert_button_click_with_valid_input(self):
        self.app.show_frame(PageOne)
        self.app.frames[PageOne].from_list.set("USD")
        self.app.frames[PageOne].To_list.set("USD")
        self.app.frames[PageOne].entry.insert(tk.END, "100")
        self.app.frames[PageOne].convert_bnt.invoke()
        converted_value = self.app.frames[PageOne].convertedvalue.cget("text")
        self.assertNotEqual(converted_value, "1")

    def test_convert_button_click_with_invalid_input(self):
        self.app.show_frame(PageOne)
        self.app.frames[PageOne].convert_bnt.invoke()
        message = self.app.frames[PageOne].error
        self.assertEqual(message, "Please enter the currency or you wish to Convert")


if __name__ == "__main__":
    unittest.main()
