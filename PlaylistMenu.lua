local WindowMan = require("WindowMan")

local Menu = {}

function Menu.SpawnWindow(LoadFileFunc)
    local playlist = loadfile(ScriptPath.."playlist.lua")()
    local items = #playlist.files
    if items > 8 then
        items = 8
    end
    local itemheight = 25
    local windowheight = 30+(itemheight*items)
    local windowwidth = 200
    local Rootwindow = WindowMan.CreateWindow(windowheight, windowwidth, WindowMan.GenericCloseNoExit,180,40)
    --TODO ADD SCROLL VIEWS TO WINDOWMAN
    local verticalScrollView = Rootwindow.CreateVerticalScrollView()
    verticalScrollView.AutoResize = false
    verticalScrollView.SetAlignment( align_HorizEdges, 0, 0 )
    verticalScrollView.SetAlignment( align_VertEdges, 0, 0 )
    for song, file in ipairs(playlist.files) do
        local function dummyloadfile()
            LoadFileFunc(song)
        end
        local button = WindowMan.CreateButton(0, (song-1)*itemheight, windowwidth, itemheight, playlist.titles[song], verticalScrollView, dummyloadfile)
    end
    verticalScrollView.ContainerSize = itemheight*(#playlist.files)
    return Rootwindow
end

return Menu