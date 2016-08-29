import os
import time
from django.test import TestCase
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from collection.models import Link, Collection
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
# Create your tests here.


class AdminTestCase(LiveServerTestCase):

	def setUp(self):
		user = User.objects.create_superuser(
			username = 'admin123',
			password = 'admin123',
			email = 'admin1@example.com',
		)

		collec = Collection.objects.create(
			user = user,
			title = 'demo title',
			slug = 'demo-title',
			description = '',
		)

		Link.objects.create(
            title='init',
            link='www.init.com',
            img= '120.png',
            domain='init.com',
            collection=collec,
        )

		chromedriver = "C:\Users\Rahaman\Desktop\chrome_d\chromedriver"
		# self.selenium = webdriver.Chrome(chromedriver)
		self.selenium = webdriver.Firefox()
		self.selenium.maximize_window()
		super(AdminTestCase, self).setUp()

	def tearDown(self):
		time.sleep(2)
		if os.path.exists("/Users/Rahaman/Desktop/Putboard/AWS_Putboard/media_cdn/images/2.png"):
			os.remove("/Users/Rahaman/Desktop/Putboard/AWS_Putboard/media_cdn/images/2.png")
		self.selenium.refresh()
		self.selenium.quit()
		time.sleep(2)
		super(AdminTestCase, self).tearDown()

	# def wait_for_element(element):
	# 	count = 1
	# 	if(self.is_element_present(element)):
	# 		if(self.is_visible(element)):
	# 			return
	# 		else:
	# 			time.sleep(1)
	# 			count = count+1
	# 	else:
	# 		time.sleep(1)
	# 		count = count + 1
	# 		if(count > 300):
	# 			print("Element %s not found" % element)
	# 			self.stop

	def test_create_user(self):
		self.selenium.get(
			'%s%s' % (self.live_server_url, '/register/')
		)

		first_name = self.selenium.find_element_by_id('id_first_name')
		first_name.send_keys('john doe')
		username = self.selenium.find_element_by_id('id_username')
		username.send_keys('admin@example.com')
		password = self.selenium.find_element_by_id('id_password')
		password.send_keys('admin123')

		# self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()
		self.selenium.find_element_by_class_name('btn-submit').click()

		self.selenium.get(
			'%s%s' % (self.live_server_url, '/')
		)
		first_board_title = self.selenium.find_element_by_id('id_title')
		first_board_title.send_keys('Test first board title')
		first_board_description = self.selenium.find_element_by_id('id_description')
		first_board_description.send_keys('first board description test')

		self.selenium.find_element_by_class_name('btn-submit').click()

		add_link_button = self.selenium.find_element_by_css_selector('.fixed-button a')
		add_link_button.click()
		time.sleep(1)

		form_link = self.selenium.find_element_by_id('formLink')
		add_link = form_link.find_element_by_id('id_link')
		add_link.send_keys('www.google.com')
		form_link.find_element_by_css_selector('.btn-add-link').click()
		time.sleep(22)

		# wait_for_element(self.selenium.find_element_by_css_selector('.img-container i'))

		self.selenium.find_element_by_css_selector('.create-board a').click()
		time.sleep(4)
		create_board_modal = self.selenium.find_element_by_id('createBoard')
		second_board_title = create_board_modal.find_element_by_id('id_title')
		second_board_title.send_keys('Second board title')
		second_board_description = create_board_modal.find_element_by_id('id_description')
		second_board_description.send_keys('Second board description test')

		create_board_modal.find_element_by_css_selector('.btn-add-link').click()

		self.selenium.find_element_by_partial_link_text('Second board title').click()
		self.selenium.find_element_by_partial_link_text('Test first board title').click()

		hover = ActionChains(self.selenium).move_to_element(self.selenium.find_element_by_class_name('img-container'))
		hover.perform()
		time.sleep(1)
		self.selenium.find_element_by_css_selector('.img-container i').click()
		time.sleep(1)
		self.selenium.find_element_by_css_selector('.delete-link .btn-add-link').click()
		time.sleep(5)