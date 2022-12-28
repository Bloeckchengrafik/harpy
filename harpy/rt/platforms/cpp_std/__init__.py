from harpy.rt.platforms.Platform import Platform
from harpy.rt.platforms.cpp_std.builtins import *

CPPSTD_RT = {
    "print": RTPrint(),
}


class CPPStdPlatform(Platform):
    """The C++ Standard Library platform."""

    def get_global_rt(self):
        return CPPSTD_RT
