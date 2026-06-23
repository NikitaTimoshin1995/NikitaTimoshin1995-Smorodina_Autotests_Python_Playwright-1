from pathlib import Path
import time
import psycopg2
import pytest
from playwright.sync_api import Page
from config import db_name, db_name_dev_logs, host, password, user


@pytest.fixture
def db_connection():
    """Fixture for connecting to the main PostgreSQL database."""
    connection = None
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=db_name,
        )
        print("(INFO) PostgreSQL connection established.")
        yield connection
    except Exception as ex:
        print("(INFO) PostgreSQL connection error:", ex)
        yield None
    finally:
        if connection is not None:
            connection.close()
            print("(INFO) PostgreSQL connection closed.")


@pytest.fixture
def db_connection_dev_logs():
    """Fixture for connecting to the dev logs PostgreSQL database."""
    connection = None
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=db_name_dev_logs,
        )
        print("(INFO) PostgreSQL connection established.")
        yield connection
    except Exception as ex:
        print("(INFO) PostgreSQL connection error:", ex)
        yield None
    finally:
        if connection is not None:
            connection.close()
            print("(INFO) PostgreSQL connection closed.")


@pytest.fixture
def intercept_requests(page: Page):
    """Fixture for capturing requests relevant to UI checks."""
    requests = []
    active_requests_count = 0

    def log_request(request):
        nonlocal active_requests_count
        if (
            request.url.startswith("https://ff.kis.v2.scr.kaspersky-labs.com/")
            or request.url.startswith("https://core-renderer-tiles.maps.yandex")
            or request.url.startswith("https://fonts.gstatic.com/")
            or request.url.startswith("https://cdn.smorodina.ru/dev/pictures/products/")
            or request.url.startswith("https://privacy-cs.mail.ru")
            or request.url.startswith("https://top-fwz1.mail.ru")
            or request.url.startswith("https://webmapapi.navitel.ru")
            or request.url.startswith("https://api.sendychat.ru")
            or request.url.startswith("https://directcrm.dashamail.com/")
            or request.url.endswith("/api/tours/bundles")
            or request.url.startswith("blob:")
        ):
            return
        # print(f\"{time.strftime('%H:%M:%S')} - Request: {request.method} {request.url}\")
        requests.append(request)
        active_requests_count += 1

    def log_response(response):
        nonlocal active_requests_count
        active_requests_count -= 1
        if active_requests_count < 0:
            active_requests_count = 0
    page.on("request", log_request)
    page.on("response", log_response)
    yield requests
    requests.clear()


@pytest.fixture
def photo_paths():
    def _get_paths(*filenames):
        project_dir = Path(__file__).parent.parent
        photos_dir = project_dir / "photos"
        return [str(photos_dir / fn) for fn in filenames]
    return _get_paths
