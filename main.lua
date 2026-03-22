local WindowMan = require("WindowMan")


local _VideoPlayer = VideoPlayers.CreatePlayer()
local starttime = os.time()
local endtime = os.time()*2
local PlayRandom
local timeremaining = 0
local timeelapsed = 0
local trackid = 0
local TrackInfo1
local TrackInfo2
local TrackInfo3
local WindowWidth = 220
local ButtonHeight = 30
local items = 6
local WindowHeight = ButtonHeight*(items+1)
local RootWindow = WindowMan.CreateWindow(WindowHeight, WindowWidth, WindowMan.GenericOnWindowClose, 40,40)
local DebugValuesShow = true
local itemindex = 0
local LibraryRootWin


local function randnum(max)
    return (math.floor((math.random()*max)+1))
end
local function LoadFile(filename)
    ---@diagnostic disable-next-line: param-type-mismatch
    if _VideoPlayer.IsPlaying then
        _VideoPlayer.Stop()
        VideoPlayers.ReleasePlayer(_VideoPlayer)
        _VideoPlayer = VideoPlayers.CreatePlayer()
    end
    _VideoPlayer.Load(filename, true)
    _VideoPlayer.Play()
end
local Play = function (id)    
    ---@diagnostic disable-next-line: param-type-mismatch
    local Library = loadfile(ScriptPath.."playlist.lua")()
    local song = id
    trackid = song
    local file = Library.Location.."/"..Library.files[song]
    local length = Library.lengths[song]
    RootWindow.Title = Library.titles[song] .. " - " .. Library.artists[song]
    TrackInfo1.Text = Library.titles[song]
    TrackInfo2.Text = Library.artists[song]
    TrackInfo3.Text = Library.albums[song]
    LoadFile(file)
    ---@diagnostic disable-next-line: cast-local-type, param-type-mismatch
    starttime = os.time()
    endtime = starttime + length
end


local function spawnPlaylistMenu()
    local LibraryMenu = loadfile(ScriptPath.."PlaylistMenu.lua")()
    if LibraryRootWin then
        WindowMan.DestroyWindow(LibraryRootWin)
    end
    LibraryRootWin = LibraryMenu.SpawnWindow(Play)
end



local PlaylistButton = WindowMan.CreateButton(0, itemindex*ButtonHeight,WindowWidth, ButtonHeight*1, "Open Library", RootWindow,spawnPlaylistMenu)
itemindex = itemindex+1
TrackInfo1 = WindowMan.CreateLabel(0, itemindex*ButtonHeight,WindowWidth, ButtonHeight, "aaaa", RootWindow)
itemindex = itemindex+1
TrackInfo2 = WindowMan.CreateLabel(0, itemindex*ButtonHeight,WindowWidth, ButtonHeight, "aaa", RootWindow)
itemindex = itemindex+1
TrackInfo3 = WindowMan.CreateLabel(0, itemindex*ButtonHeight,WindowWidth, ButtonHeight, "aa", RootWindow)
itemindex = itemindex+1


PlayRandom = function ()    
    ---@diagnostic disable-next-line: param-type-mismatch
    local Library = loadfile(ScriptPath.."playlist.lua")()
    local song = randnum(#Library.files)
    Play(song)
end
local DebugValuesLabel = WindowMan.CreateLabel(0,  itemindex*ButtonHeight-10, WindowWidth, ButtonHeight,"aaaaa", RootWindow)
DebugValuesLabel.IsVisible = DebugValuesShow
local TimeElapsedSlider = WindowMan.CreateSlider(0,  itemindex*ButtonHeight+(ButtonHeight/2), WindowWidth, ButtonHeight/2, RootWindow, 0, 1, .5)
TimeElapsedSlider.IsTargetable = false
TimeElapsedSlider.ValueDisplayFormat = ""
--TimeElapseSlider.IsInteractable = false
itemindex = itemindex+1
local function PlayPause()
    if not _VideoPlayer.IsReady then
        print("Video Player not ready!!")
        return
    end
    if _VideoPlayer.IsPlaying then
        local time = os.time()
        _VideoPlayer.Pause()
        timeremaining = endtime - time
        timeelapsed = time - starttime
        starttime = time - timeremaining
        endtime = time + timeremaining
        return
    end
    if _VideoPlayer.IsPaused then
        local time = os.time()
        _VideoPlayer.Play()
        timeremaining = endtime - time
        timeelapsed = time - starttime
        starttime = time - timeelapsed
        endtime = time + timeremaining
        return
    end
end

local function NextTrack()
    local Library = loadfile(ScriptPath.."playlist.lua")()
    local id = ((trackid+1)%(#Library.files+1))
    if id == 0 then
        id = id + 1
    end
    Play(id)
end

local function PrevTrack()
    local Library = loadfile(ScriptPath.."playlist.lua")()
    local id = trackid-1
    if id <= 0 then
        id = #Library.files
    end
    Play(id)
end
local PrevButton = WindowMan.CreateButton(0, itemindex*ButtonHeight, (WindowWidth/3)/2, ButtonHeight,"<", RootWindow, PrevTrack)
local PausePlayButton = WindowMan.CreateButton((WindowWidth/3)/2, itemindex*ButtonHeight, WindowWidth/3, ButtonHeight, "P", RootWindow, PlayPause) 
local NextButton = WindowMan.CreateButton(((WindowWidth/3)/2)+(WindowWidth/3), itemindex*ButtonHeight, (WindowWidth/3)/2, ButtonHeight,">", RootWindow, NextTrack)
local ConnectionButton = WindowMan.CreateButton((WindowWidth/3)+(WindowWidth/3), itemindex*ButtonHeight, WindowWidth/3, ButtonHeight,"R", RootWindow, PlayRandom)
if itemindex >=items then
    MessagePopupShow.Raise("Invalid Number of Indexes!")
    print("Error: Too many or too little elements")
    return
end

local lasttime = os.time()
function Update()
    local time = os.time()
    local timeOffset = math.floor(time/10000)*10000
    local humanReadable_starttime = math.floor((starttime - timeOffset)/1)
    local humanReadable_time = math.floor((time - timeOffset)/1)
    local humanReadable_endtime = math.floor((endtime - timeOffset)/1)
    local humanReadable_timeelapsed = math.floor((timeelapsed)/1)
    local humanReadable_timeremaining = math.floor((timeremaining)/1)
    if DebugValuesShow then
        DebugValuesLabel.Text = "".. trackid .. " : " .. humanReadable_starttime .. " : " .. humanReadable_endtime .. " : " .. humanReadable_time .. " : " .. humanReadable_timeelapsed  .. " : " .. humanReadable_timeremaining .. " : " .. (humanReadable_endtime - humanReadable_starttime) ..""
    end
    if time ~= lasttime then
        math.randomseed(time)
        lasttime = time
    end
    if _VideoPlayer.IsPaused then
        starttime = time - timeelapsed
        endtime = time + timeremaining
    end
    local V = (((endtime-starttime)-(endtime-time))/(endtime-starttime))
    TimeElapsedSlider.Value = V
    if V > 1 then
        NextTrack()
    end
end


function Cleanup()
    WindowMan.DestroyWindow(RootWindow)
    if LibraryRootWin then
        WindowMan.DestroyWindow(LibraryRootWin)
    end
    VideoPlayers.ReleasePlayer(_VideoPlayer)
end

