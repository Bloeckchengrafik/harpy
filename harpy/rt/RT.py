from abc import ABC, abstractmethod


class RT(ABC):
    """
    Base class for all runtime functions.
    """
    @abstractmethod
    def depends(self) -> list:
        """
        Return a list of dependencies for this runtime function.
        """
        raise NotImplementedError

    @abstractmethod
    def cpp(self) -> str:
        """
        Return the C++ source code for this runtime function.
        """
        raise NotImplementedError

    @abstractmethod
    def hpp(self) -> str:
        """
        Return the C++ header code for this runtime function.
        """
        raise NotImplementedError
