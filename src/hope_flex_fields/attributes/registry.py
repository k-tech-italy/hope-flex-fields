from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from strategy_field.registry import Registry

if TYPE_CHECKING:
    from hope_flex_fields.models import FieldDefinition


class AttributesHandlerRegistry(Registry):
    pass


class AbstractAttributeHandler(ABC):
    def __init__(self, context: "FieldDefinition"):
        self.context = context

    @abstractmethod
    def get(self) -> dict: ...

    @abstractmethod
    def set(self, value: dict) -> None: ...


class BaseAttributeHandler(AbstractAttributeHandler):
    def get(self) -> dict:
        return self.context.attrs

    def set(self, value: dict) -> None:
        self.context.attrs = value


attributes_handler_registry = AttributesHandlerRegistry(AbstractAttributeHandler)

attributes_handler_registry.register(BaseAttributeHandler)
