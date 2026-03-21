local WindowMan = require("WindowMan")

local Menu = {}

function Menu.SpawnWindow(LoadFileFunc)
    local playlist = loadfile(ScriptPath.."playlist.lua")()
    local items = #playlist.files
    local itemheight = 25
    local windowheight = 30+(itemheight*items)
    local windowwidth = 200
    local Rootwindow = WindowMan.CreateWindow(windowheight, windowwidth, WindowMan.GenericCloseNoExit,180,40)
    for song, file in ipairs(playlist.files) do
        local function dummyloadfile()
            LoadFileFunc(song)
        end
        local button = WindowMan.CreateButton(0, (song-1)*itemheight, windowwidth, itemheight, playlist.titles[song], Rootwindow, dummyloadfile)
    end
    return Rootwindow
end

return Menu