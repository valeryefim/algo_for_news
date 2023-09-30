import string  # type: ignore

from bayes import NaiveBayesClassifier
from bottle import redirect, request, route, run, template  # type: ignore
from db import News, session  # type: ignore
from scraputils import get_news


@route("/")
def index():
    redirect("/news")


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    label = request.query.label
    news_id = request.query.id

    news_item = s.query(News).filter(News.id == news_id).first()
    if news_item:
        news_item.label = label
        s.commit()

    redirect("/news")


@route("/update")
def update_news():
    s = session()
    updated_news = get_news("https://news.ycombinator.com/newest", 1)

    for news in updated_news:
        exists = s.query(
            s.query(News).filter_by(title=news["title"], author=news["author"]).exists()
        ).scalar()
        if not exists:
            news_item = News(
                title=news["title"],
                author=news["author"],
                url=news["url"],
                comments=news["comments"],
                points=news["points"],
            )
            s.add(news_item)
            s.commit()

    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    news_train = s.query(News).filter(News.label != None).all()
    news_test = s.query(News).filter(News.label == None).all()

    X_train = [
        "".join(c for c in n.title.lower() if c not in string.punctuation) for n in news_train
    ]
    y_train = [n.label for n in news_train]

    classifier = NaiveBayesClassifier()
    classifier.fit(X_train, y_train)

    X_test = ["".join(c for c in n.title.lower() if c not in string.punctuation) for n in news_test]
    y_pred = classifier.predict(X_test)

    for news_item, prediction in zip(news_test, y_pred):
        news_item.predicted_label = prediction

    sorted_news = sorted(
        news_test, key=lambda news: ("good", "maybe", "never").index(news.predicted_label)
    )

    return template("news_template", rows=sorted_news)


if __name__ == "__main__":
    run(host="localhost", port=8080)