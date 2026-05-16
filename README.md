# JSONPlaceholder API Test Suite

Automation test suite for [JSONPlaceholder](https://jsonplaceholder.typicode.com/) REST API using Python and pytest.

## Project Structure

```
jsonplaceholder_tests/
├── config/
│   ├── __init__.py
│   └── urls.py           # All API URLs defined here
├── tests/
│   ├── __init__.py
│   ├── test_posts.py
│   ├── test_comments.py
│   ├── test_albums.py
│   ├── test_photos.py
│   ├── test_todos.py
│   └── test_users.py
├── requirements.txt
├── pytest.ini
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
```

## Run All Tests

```bash
pytest
```

## Run Specific File

```bash
pytest tests/test_posts.py
```

## Run Specific Class

```bash
pytest tests/test_posts.py::TestGetPosts
```

## Run Tests and Generate Report

```bash
# Step 1 - run all tests (report.xml will be created automatically)
pytest

# Step 2 - convert XML to HTML
python generate_report.py
```

The HTML report will be saved to `reports/report.html`
