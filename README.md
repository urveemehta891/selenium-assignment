## How to run this repo

### Installation

After cloning this repo, create a virtual environment and from this repo's directory, run this command:
`pip install -r requirements.txt`

Since we are using Selenium and Google Chrome to run these tests, install Chromedriver from this link for your Google Chrome's current version: [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)

#### Mac users
Move `chromedriver` to `/usr/local/bin/` so that it gets added to the PATH.

#### Windows users
Include the ChromeDriver location in your PATH environment variable.


### Running the tests

To run the tests, run this command in the main repo folder:
`pytest -v --html wikipedia_test_report.html`


You can also open `wikipedia_test_report.html` in the browser to check your test results formatted in an easy-to-understand manner.