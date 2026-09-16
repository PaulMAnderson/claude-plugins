"""Minimal HTML view and HTTP handler."""

from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .status import Project, collect


def render(projects: list[Project]) -> str:
    rows = []
    for result in collect(projects):
        if result.error:
            cells = [result.project.name, "Error", result.error, "", "", ""]
        else:
            fields = result.fields
            assert fields is not None
            cells = [result.project.name, fields["status"], fields["current_tier"],
                     fields["current_work"] or "", fields["last_updated"], result.summary]
        rows.append("<tr>" + "".join(f"<td>{escape(str(cell))}</td>" for cell in cells) + "</tr>")
    return ("<!doctype html><html lang=\"en\"><meta charset=\"utf-8\">"
            "<title>Hypercube project status</title><style>body{font:1rem system-ui;max-width:80rem;margin:2rem auto;padding:0 1rem}"
            "table{border-collapse:collapse;width:100%}th,td{border:1px solid #aaa;padding:.5rem;text-align:left}"
            "tr:nth-child(even){background:#f3f3f3}</style><h1>Project status</h1>"
            "<table><thead><tr><th>Project</th><th>Status</th><th>Tier / error</th><th>Work</th>"
            "<th>Updated</th><th>Summary</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table></html>")


def make_handler(projects: list[Project]):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path != "/":
                self.send_error(404)
                return
            body = render(projects).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    return Handler


def serve(projects: list[Project], host: str, port: int) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), make_handler(projects))
