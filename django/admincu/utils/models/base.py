"""Django models utilities."""

from django.db import models
from django.utils import timezone

class SoftDeletionQuerySet(models.query.QuerySet):
	def delete(self):
		return super(SoftDeletionQuerySet, self).update(eliminacion=timezone.now())

	def hard_delete(self):
		return super(SoftDeletionQuerySet, self).delete()

	def alive(self):
		return self.filter(eliminacion=None)

	def dead(self):
		return self.exclude(eliminacion=None)

class SoftDeletionManager(models.Manager):
	def __init__(self, *args, **kwargs):
		self.alive_only = kwargs.pop('alive_only', True)
		super(SoftDeletionManager, self).__init__(*args, **kwargs)

	def get_queryset(self):
		if self.alive_only:
			return SoftDeletionQuerySet(self.model).filter(eliminacion=None)
		return SoftDeletionQuerySet(self.model)

	def hard_delete(self):
		return self.get_queryset().hard_delete()


class BaseModel(models.Model):
	"""
		AdminCU base model.
		Modelo abstracto para agregar en todos los modelos que necesiten de:
			comunidad
			creacion
			modificacion
			eliminacion
			a futuro: usuarios
			establece el nuevo objects y all_objects
	"""
	
	comunidad = models.ForeignKey(
		"utils.Comunidad",
		on_delete=models.CASCADE
	)
	
	creacion = models.DateTimeField(
		'creacion',
		auto_now_add=True,
		help_text='Fecha en la que fue creado.'
	)
	modificacion = models.DateTimeField(
		'modificacion',
		auto_now=True,
		help_text='Fecha en la que fue modificado.'
	)
	eliminacion = models.DateTimeField(
		'eliminacion',
		blank=True,
		null=True,
		help_text='Fecha en la que fue eliminado.'
	)

	objects = SoftDeletionManager()

	all_objects = SoftDeletionManager(alive_only=False)

	class Meta:

		"""Meta option."""

		abstract = True

		get_latest_by = 'creacion'
		ordering = ['-creacion', '-modificacion']

	def delete(self):
		self.eliminacion = timezone.now()
		self.save()

	def hard_delete(self):
		super(BaseModel, self).delete()
