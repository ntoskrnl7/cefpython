# Copyright (c) 2016 CEF Python, see the Authors file.
# All rights reserved. Licensed under BSD 3-clause license.
# Project website: https://github.com/cztomczak/cefpython

from libcpp cimport bool as cpp_bool
from cef_string cimport CefString
from cef_ptr cimport CefRefPtr
from cef_image cimport CefImage
from cef_types cimport CefPoint
from libcpp.vector cimport vector as cpp_vector

cdef extern from "include/cef_drag_data.h":
    cdef cppclass CefDragData:
        cpp_bool IsLink()
        cpp_bool IsFragment()
        cpp_bool IsFile()
        CefString GetLinkURL()
        CefString GetLinkTitle()
        CefString GetFragmentText()
        CefString GetFragmentHtml()
        CefString GetFragmentBaseURL()
        CefString GetFileName()
        cpp_bool GetFileNames(cpp_vector[CefString]& names)
        void SetFragmentText(const CefString& text)
        void SetFragmentHtml(const CefString& html)
        void SetFragmentBaseURL(const CefString& base_url)
        cpp_bool HasImage()
        CefRefPtr[CefImage] GetImage()
        CefPoint GetImageHotspot()


    cdef CefRefPtr[CefDragData] CefDragData_Create "CefDragData::Create"()
