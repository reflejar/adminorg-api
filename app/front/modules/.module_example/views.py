from ..base import BaseFrontView

from . import config

class IndexView(BaseFrontView):

	""" Vista index de example """

	MODULE = config.MODULE
	template_name = f"{config.TEMPLATE_FOLDER}/index.html"
	
	def get_context_data(self, **kwargs):
		return super().get_context_data(**kwargs)