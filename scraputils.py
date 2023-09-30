import requests  # type: ignore
from bs4 import BeautifulSoup  # type: ignore


def extract_news(parser):
    """Extract news from a given web page"""

    news_list = []
    news_table = parser.table.find_all("table")[1]
    rows = news_table.find_all("tr")

    for i in range(0, len(rows) - 2, 3):
        news_info = {}
        news = rows[i]
        news_link = news.find("span", class_="titleline").find("a")
        news_info["title"] = news_link.text
        news_info["url"] = (
            news_link["href"]
            if news_link["href"].startswith("http")
            else "https://news.ycombinator.com/" + news_link["href"]
        )

        comments_and_points = rows[i + 1]
        author = comments_and_points.find("a", class_="hnuser").text
        points = int(comments_and_points.find("span", class_="score").text.split()[0])

        comments_tag = comments_and_points.find("span", id=lambda x: x and "unv_" in x)
        comments = 0
        if comments_tag is not None:
            for sibling in comments_tag.next_siblings:
                if sibling.name == "a" and "item?id" in sibling["href"]:
                    comments_text = sibling.text.strip()
                    comments = int(comments_text.split()[0]) if "comment" in comments_text else 0
                    break

        news_info["author"] = author
        news_info["points"] = points
        news_info["comments"] = comments

        news_list.append(news_info)

    return news_list


def extract_next_page(parser):
    """Extract next page URL"""

    news_table = parser.table.find_all("table")[1]
    next_page_link = news_table.find("a", class_="morelink")

    return next_page_link["href"]


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
