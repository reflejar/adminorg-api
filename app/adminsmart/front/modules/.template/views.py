from ..base import (
	BaseAdminView
)

from . import config

class IndexView(BaseAdminView):

	""" Vista index de template """

	MODULE = config.MODULE
	MODULE_BUTTONS = config.MODULE_BUTTONS
	MODULE_HANDLER = config.MODULE_HANDLER
	template_name = f"{config.TEMPLATE_FOLDER}/index.html"
	
	