import requests
from minsearch import Index
from tqdm.auto import tqdm


def load_faq_data():
    docs_url = 'https://datatalks.club/faq/json/courses.json'
    print("getting request")
    response = requests.get(docs_url)
    print("request completed")
    courses_raw = response.json()

    documents = []
    url_prefix = 'https://datatalks.club/faq'

    for course in courses_raw:
        print(f"append information {course}")
        course_url = f'{url_prefix}{course["path"]}'
        course_response = requests.get(course_url)
        course_response.raise_for_status()
        course_data = course_response.json()

        documents.extend(course_data)

    return documents


def build_index(documents):
    print("Start building index...")
    index = Index(
        text_fields=['question', 'section', 'answer'],
        keyword_fields=['course']
    )
    index.fit(documents)

    print("Index already created")
    return index
