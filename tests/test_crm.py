# -*- coding: utf-8 -*-

from common import SeleniumCase


class TestCRM(SeleniumCase):

    _depends = ['crm']

    def test_01_partners_handling(self):
        self.web_client = self.login("admin", "admin")

        # Create two partners
        self.web_client.open_app_switcher()
        self.assertTrue(self.web_client.app_switcher.is_opened())
        self.web_client.app_switcher.click_on_menu("CRM")
        self.assertTrue(self.web_client.kanban_view.is_opened())
        self.web_client.menu.dropdown_click("Sales", "Customers")
        self.assertTrue(self.web_client.kanban_view.is_opened())
        self.web_client.kanban_view.create()
        self.assertTrue(self.web_client.form_view.is_opened())
        self.assertTrue(self.web_client.form_view.is_in_edit_mode())
        self.web_client.form_view.set_field_value_by_placeholder_name("Name", "Customer test 1")
        self.web_client.form_view.save()
        self.web_client.form_view.create()
        self.web_client.form_view.set_field_value_by_placeholder_name("Name", "Customer test 2")
        self.web_client.form_view.fill_field_by_label("Job Position", "Job position of customer test 2")
        self.web_client.form_view.save()

        # Merge these two partners
        self.web_client.control_panel.breadcrumbs.previous_path_click()
        self.web_client.control_panel.view_switcher.to_list()
        self.web_client.control_panel.search_view.type_and_enter("Customer test")
        self.web_client.list_view.row_select_all()
        self.assertTrue(self.web_client.control_panel.sidebar.is_opened())
        self.web_client.control_panel.sidebar.click("Merge Selected Contacts")
        self.assertTrue(self.web_client.wizard.is_opened())
        self.web_client.wizard.click_on_footer_buttons("MERGE CONTACTS")
        self.assertTrue(self.web_client.wizard.is_opened())
        self.web_client.wizard.click_on_footer_buttons("Close")

        # Check that the merge did something
        self.web_client.list_view.row_click(1)
        self.web_client.form_view.is_opened()
        self.assertEqual(
            self.web_client.control_panel.breadcrumbs.get_current_path(),
            "Customer test 1"
        )
        self.assertEqual(
            self.web_client.form_view.get_field_value_by_label_name("Job Position"),
            "Job position of customer test 2"
        )
