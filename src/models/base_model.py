"""Contrato base para modelos de Machine Learning."""

from abc import ABC, abstractmethod
from typing import Any


class BaseModel(ABC):
    @abstractmethod
    def fit(self, features: Any, target: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def predict(self, features: Any) -> Any:
        raise NotImplementedError