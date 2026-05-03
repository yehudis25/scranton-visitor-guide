# test scraper program

from scraper import scrape_activities
from unittest.mock import patch, Mock

FAKE_HTML = """
<html>
  <body>

    <h2 id="Landmarks_and_attractions"></h2>

    <p>
      heritage <a href="/wiki/Valid_Place" title="Valid Place">Valid Place</a>
      <a href="/wiki/National_Park" title="National Park">National Park</a>
    </p>

    <h3>Next section</h3>

  </body>
</html>
"""


"""make sure the scraper returns something and is a list"""


@patch("scraper.requests.get")
def test_scrape(mock_get):
    mock_response = Mock()
    mock_response.content = FAKE_HTML
    mock_get.return_value = mock_response

    result = scrape_activities()

    assert isinstance(result, list)
    assert len(result) > 0


"""make sure the scraping is returning proper results"""


@patch("scraper.requests.get")
def test_filtering(mock_get):
    mock_response = Mock()
    mock_response.content = FAKE_HTML
    mock_get.return_value = mock_response

    result = scrape_activities()
    names = []
    category = []

    for r in result:
        names.append(r["name"])
        category.append(r["category"])

    assert "National Park" not in names
    assert "Valid Place" in names
    assert "History" in category
    item = result[0]

    assert "name" in item
    assert "category" in item
    assert "link" in item


MISSING_HTML = """
<html>
  <body>
    <p>No section here</p>
  </body>
</html>
"""


"""assert that if the website wld close the code would return []"""


@patch("scraper.requests.get")
def test_scrape_missing(mock_get):
    mock_response = Mock()
    mock_response.content = MISSING_HTML
    mock_get.return_value = mock_response

    result = scrape_activities()

    assert result == []
