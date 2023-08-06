import io
import os
import re
import zipfile
import requests

from bs4 import BeautifulSoup

from .constant import DATA_URL
from .utils import download_2_file_content



def get_subset_links() -> list:
    """
    Get list of links for subsets of data.

    Returns:
        list: list of URLs to the zipped subsets
    """

    site = requests.get(DATA_URL)
    soup = BeautifulSoup(site.content, features="html.parser")

    links = []

    for link in soup.find_all("a"):
        if "zip" in link.get("href"):
            links.append(link.get("href"))

    return links


def download_zip(zip_url: str) -> (str, str):
    """
    Args:
        zip_url (str): URL to a zip subset of the data

    Returns:
        (str, list): file name and content of the file that is included in the zip archiv

    Raises:
        HTTPError: Will be raised if the ``zip_url`` responsed a not 200 code
    """

    try:
        request = requests.get(zip_url)

    except Exception:
        raise requests.HTTPError(f"Could not get URL: {zip_url}")


    if request.status_code == 200:
        zip_file_bytes = io.BytesIO(request.content)
        zipped_sub_set = zipfile.ZipFile(zip_file_bytes)

        # Zip archives only contain a single file
        file_name = zipped_sub_set.namelist()[0]
        download_content = zipped_sub_set.read(file_name).decode("utf8")

        # fix not consistant file names if necessary
        if not re.match(r".*\d{3}_\d{4}\.txt", file_name):
            file_name = os.path.splitext(file_name)[0]
            file_name = f"{file_name[:3]}_{file_name[-4:]}.txt"

        return file_name, download_2_file_content(download_content)

    else:
        raise requests.HTTPError(f"Could not get URL: {zip_url}")
