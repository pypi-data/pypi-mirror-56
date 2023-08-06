import warnings as _warnings

try:
    from modelbase_pde import *
except ImportError:
    _warnings.warn("Could not find pde subpackage. Did you install modelbase_pde?")
except ModuleNotFoundError:
    _warnings.warn("Could not find pde subpackage. Did you install modelbase_pde?")
