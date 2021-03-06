# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

from page_objects.common import PageObject
from page_objects.common import wait_rpc_done
from page_objects.status_bar import StatusBar


class FormView(PageObject):

    def __init__(self, *args, **kwargs):
        super(FormView, self).__init__(*args, **kwargs)
        self.status_bar = StatusBar(self.driver)

    @property
    def root(self):
        form_views = self.driver.find_elements_by_class_name('o_form_view')
        return next((form_view for form_view in form_views if form_view.is_displayed()), None)

    def is_opened(self):
        return self.root is not None

    def is_in_edit_mode(self):
        try:
            self.driver.find_element_by_class_name("o_form_editable")
            return True
        except NoSuchElementException:
            return False

    def is_in_readonly_mode(self):
        return not self.is_in_edit_mode()

    @wait_rpc_done()
    def create(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until_not(expected_conditions.invisibility_of_element_located((By.CLASS_NAME, "o_form_button_create")))
        self.driver.find_element_by_class_name("o_form_button_create").click()

    @wait_rpc_done()
    def edit(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until_not(expected_conditions.invisibility_of_element_located((By.CLASS_NAME, "o_form_button_edit")))
        self.driver.find_element_by_class_name("o_form_button_edit").click()

    @wait_rpc_done()
    def save(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until_not(expected_conditions.invisibility_of_element_located((By.CLASS_NAME, "o_form_button_save")))
        self.driver.find_element_by_class_name("o_form_button_save").click()

    @wait_rpc_done()
    def discard(self):
        self.driver.find_element_by_class_name("o_form_button_cancel").click()

    def set_field_value_by_placeholder_name(self, placeholder_name, value):
        field = self.driver.find_element_by_css_selector("input[placeholder='%s']" % placeholder_name)
        field.send_keys(value)

    def _find_label(self, label_text):
        labels = self.driver.find_elements_by_tag_name('label')
        label_index = None
        for index, label in enumerate(labels):
            if label.text == label_text:
                label_index = index
                break

        try:
            return labels[label_index]
        except (IndexError, ValueError):
            raise NoSuchElementException(msg='Label "%s" was not found' % label_text)

    def fill_field_by_label(self, label_text, value):
        label = self._find_label(label_text)
        field_id = label.get_attribute("for")

        field_elem = self.driver.find_element_by_id(field_id)

        # Selection field
        if field_elem.tag_name == 'select':
            select_elem = Select(field_elem)
            select_elem.select_by_visible_text(value)
        else:
            field_elem.send_keys(value)

    def get_field_value_by_label_name(self, label_name):
        label = self._find_label(label_name)
        field_id = label.get_attribute("for")
        return self.driver.find_element_by_xpath("//label[@for='%s']/../following-sibling::td" % field_id).text
