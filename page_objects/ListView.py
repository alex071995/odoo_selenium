# -*- coding: utf-8 -*-

from page_objects.common import PageObject
from page_objects.common import wait_rpc_done


class ListView(PageObject):

    def select_rows(self, *args):
        pass

    def select_all_rows(self):
        self.driver.find_element_by_class_name("o_list_view")\
            .find_element_by_class_name("o_list_record_selector")\
            .find_element_by_tag_name("input")\
            .click()

    @wait_rpc_done()
    def click_on_row(self, row_index):
        rows = self.driver.find_element_by_class_name("o_list_view")\
            .find_element_by_tag_name("tbody")\
            .find_elements_by_tag_name("tr")
        rows[row_index -1].click()
