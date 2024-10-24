import logging
from inspect import isclass

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext as _

from strategy_field.fields import StrategyClassField, StrategyField
from strategy_field.utils import fqn

from hope_flex_fields.utils import get_kwargs_from_field_class

from ..attributes.registry import attributes_handler_registry
from ..fields import FlexFormMixin
from ..registry import field_registry
from ..utils import get_default_attrs
from ..validators import JsValidator, ReValidator
from .base import AbstractField, BaseManager

logger = logging.getLogger(__name__)


class FieldDefinitionManager(BaseManager):

    def get_by_natural_key(self, name):
        return self.get(name=name)

    def get_from_django_field(self, django_field: "forms.Field|type[forms.Field]"):
        if isinstance(django_field, forms.Field):
            fld = type(django_field)
        elif isclass(django_field) and issubclass(django_field, forms.Field):
            fld = django_field
        else:
            raise ValueError(django_field)
        name = fld.__name__
        return FieldDefinition.objects.get_or_create(
            name=name,
            field_type=fqn(fld),
            defaults={"attrs": get_kwargs_from_field_class(fld, get_default_attrs())},
        )[0]


class FieldDefinition(AbstractField):
    """This class is the equivalent django.forms.Field class, used to create reusable field types"""

    field_type = StrategyClassField(registry=field_registry)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True
    )
    system_data = models.JSONField(default=dict, blank=True, editable=False, null=True)
    # protected = models.BooleanField(default=False, help_text="If true the field can be deleted only by superusers")
    attribute_handler = StrategyField(
        registry=attributes_handler_registry,
        default="hope_flex_fields.attributes.registry.BaseAttributeHandler",
    )

    objects = FieldDefinitionManager()

    class Meta:
        verbose_name = _("Field Definition")
        verbose_name_plural = _("Field Definitions")
        constraints = (
            UniqueConstraint(fields=("name",), name="fielddefinition_unique_name"),
            UniqueConstraint(fields=("slug",), name="fielddefinition_unique_slug"),
        )

    @property
    def attributes(self):
        return self.attribute_handler.get()
        # return self.attrs

    @attributes.setter
    def attributes(self, value):
        return self.attribute_handler.set(value)
        # self.attrs = value

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)

    def clean(self):
        self.set_default_arguments()
        self.name = str(self.name)
        try:
            self.get_field()
        except TypeError:
            self.attributes = {}
            self.set_default_arguments()

    def set_default_arguments(self):
        if not isinstance(self.attributes, dict) or not self.attributes:
            self.attributes = get_default_attrs()
        if self.field_type:
            attrs = get_kwargs_from_field_class(self.field_type)
            attrs.update(**self.attributes)
            self.attributes = attrs

    @property
    def required(self):
        return self.attributes.get("required", False)

    def get_field(self, override_attrs=None):
        try:
            if override_attrs is not None:
                kwargs = dict(override_attrs)
            else:
                kwargs = dict(self.attributes)
            validators = []
            if self.validation:
                validators.append(JsValidator(self.validation))
            if self.regex:
                validators.append(ReValidator(self.regex))

            kwargs["validators"] = validators
            field_class = type(
                f"{self.name}Field", (FlexFormMixin, self.field_type), {}
            )
            fld = field_class(**kwargs)
        except Exception as e:  # pragma: no cover
            logger.exception(e)
            raise TypeError(
                f"Error creating field for FieldDefinition {self.name}: {e}"
            )
        return fld
