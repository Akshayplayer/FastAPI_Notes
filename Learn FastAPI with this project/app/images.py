from dotenv import load_dotenv
from imagekitio import ImageKit
import os

load_dotenv() # check the present .env file and load the below variables.

imagekit = ImageKit(
    private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),
    public_key=os.getenv("IMAGEKIT_PUBLIC_KEY"),
    url_endpoint=os.getenv("IMAGEKIT_URL")
)