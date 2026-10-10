#!/usr/bin/env python3
"""Launch the complete keeper animation reviewer without an internet connection."""

from __future__ import annotations

import argparse
import errno
import json
import sys
import threading
import urllib.error
import urllib.request
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
HOST = "127.0.0.1"
PORT = 8765
REVIEW_ROUTE = "/docs/keeper-scale-audit/review.html"
REVIEW_PATH = ROOT / REVIEW_ROUTE.removeprefix("/")
REVIEW_URL = f"http://{HOST}:{PORT}{REVIEW_ROUTE}"
SOURCE_PREFIX = "/art/raw/keeper-first-batch/"
PAGE_MARKER = "<title>Keeper sizing and transition review</title>"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def review_sources() -> list[str]:
    """Return every unique source strip named by the generated review payload."""
    page = REVIEW_PATH.read_text()
    try:
        payload_text = page.split("const DATA=", 1)[1].split(";\nconst $=", 1)[0]
    except IndexError as error:
        raise RuntimeError("the generated review payload could not be found") from error
    payload = json.loads(payload_text)
    sources: set[str] = set()

    def visit(value: object) -> None:
        if isinstance(value, dict):
            source = value.get("source")
            if isinstance(source, str):
                sources.add(source)
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(payload)
    return sorted(sources)


def validate_local_files() -> list[str]:
    if not REVIEW_PATH.is_file():
        raise RuntimeError(f"the generated review page is missing: {REVIEW_PATH}")
    page = REVIEW_PATH.read_text()
    if PAGE_MARKER not in page:
        raise RuntimeError("the generated review page has the wrong title")
    sources = review_sources()
    if len(sources) != 173:
        raise RuntimeError(
            f"the generated review page names {len(sources)} unique sprite strips, expected 173"
        )
    for source in sources:
        path = (ROOT / source).resolve()
        try:
            path.relative_to(ROOT)
        except ValueError as error:
            raise RuntimeError(f"review source escapes the repository: {source}") from error
        if not path.is_file():
            raise RuntimeError(f"review source is missing: {source}")
        with path.open("rb") as handle:
            if handle.read(8) != PNG_SIGNATURE:
                raise RuntimeError(f"review source is not a PNG: {source}")
    return sources


class OfflineReviewHandler(SimpleHTTPRequestHandler):
    """Serve only the review page and its keeper PNGs on loopback."""

    def allowed(self) -> bool:
        route = unquote(urlsplit(self.path).path)
        return route == REVIEW_ROUTE or (
            route.startswith(SOURCE_PREFIX) and route.endswith(".png")
        )

    def redirect_root(self) -> bool:
        if urlsplit(self.path).path != "/":
            return False
        self.send_response(302)
        self.send_header("Location", REVIEW_ROUTE)
        self.end_headers()
        return True

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler API
        if self.redirect_root():
            return
        if not self.allowed():
            self.send_error(404)
            return
        super().do_GET()

    def do_HEAD(self) -> None:  # noqa: N802 - stdlib handler API
        if self.redirect_root():
            return
        if not self.allowed():
            self.send_error(404)
            return
        super().do_HEAD()

    def log_message(self, format: str, *args: object) -> None:
        return


def page_is_served(sources: list[str]) -> bool:
    try:
        with urllib.request.urlopen(REVIEW_URL, timeout=3) as response:
            page = response.read().decode("utf-8")
        if PAGE_MARKER not in page:
            return False
        for source in sources:
            request = urllib.request.Request(
                f"http://{HOST}:{PORT}/{source}", method="HEAD"
            )
            with urllib.request.urlopen(request, timeout=3) as response:
                content_type = response.headers.get_content_type()
                if response.status != 200 or content_type != "image/png":
                    return False
        try:
            urllib.request.urlopen(f"http://{HOST}:{PORT}/README.md", timeout=3)
        except urllib.error.HTTPError as error:
            if error.code != 404:
                return False
        else:
            return False
        return True
    except (OSError, UnicodeError, urllib.error.URLError):
        return False


def new_server() -> ThreadingHTTPServer:
    handler = partial(OfflineReviewHandler, directory=str(ROOT))
    server = ThreadingHTTPServer((HOST, PORT), handler)
    server.daemon_threads = True
    return server


def pause_after_error() -> None:
    if sys.stdin.isatty():
        try:
            input("\nPress Return to close.")
        except EOFError:
            pass


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the page and every sprite through the offline server, then exit",
    )
    parser.add_argument("--no-open", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    try:
        sources = validate_local_files()
        try:
            server = new_server()
        except OSError as error:
            if error.errno == errno.EADDRINUSE and page_is_served(sources):
                if args.check:
                    print(
                        f"Verified existing offline keeper review and {len(sources)} "
                        f"sprite strips at {REVIEW_URL}"
                    )
                elif not args.no_open:
                    webbrowser.open(REVIEW_URL)
                    print("Opened the already-running offline keeper review.")
                return 0
            if error.errno == errno.EADDRINUSE:
                raise RuntimeError(
                    f"port {PORT} is already used by another local app; close it and try again"
                ) from error
            raise RuntimeError(
                f"the local server could not bind to {HOST}:{PORT}: {error}"
            ) from error

        if args.check:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                if not page_is_served(sources):
                    raise RuntimeError("the local page or one of its sprite strips did not load")
                print(
                    f"Verified offline keeper review and {len(sources)} sprite strips "
                    f"at {REVIEW_URL}"
                )
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=3)
            return 0

        if not args.no_open:
            webbrowser.open(REVIEW_URL)
        print("\nKeeper review is ready offline at:")
        print(REVIEW_URL)
        print("\nLeave this Terminal window open while reviewing.")
        print(
            "Saved choices stay in this browser, and Export downloads "
            "keeper-scale-choices.json normally."
        )
        print("Press Control-C here when you are finished.\n")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nOffline keeper review stopped.")
        finally:
            server.server_close()
        return 0
    except (OSError, RuntimeError, json.JSONDecodeError) as error:
        print(f"Offline keeper review could not start: {error}", file=sys.stderr)
        pause_after_error()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
