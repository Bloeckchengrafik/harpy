from harpy.rt.RT import DynamicRT


def _(path: str):
    return DynamicRT(path, __file__)


RTPrint = _("print")
RTInput = _("input")
