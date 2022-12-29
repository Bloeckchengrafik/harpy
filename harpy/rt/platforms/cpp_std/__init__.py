from harpy.rt.platforms.Platform import Platform
import harpy.rt.platforms.cpp_std.rtdefs as rtdefs

CPPSTD_RT = {}


class CPPStdPlatform(Platform):
    """The C++ Standard Library platform."""

    def get_global_rt(self):
        if not CPPSTD_RT:
            for rtdef in rtdefs.__dict__.values():
                if isinstance(rtdef, rtdefs.DynamicRT):
                    for provider in rtdef.provides():
                        CPPSTD_RT[provider] = rtdef

        return CPPSTD_RT
