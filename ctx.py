from dataclasses import dataclass

@dataclass
class Ctx:
    ...

ctx: Ctx = Ctx()

def app_ctx():
    global ctx
    return ctx
