from abc import ABCMeta, abstractmethod
from typing import List


class PackageRepository(metaclass=ABCMeta):
    @abstractmethod
    def require_package(self, name: str):
        pass

    @abstractmethod
    def get_required_packages(self) -> List[str]:
        pass

    @abstractmethod
    def unrequire_package(self, name: str):
        pass