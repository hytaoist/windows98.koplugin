-- Lightweight test for the plugin menus and WeChat sponsor dialog.

local shown_widget
local copied_text
local opened_url

local function extend_class(parent, options)
    options = options or {}
    options.__index = options
    return setmetatable(options, { __index = parent })
end

package.preload["ui/widget/confirmbox"] = function()
    return {}
end

package.preload["datastorage"] = function()
    return {
        getSettingsDir = function() return "/tmp" end,
    }
end

package.preload["device"] = function()
    return {
        canOpenLink = function() return false end,
        openLink = function(_, url) opened_url = url end,
        input = {
            setClipboardText = function(_, text) copied_text = text end,
        },
    }
end

package.preload["ui/widget/infomessage"] = function()
    local InfoMessage = {}
    function InfoMessage:new(options)
        options.is_info_message = true
        return options
    end
    return InfoMessage
end

package.preload["luasettings"] = function()
    local LuaSettings = {}
    function LuaSettings:open()
        return {
            readSetting = function() end,
            saveSetting = function() end,
            delSetting = function() end,
            flush = function() end,
        }
    end
    return LuaSettings
end

package.preload["ui/uimanager"] = function()
    return {
        show = function(_, widget) shown_widget = widget end,
        close = function() shown_widget = nil end,
        nextTick = function(_, callback) callback() end,
        scheduleIn = function(_, _, callback) callback() end,
        askForRestart = function() end,
    }
end

package.preload["ui/widget/container/widgetcontainer"] = function()
    local WidgetContainer = {}
    WidgetContainer.extend = extend_class
    return WidgetContainer
end

package.preload["ffi/util"] = function()
    return {
        template = function(text, ...)
            local values = { ... }
            return (text:gsub("%%(%d+)", function(index)
                return tostring(values[tonumber(index)] or "")
            end))
        end,
    }
end

package.preload["logger"] = function()
    return { warn = function() end }
end

package.preload["gettext"] = function()
    return function(text) return text end
end

package.preload["ui/widget/buttondialog"] = function()
    local ButtonDialog = {}
    function ButtonDialog:new(options)
        options.is_button_dialog = true
        return options
    end
    return ButtonDialog
end

package.preload["ui/widget/qrmessage"] = function()
    local QRMessage = {}
    function QRMessage:new(options)
        options.is_qr_message = true
        return options
    end
    return QRMessage
end

package.preload["ui/widget/imageviewer"] = function()
    local ImageViewer = {}
    function ImageViewer:new(options)
        options.is_image_viewer = true
        return options
    end
    return ImageViewer
end

local Device = require("device")
local Windows98 = assert(loadfile(arg[1] or "plugin/main.lua"))()
local plugin = Windows98:extend{
    path = "plugin",
    version = "1.0.0",
    github = "hytaoist/windows98.koplugin",
    sponsor_url = nil,
    wechat_reward_path = "assets/sponsor/wechat-reward.jpg",
    deploy = {
        deployed_version = function() return "1.0.0" end,
    },
}

local function find_button(dialog, label)
    for _, row in ipairs(dialog.buttons or {}) do
        for _, button in ipairs(row) do
            if button.text == label then return button end
        end
    end
end

plugin:showAbout()
assert(shown_widget and shown_widget.is_button_dialog, "About did not open a button dialog")
assert(shown_widget.title:find("Windows 98 for KOReader", 1, true),
    "About is missing the Windows 98 product name")
assert(shown_widget.title:find("103 KOReader icons", 1, true),
    "About is missing the icon count")
assert(shown_widget.title:find("Windows98UI", 1, true),
    "About is missing the font family")
local sponsor_button = assert(
    find_button(shown_widget, "Sponsor this project"),
    "About is missing the sponsor module"
)

sponsor_button.callback()
assert(shown_widget and shown_widget.is_button_dialog, "Sponsor dialog did not open")
local wechat_button = assert(
    find_button(shown_widget, "Show WeChat reward code"),
    "WeChat reward button missing"
)
assert(find_button(shown_widget, "Show QR code") == nil,
    "URL QR button should be hidden for the WeChat-only configuration")
assert(find_button(shown_widget, "Copy link") == nil,
    "Copy button should be hidden for the WeChat-only configuration")
assert(find_button(shown_widget, "Open sponsor page in browser") == nil,
    "Browser button should be hidden for the WeChat-only configuration")

wechat_button.callback()
assert(shown_widget and shown_widget.is_image_viewer, "WeChat reward image did not open")
assert(shown_widget.file == plugin.wechat_reward_path,
    "WeChat reward image has the wrong path")
assert(shown_widget.fullscreen == true, "WeChat reward image should use fullscreen mode")
assert(shown_widget.with_title_bar == true, "WeChat reward image needs its close title bar")
assert(shown_widget.title_text == "WeChat reward code",
    "WeChat reward image has the wrong title")

plugin.sponsor_url = "https://example.com/sponsor"
plugin:showSponsor()
wechat_button = assert(
    find_button(shown_widget, "Show WeChat reward code"),
    "WeChat reward button missing with an optional sponsor URL"
)
local qr_button = assert(find_button(shown_widget, "Show QR code"), "Sponsor QR button missing")
local copy_button = assert(find_button(shown_widget, "Copy link"), "Sponsor copy button missing")
qr_button.callback()
assert(shown_widget and shown_widget.is_qr_message, "Sponsor QR code did not open")
assert(shown_widget.text == plugin.sponsor_url, "Sponsor QR code has the wrong URL")

plugin:showSponsor()
copy_button = assert(find_button(shown_widget, "Copy link"), "Sponsor copy button missing")
copy_button.callback()
assert(copied_text == plugin.sponsor_url, "Sponsor link was not copied")
assert(shown_widget and shown_widget.is_info_message, "Copy confirmation was not shown")

Device.canOpenLink = function() return true end
plugin:showSponsor()
local browser_button = assert(
    find_button(shown_widget, "Open sponsor page in browser"),
    "Browser button is missing on capable devices"
)
browser_button.callback()
assert(opened_url == plugin.sponsor_url, "Sponsor page was not opened")

plugin.sponsor_url = nil
plugin:showSponsor()
wechat_button = assert(
    find_button(shown_widget, "Show WeChat reward code"),
    "WeChat reward button missing without a sponsor URL"
)
wechat_button.callback()
assert(shown_widget and shown_widget.is_image_viewer,
    "Image-only sponsor configuration did not open the WeChat reward code")

local menu_items = {}
plugin:addToMainMenu(menu_items)
assert(menu_items.windows98.text == "Windows 98 for KOReader",
    "Tools menu uses the wrong product name")
assert(menu_items.windows95 == nil, "Legacy Windows 95 menu key is still present")

print("main test OK")
