# Copyright (c) 2012 CEF Python, see the Authors file.
# All rights reserved. Licensed under BSD 3-clause license.
# Project website: https://github.com/cztomczak/cefpython

include "../cefpython.pyx"
include "../browser.pyx"

cdef public cpp_bool DragHandler_OnDragEnter(
        CefRefPtr[CefBrowser] cefBrowser,
        CefRefPtr[CefDragData] cefDragData,
        uint32 mask
        ) except * with gil:
    
    cdef PyBrowser pyBrowser
    cdef object callback
    cdef DragData dragData
    try:
        pyBrowser = GetPyBrowser(cefBrowser, "OnDragEnter")
        callback = pyBrowser.GetClientCallback("OnDragEnter")
        dragData = DragData_Init(cefDragData)
        if callback:
            return bool(callback(browser=pyBrowser, dragData=dragData, mask=mask))
        return False
    except:
        (exc_type, exc_value, exc_trace) = sys.exc_info()
        sys.excepthook(exc_type, exc_value, exc_trace)


cdef public void DragHandler_OnDraggableRegionsChanged(
        CefRefPtr[CefBrowser] cefBrowser,
        cpp_vector[CefDraggableRegion]& cefRegions
        ) except * with gil:
    cdef PyBrowser pyBrowser
    cdef object callback
    cdef list region;
    cdef list regions = []
    cdef CefDraggableRegion cefRegion;
    cdef cpp_vector[CefDraggableRegion].iterator iterator
    try:
        pyBrowser = GetPyBrowser(cefBrowser, "OnDraggableRegionsChanged")
        callback = pyBrowser.GetClientCallback("OnDraggableRegionsChanged")
        
        iterator = cefRegions.begin()
        while iterator != cefRegions.end():
            cefRegion = deref(iterator)
            region = [ cefRegion.bounds, cefRegion.draggable ]
            regions.append(region)
            preinc(iterator)

        if callback:
            callback(browser=pyBrowser, regions=regions)
    except:
        (exc_type, exc_value, exc_trace) = sys.exc_info()
        sys.excepthook(exc_type, exc_value, exc_trace)