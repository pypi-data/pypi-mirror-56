'''
This module presents instances for the OpenDSS Version 7 implementation. It is the classic version, without parallel machine functionality. If you want to handle parallel and distributed computations with third-party modules, this is the recommended version. It is also more stable and tested.
'''

from __future__ import absolute_import
from ._dss_capi_v7 import ffi, lib
from ._cffi_api_util import CffiApiUtil, use_com_compat, DssException
from . import dss_capi_gr, dss_capi_ir, enums
from .enums import *

# Bind to the FFI module instance for OpenDSS-v7
api_util = CffiApiUtil(ffi, lib) #: API utility functions and low-level access for the Version 7 library

DSS_GR = dss_capi_gr.IDSS(api_util) #: GR (Global Result) interface to the Version 7 library
DSS_IR = dss_capi_ir.IDSS(api_util) #: IR (Immediate Result) interface to the Version 7 library
DSS = DSS_GR #: Same as DSS_GR

#__all__ = ['DSS', 'DSS_GR', 'DSS_IR', 'api_util']