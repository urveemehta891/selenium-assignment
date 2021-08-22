import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

# constants
BASE_URL = "https://en.wikipedia.org/wiki/Metis_(mythology)"
TABLE_OF_CONTENTS_CSS_SELECTOR = "div.toc ul li.toclevel-1{}"
PAGE_PREVIEW_API_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"
PAGE_PREVIEW_TEXT_TO_CHECK = "In ancient Greek civilization, Nike was a goddess who personified victory. Her Roman equivalent was Victoria."

def setup_module():
	global driver
	driver = webdriver.Chrome(executable_path="C:\\bin\\chromedriver.exe")
	driver.implicitly_wait(3)
	driver.get(BASE_URL)

def teardown_module():
	driver.quit()

def test_table_of_contents():
	headings_toc = []
	headings_page = []

	table_of_contents = get_table_of_contents(driver)
	
	for content in table_of_contents:
		heading = content.find_element(By.CSS_SELECTOR, "a span.toctext")
		headings_toc.append(heading.text)

	headings_page_element = driver.find_elements(By.CSS_SELECTOR, "h2 span.mw-headline")

	for element in headings_page_element:
		headings_page.append(element.text)

	assert len(headings_page) == len(headings_toc)
	assert headings_page == headings_toc

def test_table_of_contents_hyperlinks():
	toc_link_elements = get_table_of_contents(driver, " a")

	hyperlinks = [element.get_attribute("href") for element in toc_link_elements]

	sub_links = []

	# clicking on these links will onyl scroll to that part of the page,. instead, we are checking the h2 tag with the link sub text after removing the base link - if they match, the hyperlinks will work
	for hyperlink in hyperlinks:
		subtext = hyperlink.split("#")

		if len(subtext) == 1:
			assert False

		sub_links.append(subtext[1].replace("_", " "))

	headings_page = []
	headings_page_elements = driver.find_elements(By.CSS_SELECTOR, "h2 span.mw-headline")

	for element in headings_page_elements:
		headings_page.append(element.text)

	assert headings_page == sub_links

def test_personified_concepts_nike_popup():
	nike_element = driver.find_element(By.LINK_TEXT, "Nike")
	nike_wiki_link = nike_element.get_attribute("href")

	_, page_title = nike_wiki_link.split("/wiki/")

	# the page preview popup calls Wikipedia API on hover action so we are directly calling that API and comparing the extact with the text
	# we can also check whether the page preview functionality has been enabled or not but that is beyond the scope of this test
	response = requests.get(PAGE_PREVIEW_API_URL.format(page_title))

	if response.status_code != 200:
		assert False
	
	response = response.json()
	summary = response["extract"]

	assert summary == PAGE_PREVIEW_TEXT_TO_CHECK


def test_personified_concepts_nike_family_tree():
	nike_element = driver.find_element(By.LINK_TEXT, "Nike")
	nike_wiki_link = nike_element.get_attribute("href")

	driver.get(nike_wiki_link)
	toc_link_elements = get_table_of_contents(driver, " a")
	family_tree_link = None

	for element in toc_link_elements:
		if element.find_element(By.CSS_SELECTOR, "span.toctext").text.lower() == "family tree":
			family_tree_link = element.get_attribute("href")

	if not family_tree_link:
		assert False

	driver.get(family_tree_link)
	driver.save_screenshot("nike_family_tree.png")
	assert True

# Helper methods
def get_table_of_contents(driver, extra_selectors=""):
	return driver.find_elements(By.CSS_SELECTOR, TABLE_OF_CONTENTS_CSS_SELECTOR.format(extra_selectors))

