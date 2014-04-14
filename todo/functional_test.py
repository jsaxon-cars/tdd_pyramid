import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        #self.browser.quit()
        pass

    def get_table_rows(self):
        table = self.browser.find_element_by_id('id_list_tab')
        rows = table.find_elements_by_tag_name('tr')
        row_texts = [row.text for row in rows]
        return row_texts

    def test_starting_a_todo_list(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get('http://localhost:6543')

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)

        # She is invited to enter a to-do item straight away

        self.assertIn('To-Do', self.browser.find_element_by_tag_name('h1').text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)

        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        row_texts = self.get_table_rows()
        self.assertIn('1: Buy peacock feathers', row_texts)

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to buy a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        row_texts = self.get_table_rows()
        self.assertIn('1: Buy peacock feathers', row_texts)
        self.assertIn('2: Use peacock feathers to buy a fly', row_texts)

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep

        self.fail('Finish the test!')


if __name__ == "__main__":
    unittest.main(warnings='ignore')
