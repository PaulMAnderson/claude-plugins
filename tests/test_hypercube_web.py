from http.client import HTTPConnection
from pathlib import Path
import tempfile
import threading
import unittest

from hypercube.status import Project
from hypercube.web import serve
from test_hypercube_status import VALID


class WebTests(unittest.TestCase):
    def test_http_page_is_escaped_and_refreshes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            status = root / ".astrolabe" / "STATUS.md"
            status.parent.mkdir()
            status.write_text(VALID.replace("Working on sample.", "<script>alert(1)</script>"))
            with serve([Project("<test>", root), Project("Missing", root / "missing")], "127.0.0.1", 0) as server:
                thread = threading.Thread(target=server.serve_forever, daemon=True)
                thread.start()
                try:
                    connection = HTTPConnection("127.0.0.1", server.server_port)
                    connection.request("GET", "/")
                    response = connection.getresponse()
                    page = response.read().decode()
                    self.assertEqual(response.status, 200)
                    self.assertIn("&lt;test&gt;", page)
                    self.assertIn("&lt;script&gt;", page)
                    self.assertNotIn("<script>", page)
                    self.assertIn("Missing", page)
                    self.assertIn("Error", page)
                    status.write_text(VALID.replace("Working on sample.", "Updated."))
                    connection.request("GET", "/")
                    self.assertIn("Updated.", connection.getresponse().read().decode())
                    connection.request("GET", "/other")
                    self.assertEqual(connection.getresponse().status, 404)
                    connection.close()
                finally:
                    server.shutdown()
                    thread.join()


if __name__ == "__main__":
    unittest.main()
