"""Compatibility entry point for the existing Lab 18 app link."""

from pathlib import Path
from runpy import run_path

run_path(Path(__file__).with_name("Lab_19_Legend_Panel_App.py"), run_name="__main__")
