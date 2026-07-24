"""
Dynamic loader for the original ComfyUI_VNCCS package.
Finds the VNCCS package via folder_paths and loads individual modules
without triggering __init__.py side-effects.
"""
import os
import importlib.util as _ilu
import folder_paths


def _find_vnccs_root():
    """Locate the original VNCCS package directory."""
    base = os.path.dirname(folder_paths.__file__)
    candidates = [
        os.path.join(base, "custom_nodes", "vnccs"),
        os.path.join(base, "custom_nodes", "ComfyUI_VNCCS"),
    ]
    for path in candidates:
        if os.path.isdir(path):
            return path
    raise FileNotFoundError(
        "Cannot find original VNCCS package. "
        "Expected at custom_nodes/vnccs/ or custom_nodes/ComfyUI_VNCCS/"
    )


_VNCCS_ROOT = None


def get_vnccs_root():
    global _VNCCS_ROOT
    if _VNCCS_ROOT is None:
        _VNCCS_ROOT = _find_vnccs_root()
    return _VNCCS_ROOT


def _load_module(name, relative_path):
    """Load a single .py file from the VNCCS package without running __init__."""
    root = get_vnccs_root()
    filepath = os.path.join(root, relative_path)
    spec = _ilu.spec_from_file_location(name, filepath)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {filepath}")
    mod = _ilu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_utils():
    return _load_module("_vnccs_utils_mod", "utils.py")


def load_vnccs_utils():
    return _load_module("_vnccs_vnccs_utils_mod", "nodes/vnccs_utils.py")


def load_character_generator():
    return _load_module("_vnccs_char_gen_mod", "nodes/character_generator.py")
