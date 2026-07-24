"""VNCCS Control Center Edited - lightweight clone of the original VNCCS Control Center node."""

from .nodes.vnccs_control_center_edited import NODE_CLASS_MAPPINGS as CC_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as CC_DISPLAY
from .nodes.clothes_designer_edited import NODE_CLASS_MAPPINGS as CD_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as CD_DISPLAY
from .nodes.character_creator_v2_edited import NODE_CLASS_MAPPINGS as CCV2_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as CCV2_DISPLAY

NODE_CLASS_MAPPINGS = {**CC_MAPPINGS, **CD_MAPPINGS, **CCV2_MAPPINGS}
NODE_DISPLAY_NAME_MAPPINGS = {**CC_DISPLAY, **CD_DISPLAY, **CCV2_DISPLAY}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

WEB_DIRECTORY = "web"
