import argparse
import logging
import os

import uvicorn

from life.config import load_config
from life.server import create_app


def main() -> None:
    parser = argparse.ArgumentParser(description="LIFE emergency detection")
    parser.add_argument("--config", default=None, help="Path to config.yaml")
    parser.add_argument("--source", choices=["webcam", "file", "rtsp", "demo"],
                        help="Override source type")
    parser.add_argument("--path", help="Override source path (index / file / url)")
    parser.add_argument("--host", default=None, help="Override server host")
    parser.add_argument("--port", type=int, default=None, help="Override server port")
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(args.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    config = load_config(args.config)
    if args.source:
        config["source"]["type"] = args.source
    if args.path is not None:
        config["source"]["path"] = args.path

    host = args.host or os.getenv("HOST", "0.0.0.0")
    port = args.port or int(os.getenv("PORT", "8000"))

    app = create_app(config)

    logging.getLogger("life").info(
        "Dashboard: http://%s:%s  (source=%s)", host, port, config["source"]["type"]
    )

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level=args.log_level.lower()
    )


if __name__ == "__main__":
    main()