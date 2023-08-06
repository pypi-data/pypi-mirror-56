import argparse
import configparser as ConfigParser
import os
import sys
from pathlib import Path
from webbrowser import open_new_tab

import pyperclip
import requests
from imgz_cli import __version__


def upload(api_key, image, title="", expires_in=None):
    params = {"expires_in": expires_in}
    if title:
        params["title"] = title

    response = requests.post(
        "https://imgz.org/api/image/",
        files={"image": image},
        auth=("", api_key),
        data=params,
        headers={"User-Agent": "Mozilla/5.0 (Python) imgz_cli library"},
    )
    if 400 <= response.status_code < 500:
        rd = response.json()
        raise RuntimeError(rd["error_message"])
    elif 500 <= response.status_code < 600:
        raise RuntimeError("There was a server error, please try again later.")
    elif response.status_code == 413:
        raise RuntimeError(
            "Much like yourself, that file was too large. Try something smaller."
        )
    else:
        return response.json()


def main():
    config = ConfigParser.ConfigParser()
    config.read([os.path.expanduser("~/.config/imgz.cfg")])
    try:
        config = dict(config.items("imgz"))
    except:  # noqa
        sys.exit(
            "Config file not found. Make sure you have a config file"
            " at ~/.config/imgz.cfg with a [imgz] section containing"
            " your IMGZ API key, which you can get from your"
            " https://imgz.org account page.\n\n"
            "Example:\n\n"
            "[imgz]\napi_key = MyIMGZAp13eY"
        )

    if "api_key" not in config:
        sys.exit(
            "IMGZ API key not found in the config. Get it from your"
            " https://imgz.org account page."
        )

    parser = argparse.ArgumentParser(description="Upload a file to IMGZ.")
    parser.add_argument(
        "filename",
        metavar="FILENAME",
        type=str,
        default="",
        nargs="?",
        help="the name of the image to upload (or stdin, if omitted)",
    )
    parser.add_argument(
        "-t", "--title", metavar="TITLE", type=str, help="the title of the image"
    )
    parser.add_argument(
        "-e",
        "--expires-in",
        metavar="MINUTES",
        type=int,
        help="the number of minutes this image expires in",
    )
    parser.add_argument(
        "-p",
        "--page",
        action="store_true",
        help="copy the image page's URL instead of the image's",
    )
    parser.add_argument(
        "-b",
        "--open-browser",
        action="store_true",
        help="automatically open a browser window when done",
    )
    parser.add_argument(
        "-V", "--version", action="store_true", help="show the version and quit"
    )

    args = parser.parse_args()
    if args.version:
        sys.exit("imgz, version %s." % __version__)

    if args.filename:
        image = open(args.filename, "rb").read()
        title = args.title or Path(args.filename).name
    else:
        if sys.stdin.isatty():
            print(
                "Now what? Are you going to type your image in? Alright,"
                " press Ctrl+D when you're done. Idiot."
            )
        image = sys.stdin.buffer.read()
        if not image:
            sys.exit("Didn't think so.")
        title = args.title or "My stdin"

    try:
        data = upload(config["api_key"], image, title=title, expires_in=args.expires_in)
    except RuntimeError as e:
        print("ERROR: %s" % e)
    else:
        image_url = data["urls"]["image"]
        page_url = data["urls"]["page"]
        print("Page URL: %s" % page_url)
        print("Image URL: %s" % image_url)
        url = page_url if args.page else image_url
        try:
            pyperclip.copy(url)
        except pyperclip.exceptions.PyperclipException:
            print(
                "Pyperclip isn't working properly on your system, imgz"
                " cannot copy the URL to the clipboard automatically. If"
                " you are on Linux, try installing xclip."
            )
        if args.open_browser:
            open_new_tab(url)


if __name__ == "__main__":
    main()
