#!/usr/bin/env python3
"""Build or verify immutable complete kitchen review V44."""

import os
import runpy

os.environ["KITCHEN_COMPLETE_REVIEW_VERSION"] = "44"
runpy.run_path(os.path.join(os.path.dirname(__file__), "build_kitchen_ligne_claire_complete_review_v43.py"), run_name="__main__")
