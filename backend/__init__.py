#!/usr/bin/env python3

"""Backend package metadata.

Avoid importing runtime modules here to prevent side effects during package import
(for example, initializing DB configuration in test discovery).
"""

__version__ = "0.1.0"
__author__ = "John Makau"
__email__ = "makauwanyoike@gmail.com"
__license__ = "MIT"
__description__ = "A FastAPI application for managing collections with Excel import functionality."
__status__ = "Development"
__copyright__ = "Copyright (c) 2023 John Makau"

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__description__",
    "__status__",
    "__copyright__",
]
