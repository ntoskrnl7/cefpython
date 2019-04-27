// Copyright (c) 2012 CEF Python, see the Authors file.
// All rights reserved. Licensed under BSD 3-clause license.
// Project website: https://github.com/cztomczak/cefpython

#include "drag_handler.h"

bool DragHandler::OnDragEnter(CefRefPtr<CefBrowser> browser,
                         CefRefPtr<CefDragData> dragData,
                         DragOperationsMask mask)
{
    REQUIRE_UI_THREAD();

    return DragHandler_OnDragEnter(browser, dragData, mask);
}

void DragHandler::OnDraggableRegionsChanged(
      CefRefPtr<CefBrowser> browser,
      const std::vector<CefDraggableRegion>& regions)
{
    REQUIRE_UI_THREAD();
    DragHandler_OnDraggableRegionsChanged(browser, const_cast<std::vector<CefDraggableRegion>&>(regions));
}