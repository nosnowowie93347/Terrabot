import asyncio
import collections.abc
import contextlib
import json
import logging
import os
import re
import shutil
import tarfile
import warnings
from datetime import datetime
from pathlib import Path
from typing import (
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    Callable,
    Generator,
    Iterable,
    Iterator,
    List,
    Optional,
    Union,
    TypeVar,
    TYPE_CHECKING,
    Tuple,
    cast,
)

import aiohttp
import discord
import pkg_resources
from rich.progress import ProgressColumn
from rich.progress_bar import ProgressBar

class RichIndefiniteBarColumn(ProgressColumn):
    def render(self, task):
        return ProgressBar(
            pulse=task.completed < task.total,
            animation_time=task.get_time(),
            width=40,
            total=task.total,
            completed=task.completed,
        )