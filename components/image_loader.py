from io import BytesIO
from pathlib import Path

import requests
import streamlit as st
from PIL import Image
from pydantic import HttpUrl


@st.cache_data(show_spinner=False)
def _fetch_cached_image(url: str) -> Image.Image | None:
    """Fetch and cache an image from a URL."""
    response = requests.get(str(url), timeout=10)

    if response.status_code == 200:

        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type:
            return None

        return Image.open(BytesIO(response.content))

    return None

def fetch_cached_image(url: HttpUrl | str) -> Image.Image | None:
    """Parse any url to string in order to fetch it."""
    image = _fetch_cached_image(str(url))
    if image:
        return image

    return Image.open(Path(__file__).parent.parent / "statics" / "image-not-found.jpg")
