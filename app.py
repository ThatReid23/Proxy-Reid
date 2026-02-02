# app.py
from flask import Flask, request, Response, send_from_directory
from urllib.parse import unquote
import requests
import gzip
import re
import os

# ----------------------------------------------------------------------
# Flask app
# ----------------------------------------------------------------------
app = Flask(__name__)

# ----------------------------------------------------------------------
# 1. Static File Handling
# ----------------------------------------------------------------------

@app.route("/")
def index():
    return send_from_directory(".", "games.html")

@app.route("/assets/<path:filename>")
def serve_assets(filename):
    """Maps the /assets/ URL used in games.html to your actual static/img folder."""
    return send_from_directory("static/img", filename)

@app.route("/static/<path:filename>")
def serve_static_files(filename):
    """Serves CSS and JS from the static folder."""
    return send_from_directory("static", filename)

@app.route("/<path:filename>")
def root_static(filename):
    """General handler for files in the root directory (like runer.html)."""
    if ".." in filename or filename.startswith("/"):
        return "Forbidden", 403
        
    allowed = {
        ".html", ".css", ".js", ".png", ".jpg", ".jpeg",
        ".gif", ".svg", ".ico", ".woff2", ".woff", ".ttf",
        ".webp", ".avif", ".jfif"
    }
    
    if not any(filename.lower().endswith(ext) for ext in allowed):
        return "Not allowed", 415
        
    return send_from_directory(".", filename)


# ----------------------------------------------------------------------
# 2. Stealth proxy – /p/<encoded_url>
# ----------------------------------------------------------------------
@app.route("/p/<path:encoded_url>")
def stealth_proxy(encoded_url):
    try:
        url = unquote(encoded_url)
        if not url.lower().startswith(("http://", "https://")):
            return "Invalid URL – must start with http(s)://", 400

        headers = {
            "User-Agent": request.headers.get(
                "User-Agent",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/129.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": request.headers.get("Referer", ""),
            "Connection": "keep-alive",
        }

        sess = requests.Session()
        sess.headers.update(headers)

        resp = sess.get(
            url,
            params=request.args,
            timeout=30,
            allow_redirects=True,
            stream=False,
        )
        resp.raise_for_status()

        # ----- Decompress safely -----
        content = resp.content
        enc = resp.headers.get("Content-Encoding", "").lower()

        try:
            if "br" in enc:
                import brotli
                content = brotli.decompress(content)
            elif "gzip" in enc:
                content = gzip.decompress(content)
        except Exception as e:
            print(f"Decompression failed, using raw: {e}")

        # ----- Prepare headers -----
        excluded = ["content-encoding", "content-length", "transfer-encoding", "connection"]
        resp_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded}
        resp_headers.setdefault("Content-Type", "text/html; charset=utf-8")

        # ----- HTML rewriting -----
        if "text/html" in resp_headers.get("Content-Type", ""):
            try:
                text = content.decode("utf-8", errors="replace")
                # Simple logic to keep relative links inside the proxy
                base_proxy = "/p/" + url.split("://", 1)[1].split("/", 1)[0]
                text = re.sub(r'(href|src|action)=["\']/(?!/)', rf'\1="{base_proxy}/', text)
                text = re.sub(r'(href|src|action)=["\'](?!https?:|/)', rf'\1="{base_proxy}/', text)
                content = text.encode("utf-8")
            except Exception as e:
                print(f"HTML rewrite error: {e}")

        # ----- Stream response -----
        def stream():
            for i in range(0, len(content), 8192):
                yield content[i:i+8192]

        return Response(
            stream(),
            status=resp.status_code,
            headers=resp_headers,
            content_type=resp_headers.get("Content-Type")
        )

    except Exception as e:
        print(f"Proxy error ({url}): {e}")
        return f"Proxy error: {e}", 500

# ----------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)