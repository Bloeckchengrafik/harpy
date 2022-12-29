import json
import os
from rich import print


class RT:
    """
    Base class for all runtime functions.
    """

    def depends(self) -> list:
        """
        Return a list of dependencies for this runtime function.
        """
        raise NotImplementedError

    def cpp(self) -> str:
        """
        Return the C++ source code for this runtime function.
        """
        raise NotImplementedError

    def hpp(self) -> str:
        """
        Return the C++ header code for this runtime function.
        """
        raise NotImplementedError

    def provides(self) -> list:
        """
        Return a list of symbols provided by this runtime function.
        """
        return []


class DynamicRT(RT):
    """
    Dynamically load a runtime function from a file.
    """

    def __init__(self, path: str, platform_rtdefs_file):
        basepath = os.path.join(os.path.dirname(platform_rtdefs_file), "platform", path)

        self._deps = []
        self._provides = []
        self._cpp = ""
        self._hpp = ""

        # Enumerate all files in the directory
        for filename in os.listdir(basepath):
            if filename.endswith(".cpp"):
                with open(os.path.join(basepath, filename), "r") as f:
                    self._cpp += f.read() + "\n"

            elif filename.endswith(".hpp") or filename.endswith(".h"):
                with open(os.path.join(basepath, filename), "r") as f:
                    self._hpp += f.read() + "\n"

            elif filename.endswith(".deps.json"):
                with open(os.path.join(basepath, filename), "r") as f:
                    self._deps += json.load(f)

            elif filename.endswith(".provides.json"):
                with open(os.path.join(basepath, filename), "r") as f:
                    self._provides += json.load(f)

        if len(self._provides) == 0:
            self._provides = [os.path.splitext(path)[-2]]

    def depends(self) -> list:
        return self._deps

    def cpp(self) -> str:
        return self._cpp

    def hpp(self) -> str:
        return self._hpp

    def provides(self) -> list:
        return self._provides

