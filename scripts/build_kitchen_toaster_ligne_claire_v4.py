#!/usr/bin/env python3
"""Build or verify immutable toaster Ligne-Claire V4."""

import os
import runpy

os.environ["TOASTER_LIGNE_CLAIRE_VERSION"] = "4"
runpy.run_path(os.path.join(os.path.dirname(__file__), "build_kitchen_toaster_ligne_claire_v1.py"), run_name="__main__")
