"""Launch the Hypercube status dashboard."""

import argparse
from pathlib import Path

from .status import load_watch_list
from .web import serve


def main() -> None:
    parser = argparse.ArgumentParser(description="Show registered Astrolabe project statuses")
    parser.add_argument("--config", type=Path, required=True, help="JSON watch-list path")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    try:
        projects = load_watch_list(args.config)
    except ValueError as exc:
        parser.error(str(exc))
    with serve(projects, args.host, args.port) as server:
        print(f"Hypercube serving {len(projects)} projects at http://{args.host}:{server.server_port}/", flush=True)
        server.serve_forever()


if __name__ == "__main__":
    main()
