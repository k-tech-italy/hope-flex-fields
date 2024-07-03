from django import forms
from django.contrib.auth.models import User

import factory.fuzzy
from factory.base import FactoryMetaClass

from hope_flex_fields.models import (
    DataChecker,
    DataCheckerFieldset,
    FieldDefinition,
    Fieldset,
    FieldsetField,
)

factories_registry = {}


class AutoRegisterFactoryMetaClass(FactoryMetaClass):
    def __new__(mcs, class_name, bases, attrs):
        new_class = super().__new__(mcs, class_name, bases, attrs)
        factories_registry[new_class._meta.model] = new_class
        return new_class


class AutoRegisterModelFactory(
    factory.django.DjangoModelFactory, metaclass=AutoRegisterFactoryMetaClass
):
    pass


def get_factory_for_model(_model):
    class Meta:
        model = _model

    if _model in factories_registry:
        return factories_registry[_model]
    return type(
        f"{_model._meta.model_name}Factory", (AutoRegisterModelFactory,), {"Meta": Meta}
    )


class UserFactory(AutoRegisterModelFactory):
    _password = "password"
    username = factory.Sequence(lambda n: "m%03d@example.com" % n)
    password = factory.django.Password(_password)
    email = factory.Sequence(lambda n: "m%03d@example.com" % n)

    class Meta:
        model = User
        django_get_or_create = ("username",)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        ret = super()._create(model_class, *args, **kwargs)
        ret._password = cls._password
        return ret


class SuperUserFactory(UserFactory):
    username = factory.Sequence(lambda n: "superuser%03d@example.com" % n)
    email = factory.Sequence(lambda n: "superuser%03d@example.com" % n)
    is_superuser = True
    is_staff = True
    is_active = True


class FieldDefinitionFactory(AutoRegisterModelFactory):
    name = factory.Sequence(lambda d: "FieldDefinition-%s" % d)
    field_type = factory.fuzzy.FuzzyChoice([forms.CharField, forms.IntegerField])
    attrs = {}

    class Meta:
        model = FieldDefinition
        django_get_or_create = ("name",)


class FieldsetFactory(AutoRegisterModelFactory):
    name = factory.Sequence(lambda d: "Fieldset-%s" % d)

    class Meta:
        model = Fieldset
        django_get_or_create = ("name",)

    @factory.post_generation
    def fields(self, create, extracted, **kwargs):
        if not create:
            # Simple build, or nothing to add, do nothing.
            return
        if extracted:
            # Add the iterable of groups using bulk addition
            self.fields.add(*extracted)
        else:
            self.fields.add(FieldsetFieldFactory(fieldset=self))


class FieldsetFieldFactory(AutoRegisterModelFactory):
    name = factory.Sequence(lambda d: "FieldsetField-%s" % d)
    fieldset = factory.SubFactory(FieldsetFactory)
    field = factory.SubFactory(FieldDefinitionFactory)
    attrs = {}

    class Meta:
        model = FieldsetField
        django_get_or_create = ("name",)


class DataCheckerFactory(AutoRegisterModelFactory):
    name = factory.Sequence(lambda d: "DataChecker-%s" % d)

    class Meta:
        model = DataChecker
        django_get_or_create = ("name",)


class DataCheckerFieldsetFactory(AutoRegisterModelFactory):
    checker = factory.SubFactory(DataCheckerFactory)
    fieldset = factory.SubFactory(FieldsetFactory)
    prefix = "aaa"

    class Meta:
        model = DataCheckerFieldset
        django_get_or_create = ("checker", "prefix")
