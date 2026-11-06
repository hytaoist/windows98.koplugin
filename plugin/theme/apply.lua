-- Windows 98 runtime for KOReader.
--
-- This file is copied into KOReader's stable theme data directory by the
-- windows98.koplugin. The installed patch is intentionally tiny and only
-- loads this runtime, so Storefront can replace the plugin while the user patch
-- remains stable.

local logger = require("logger")

if G_reader_settings:isFalse("windows98_enabled") then
    logger.info("Windows98: disabled by settings.reader.lua")
    return
end

if _G._windows98_theme_loaded then
    logger.info("Windows98: theme runtime already loaded")
    return
end
_G._windows98_theme_loaded = true

local UI_FONT_FILE = "Windows98UI.ttf"
local UI_FONT_BOLD_FILE = "Windows98UI-Bold.ttf"
local FONT_SLOTS = {
    "cfont",
    "tfont",
    "smalltfont",
    "x_smalltfont",
    "ffont",
    "smallffont",
    "largeffont",
    "rifont",
    "pgfont",
    "hfont",
    "infofont",
    "smallinfofont",
    "smallinfofontbold",
    "x_smallinfofont",
    "xx_smallinfofont",
}
local BOLD_FONT_SLOTS = {
    "tfont",
    "smalltfont",
    "x_smalltfont",
    "smallinfofontbold",
}

local function apply_ui_font()
    local Font = require("ui/font")
    local FontList = require("fontlist")
    local lfs = require("libs/libkoreader-lfs")
    local font_path = FontList.fontdir .. "/" .. UI_FONT_FILE
    if lfs.attributes(font_path, "mode") ~= "file" then
        return false, font_path
    end

    local bold_path = FontList.fontdir .. "/" .. UI_FONT_BOLD_FILE
    local has_bold = lfs.attributes(bold_path, "mode") == "file"
    for _index, slot in ipairs(FONT_SLOTS) do
        Font.fontmap[slot] = UI_FONT_FILE
    end
    if has_bold then
        for _index, slot in ipairs(BOLD_FONT_SLOTS) do
            Font.fontmap[slot] = UI_FONT_BOLD_FILE
        end
        Font.bold_font_variant = Font.bold_font_variant or {}
        Font.regular_font_variant = Font.regular_font_variant or {}
        Font.bold_font_variant[UI_FONT_FILE] = UI_FONT_BOLD_FILE
        Font.regular_font_variant[UI_FONT_BOLD_FILE] = UI_FONT_FILE
    end
    return true
end

local function refresh_titlebar_faces()
    local ok_tb, TitleBar = pcall(require, "ui/widget/titlebar")
    if not ok_tb or not TitleBar then return end
    local Font = require("ui/font")
    local slots = {
        { field = "title_face_fullscreen",     face = "smalltfont" },
        { field = "title_face_not_fullscreen", face = "x_smalltfont" },
        { field = "subtitle_face",             face = "xx_smallinfofont" },
        { field = "info_text_face",            face = "x_smallinfofont" },
    }
    for _index, slot in ipairs(slots) do
        local ok_face, face = pcall(Font.getFace, Font, slot.face)
        if ok_face and face then
            TitleBar[slot.field] = face
        end
    end
end

local function apply_simpleui_tokens()
    local ok, SimpleUIStyle = pcall(require, "features/sui_style")
    if not ok or type(SimpleUIStyle) ~= "table" then
        return false
    end
    local Screen = require("device").screen
    local Blitbuffer = require("ffi/blitbuffer")
    local light_gray = Blitbuffer.COLOR_LIGHT_GRAY
        or Blitbuffer.COLOR_DARK_GRAY
        or Blitbuffer.COLOR_WHITE
    local dark_gray = Blitbuffer.COLOR_DARK_GRAY or Blitbuffer.COLOR_BLACK
    SimpleUIStyle.BORDER_SZ = math.max(2, math.floor(Screen:scaleBySize(2)))
    if type(SimpleUIStyle.COLOR) == "table" then
        SimpleUIStyle.COLOR.text_primary = Blitbuffer.COLOR_BLACK
        SimpleUIStyle.COLOR.text_dim = dark_gray
        SimpleUIStyle.COLOR.surface = light_gray
        SimpleUIStyle.COLOR.surface_gray = light_gray
        SimpleUIStyle.COLOR.gray = dark_gray
        SimpleUIStyle.COLOR.gray_strong = Blitbuffer.COLOR_BLACK
    end
    return true
end

local function apply_theme()
    local Blitbuffer = require("ffi/blitbuffer")
    local Device = require("device")
    local Screen = Device.screen
    local Size = require("ui/size")

    local white = Blitbuffer.COLOR_WHITE
    local black = Blitbuffer.COLOR_BLACK
    local silver = Blitbuffer.COLOR_LIGHT_GRAY
        or Blitbuffer.COLOR_DARK_GRAY
        or white
    local shadow = Blitbuffer.COLOR_DARK_GRAY or black
    local titlebar = Blitbuffer.COLOR_DARK_GRAY or black
    local unit = math.max(1, math.floor(Screen:scaleBySize(1)))
    local rule = math.max(1, math.floor(Screen:scaleBySize(1)))
    local edge = math.max(2, unit * 2)

    local has_ui_font, font_path = apply_ui_font()
    if not has_ui_font then
        logger.warn("Windows98: font not found at", font_path, "- using stock UI font")
    end

    Size.border.default = rule
    Size.border.button = edge
    Size.border.window = edge
    Size.line.thick = math.max(2, edge)
    Size.radius.default = 0
    Size.radius.window = 0
    Size.radius.button = 0

    local function paint_button_bevel(bb, x, y, w, h, sunken)
        x, y, w, h = math.floor(x), math.floor(y), math.floor(w), math.floor(h)
        if w <= unit * 6 or h <= unit * 6 then return end
        local outer_high = sunken and shadow or white
        local outer_low = sunken and white or shadow
        local inner_high = sunken and black or white
        local inner_low = sunken and white or black

        bb:paintRect(x, y, w, unit, outer_high)
        bb:paintRect(x, y, unit, h, outer_high)
        bb:paintRect(x, y + h - unit, w, unit, outer_low)
        bb:paintRect(x + w - unit, y, unit, h, outer_low)

        bb:paintRect(x + unit, y + unit, w - unit * 2, unit, inner_high)
        bb:paintRect(x + unit, y + unit, unit, h - unit * 2, inner_high)
        bb:paintRect(x + unit, y + h - unit * 2, w - unit * 2, unit, inner_low)
        bb:paintRect(x + w - unit * 2, y + unit, unit, h - unit * 2, inner_low)
    end

    local function paint_raised_box(bb, x, y, w, h)
        x, y, w, h = math.floor(x), math.floor(y), math.floor(w), math.floor(h)
        if w < edge * 2 or h < edge * 2 then return end
        bb:paintRect(x, y, w, h, silver)
        paint_button_bevel(bb, x, y, w, h, false)
    end

    local FrameContainer = require("ui/widget/container/framecontainer")
    FrameContainer.bordersize = edge
    FrameContainer.radius = 0
    FrameContainer.color = black
    FrameContainer.focus_border_size = edge
    FrameContainer.focus_border_color = black

    local orig_frame_new = FrameContainer.new
    FrameContainer.new = function(class, options)
        if type(options) == "table" then
            options.radius = 0
        end
        return orig_frame_new(class, options)
    end

    local orig_frame_paint = FrameContainer.paintTo
    FrameContainer.paintTo = function(self, bb, x, y)
        local result = orig_frame_paint(self, bb, x, y)
        if not self.dimen or (self.bordersize or 0) <= 0 then return result end
        local w, h = self.dimen.w or 0, self.dimen.h or 0
        if w < edge * 6 or h < edge * 5 then return result end
        if w >= Screen:getWidth() * 0.995 or h >= Screen:getHeight() * 0.995 then
            return result
        end

        local is_dialog = w > Screen:getWidth() * 0.30
            and w < Screen:getWidth() * 0.98
            and h > Screen:scaleBySize(70)
            and h < Screen:getHeight() * 0.98
        if G_reader_settings:nilOrTrue("windows98_shadows") and is_dialog then
            local offset = math.max(2, math.floor(Screen:scaleBySize(2)))
            bb:paintRect(
                math.floor(x + w),
                math.floor(y + offset),
                offset,
                math.floor(h - offset),
                black
            )
            bb:paintRect(
                math.floor(x + offset),
                math.floor(y + h),
                math.floor(w - offset),
                offset,
                black
            )
        end
        paint_button_bevel(bb, x, y, w, h, false)
        return result
    end

    local TitleBar = require("ui/widget/titlebar")
    TitleBar.align = "center"
    TitleBar.button_padding = Screen:scaleBySize(7)
    TitleBar.title_h_padding = Size.padding.large
    TitleBar.left_icon_size_ratio = 0.62
    TitleBar.right_icon_size_ratio = 0.62
    refresh_titlebar_faces()

    local function paint_titlebar_control(bb, button, x, y, bar_width)
        if not button or not button.dimen or not button.image then return end
        local icon_w = button.image.width or button.width or 0
        local icon_h = button.image.height or button.height or 0
        if icon_w <= 0 or icon_h <= 0 then return end
        local pad_left = button.padding_left or 0
        local pad_top = button.padding_top or 0
        local control_x
        if button.overlap_align == "right" then
            control_x = x + bar_width - button.dimen.w + pad_left
        else
            control_x = x + pad_left
        end
        paint_raised_box(bb, control_x, y + pad_top, icon_w, icon_h)
    end

    local orig_titlebar_init = TitleBar.init
    TitleBar.init = function(self, ...)
        refresh_titlebar_faces()
        local result = orig_titlebar_init(self, ...)
        local face_slots = {
            { widget = self.title_widget, face = "x_smalltfont" },
            { widget = self.subtitle_widget, face = "xx_smallinfofont" },
        }
        local Font = require("ui/font")
        local titlebar_enabled = G_reader_settings:nilOrTrue("windows98_titlebar")
        for _index, slot in ipairs(face_slots) do
            if slot.widget then
                slot.widget.fgcolor = titlebar_enabled and white or black
                local ok_face, face = pcall(Font.getFace, Font, slot.face)
                if ok_face and face then slot.widget.face = face end
            end
        end
        return result
    end

    local orig_titlebar_paint = TitleBar.paintTo
    TitleBar.paintTo = function(self, bb, x, y)
        if self.dimen and G_reader_settings:nilOrTrue("windows98_titlebar") then
            local x0, y0 = math.floor(x), math.floor(y)
            local w = math.floor(self.width or self.dimen.w)
            local h = math.floor(self.titlebar_height or self.dimen.h)
            bb:paintRect(x0, y0, w, h, titlebar)
            bb:paintRect(x0, y0, w, rule, white)
            bb:paintRect(x0, y0 + h - rule, w, rule, black)
            paint_titlebar_control(bb, self.left_button, x0, y0, w)
            paint_titlebar_control(bb, self.right_button, x0, y0, w)
        end
        return orig_titlebar_paint(self, bb, x, y)
    end

    local Button = require("ui/widget/button")
    Button.bordersize = edge
    Button.radius = 0
    Button.padding = Size.padding.button
    Button.text_font_face = "cfont"
    Button.text_font_bold = false

    local orig_button_init = Button.init
    Button.init = function(self, ...)
        orig_button_init(self, ...)
        if self.frame then
            self.frame.background = silver
            self.frame.color = black
            self.frame.radius = 0
        end
    end

    local orig_button_paint = Button.paintTo
    Button.paintTo = function(self, bb, x, y)
        local result = orig_button_paint(self, bb, x, y)
        if self.frame and self.frame.dimen and not self.frame.invert then
            local dimen = self.frame.dimen
            paint_button_bevel(
                bb,
                dimen.x or x,
                dimen.y or y,
                dimen.w or 0,
                dimen.h or 0,
                false
            )
        end
        return result
    end

    -- Some widgets briefly exist without a laid-out frame/image. KOReader's
    -- flash_ui path assumes a geometry and crashes while indexing dimen.
    -- Keep normal feedback, but skip only the unavailable visual highlight.
    if not Button._windows98_flash_guard then
        Button._windows98_flash_guard = true
        local orig_feedback_highlight = Button._doFeedbackHighlight
        local orig_feedback_unhighlight = Button._undoFeedbackHighlight
        Button._doFeedbackHighlight = function(self, ...)
            local frame = self and self[1]
            if not frame or not frame.dimen then return end
            return orig_feedback_highlight(self, ...)
        end
        Button._undoFeedbackHighlight = function(self, ...)
            local frame = self and self[1]
            if not frame or not frame.dimen then return end
            return orig_feedback_unhighlight(self, ...)
        end
    end

    local ok_icon_button, IconButton = pcall(require, "ui/widget/iconbutton")
    if ok_icon_button and type(IconButton) == "table" and not IconButton._windows98_flash_guard then
        IconButton._windows98_flash_guard = true
        local orig_icon_tap = IconButton.onTapIconButton
        IconButton.onTapIconButton = function(self)
            if not self.callback then return end
            local flash_enabled = not G_reader_settings:isFalse("flash_ui") and self.allow_flash
            if flash_enabled and (not self.dimen or not self.image or not self.image.dimen) then
                self.callback()
                return true
            end
            return orig_icon_tap(self)
        end
    end

    local ButtonTable = require("ui/widget/buttontable")
    ButtonTable.sep_width = math.max(2, edge)
    local orig_add_vertical_separator = ButtonTable.addVerticalSeparator
    ButtonTable.addVerticalSeparator = function(self)
        return orig_add_vertical_separator(self, true)
    end

    local TouchMenu = require("ui/widget/touchmenu")
    TouchMenu.split_color = black
    TouchMenu.split_height = math.max(2, edge)
    local userpatch = require("userpatch")
    local TouchMenuBar = select(1, userpatch.getUpValue(TouchMenu.init, "TouchMenuBar"))
    if TouchMenuBar and not TouchMenuBar._windows98_bar then
        TouchMenuBar._windows98_bar = true
        local orig_menubar_paint = TouchMenuBar.paintTo
        TouchMenuBar.paintTo = function(self, bb, x, y)
            local w = math.floor(self.width or (self.dimen and self.dimen.w) or Screen:getWidth())
            local h = math.floor(self.height or (self.dimen and self.dimen.h) or 0)
            if h > 0 then
                local x0, y0 = math.floor(x), math.floor(y)
                bb:paintRect(x0, y0, w, h, silver)
                bb:paintRect(x0, y0, w, rule, white)
                bb:paintRect(x0, y0 + h - rule * 2, w, rule, shadow)
                bb:paintRect(x0, y0 + h - rule, w, rule, black)
            end
            return orig_menubar_paint(self, bb, x, y)
        end
    end

    local Menu = require("ui/widget/menu")
    Menu.line_color = shadow

    logger.info("Windows98: Windows 98 theme applied",
        has_ui_font and "(Windows98UI)" or "(stock UI font)")
end

local ok, err = pcall(apply_theme)
if not ok then
    logger.warn("Windows98: theme failed:", err)
end

-- SimpleUI applies its saved UI font after instantiation. Reassert the Windows
-- 98 UI fonts afterwards and update the few style tokens read at build time.
local userpatch = require("userpatch")
if type(userpatch.registerPatchPluginFunc) == "function" then
    pcall(userpatch.registerPatchPluginFunc, "simpleui", function()
        local ok_simpleui, err_simpleui = pcall(function()
            apply_ui_font()
            refresh_titlebar_faces()
            apply_simpleui_tokens()
        end)
        if not ok_simpleui then
            logger.warn("Windows98: SimpleUI integration failed:", err_simpleui)
        end
    end)
end
