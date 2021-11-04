#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8


import argparse
import logging
import sys

import uvicorn
from smartsim.core.app import app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(sys.argv[0])


class Session:
    # TODO add up?
    def __init__(self):
        parser = argparse.ArgumentParser(prog="smart session",
                                         description="Start a SmartSim session")

        parser.add_argument("--host", type=str, default="0.0.0.0",
                            help="Specify host address to bind to")
        parser.add_argument("--port", type=int, default="8000",
                            help="Specify port to use")
        args = parser.parse_args(sys.argv[2:])

        self.serve(args.host, args.port)

    def serve(self, host, port):
        try:
            logger.info(f"Running server at address {':'.join((host, str(port)))}")
            uvicorn.run(app, host="0.0.0.0", port=8000)
        except KeyboardInterrupt:
            logger.info("Exiting on KeyboardInterrupt")
        except Exception as exc:
            logger.info(f"Exiting on unknown error {exc}")
        finally:
            pass
