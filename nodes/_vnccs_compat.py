"""
Dynamic loader for the original ComfyUI_VNCCS package.
Finds the VNCCS package via folder_paths and provides utilities
without triggering __init__.py side-effects.
"""
import os
import sys
import types
import inspect
import importlib.util as _ilu
from types import SimpleNamespace
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
    spec = _ilu.spec_from_file_location(name, filepath,
                                        submodule_search_locations=[])
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {filepath}")
    mod = _ilu.module_from_spec(spec)
    mod.__package__ = "vnccs"
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def load_utils():
    return _load_module("_vnccs_utils_pkg", "utils.py")


def load_vnccs_utils():
    return _load_module("_vnccs_vnccs_utils_pkg", "nodes/vnccs_utils.py")


def _call_comfy_node(class_name, **kwargs):
    """Standalone version of character_generator._call_comfy_node.
    Looks up a ComfyUI node by class name and calls its FUNCTION."""
    import nodes as comfy_nodes

    vnccs_node_id = kwargs.pop("_vnccs_node_id", None)
    mappings = getattr(comfy_nodes, "NODE_CLASS_MAPPINGS", {})
    cls = mappings.get(class_name)
    if cls is None:
        raise RuntimeError(f"Required node '{class_name}' is not available")

    instance = cls()
    method_name = getattr(cls, "FUNCTION", None)
    method = getattr(instance, method_name, None) if method_name else None
    if method is None:
        for candidate in ("execute", "process", "process_image", "load_model",
                          "loadmodel", "load", "sample", "decode"):
            method = getattr(instance, candidate, None)
            if method is not None:
                break
    if method is None:
        raise RuntimeError(f"Node '{class_name}' has no callable FUNCTION")

    signature = inspect.signature(method)
    accepts_kwargs = any(
        p.kind == inspect.Parameter.VAR_KEYWORD
        for p in signature.parameters.values()
    )
    accepted = (
        kwargs
        if accepts_kwargs
        else {k: v for k, v in kwargs.items() if k in signature.parameters}
    )
    try:
        return method(**accepted)
    except AttributeError as exc:
        if vnccs_node_id is None or "'NoneType' object has no attribute 'node_id'" not in str(exc):
            raise
        module = inspect.getmodule(cls) or inspect.getmodule(method)
        context_getter = getattr(module, "get_executing_context", None) if module is not None else None
        if context_getter is None:
            raise
        context = SimpleNamespace(node_id=str(vnccs_node_id))
        setattr(module, "get_executing_context", lambda: context)
        return method(**accepted)
