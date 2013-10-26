-- Standard awesome library
require("awful")
require("awful.autofocus")
require("awful.rules")
require("flaw.helper")
-- Theme handling library
require("beautiful")
-- Notification library
require("naughty")
require("shifty")

local vicious = require("vicious")
local hostname = io.lines('/proc/sys/kernel/hostname')()
homedir = os.getenv("HOME")

require("aweror")
local lasttag = require("lasttag")
local mousecoords = require("mousecoords")
local tagviewonly = require("tagviewonly")

function dbg(vars)
    local text = ""
    for i=1, #vars do text = text .. vars[i] .. " | " end
    naughty.notify({ text = text, timeout = 0 })
end

-- widgets!

newmailwidget = {}
newmailwidget.iconwidget = widget ({type = 'imagebox', name = 'newmailwidget-image'})
newmailwidget.textwidget = widget ({ type = 'textbox', name = 'newmailwidget-text' })
newmailwidget.newimage = image (awful.util.getdir ("config") .. "/icons/newmail.png")
newmailwidget.noimage = image (awful.util.getdir ("config") .. "/icons/nomail.png")
newmailwidget.update = function () os.execute ("unread.py &") end
newmailwidget.callback = function (count)

  if count > 0 then
    newmailwidget.textwidget.text = ' ' .. count .. ' '
    newmailwidget.iconwidget.image = newmailwidget.newimage
  else
    newmailwidget.textwidget.text = ''
    newmailwidget.iconwidget.image = newmailwidget.noimage
  end

end

newmailwidget.timer = timer ({ timeout = 60 })
newmailwidget.timer:add_signal ("timeout", function () newmailwidget.update () end)
newmailwidget.timer:start ()
newmailwidget.update ()

rsscountwidget = {}
rsscountwidget.textwidget = widget ({type = 'textbox', name = 'rsscount-text'})
rsscountwidget.iconwidget = widget ({type = 'imagebox', name = 'rsscount-image'})
rsscountwidget.image = image (awful.util.getdir ("config") .. "/icons/rss.png")
rsscountwidget.update = function () os.execute ("rss.py &") end
rsscountwidget.callback = function (count)

  if count > 0 then
    rsscountwidget.textwidget.text = ' ' .. count .. ' '
    rsscountwidget.iconwidget.image = rsscountwidget.image
  else
    rsscountwidget.textwidget.text = ''
    rsscountwidget.iconwidget.image = nil
  end

end

volumewidget = {}
volumewidget.iconwidget = widget ({ type = 'imagebox', name = 'volume-icon-widget' })
volumewidget.textwidget = widget ({type = 'textbox', name = 'volumewidget'})
volumewidget.start = function () os.execute ("volume_notification &") end
volumewidget.callback = function (volume, mute, name)

  volumewidget.iconwidget.image = image (awful.util.getdir ("config") .. "/icons/" .. name .. ".png")

  if mute == true then
    volumewidget.textwidget.text = ' <span color="#666666">' .. volume .. '%</span> '
  else
    volumewidget.textwidget.text = ' <span color="#dcdccc">' .. volume .. '%</span> '
  end

end

volumewidget.start ()

if hostname == "shodan" then

  rsscountwidget.timer = timer ({ timeout = 60 })
  rsscountwidget.timer:add_signal ("timeout", function () rsscountwidget.update () end)
  rsscountwidget.timer:start ()
  rsscountwidget.update ()

end

batterywidget = {}
batterywidget.textwidget = nil
batterywidget.iconwidget = nil

if hostname == "daedalus" then

  batterywidget.textwidget = widget ({type = 'textbox', name = 'batterywidget-text'})
  batterywidget.iconwidget = widget ({type = 'imagebox', name = 'batterywidget-image'})
  batterywidget.update = function () os.execute ("battery-status update &") end
  batterywidget.callback = function (percent, name)
    batterywidget.iconwidget.image = image (awful.util.getdir ("config") .. "/icons/" .. name .. ".png")
    batterywidget.textwidget.text = percent .. "% "
  end

  batterywidget.timer = timer ({ timeout = 60 })
  batterywidget.timer:add_signal ("timeout", function () batterywidget.update () end)
  batterywidget.timer:start ()

  batterywidget.update ()

end

thermal = widget({ type = "textbox" })

cpuwidget = widget({ type = "textbox" })
vicious.register(cpuwidget, vicious.widgets.cpu, ' <span color="#f0edd4">CPU:</span> $1%', 10)

-- Initialize widget
memwidget = widget({ type = "textbox" })
-- Register widget
vicious.register(memwidget, vicious.widgets.mem, ' <span color="#cfd7e3">Mem:</span> $1%', 13)

if hostname == "shodan" then
  vicious.register(thermal, vicious.widgets.thermal, ' <span color="#edcfd5">$1°C</span>', 20, {"coretemp.0", "core"})
elseif hostname == "mmawdsley-desktop" then
  vicious.register(thermal, vicious.widgets.thermal, ' <span color="#edcfd5">$1°C</span>', 20, {"thermal_zone0", "sys"})
end

pkg = widget({ type = "textbox" })
vicious.register(pkg, vicious.widgets.pkg, 'Ubuntu', 3600)

-- Load Debian menu entries
require("debian.menu")

-- {{{ Variable definitions
-- Themes define colours, icons, and wallpapers
beautiful.init(homedir .. '/.config/awesome/theme.lua')

-- This is used later as the default terminal and editor to run.
terminal = "urxvtq"
editor = os.getenv("EDITOR") or "editor"
editor_cmd = terminal .. " -e " .. editor

-- Default modkey.
-- Usually, Mod4 is the key with a logo between Control and Alt.
-- If you do not like this or do not have such a key,
-- I suggest you to remap Mod4 to another key using xmodmap or other tools.
-- However, you can use another modifier like Mod1, but it may interact with others.
modkey = "Mod4"

-- Table of layouts to cover with awful.layout.inc, order matters.
layouts =
{
  awful.layout.suit.floating,
  awful.layout.suit.tile,
  -- awful.layout.suit.tile.left,
  -- awful.layout.suit.tile.bottom,
  -- awful.layout.suit.tile.top,
  -- awful.layout.suit.fair,
  -- awful.layout.suit.fair.horizontal,
  -- awful.layout.suit.spiral,
  -- awful.layout.suit.spiral.dwindle,
  awful.layout.suit.max,
  -- awful.layout.suit.max.fullscreen,
  -- awful.layout.suit.magnifier
}
-- }}}

if screen.count() > 1 then

-- Shifty configured tags.
shifty.config.tags = {
  ["1:sys"] = {
    layout    = awful.layout.suit.tile,
    mwfact    = 0.50,
    exclusive = false,
    position  = 1,
    init      = true,
    screen    = 1,
  },
  ["2:web"] = {
    layout    = awful.layout.suit.tile,
    exclusive   = false,
    position    = 2,
    mwfact    = 0.65,
    screen    = 2,
    init      = true,
  },
  ["3:mail"] = {
    layout    = awful.layout.suit.tile,
    mwfact    = 0.45,
    exclusive = false,
    position  = 3,
    screen    = 2,
    init      = true,
  },
  ["4:media"] = {
    layout    = awful.layout.suit.floating,
    exclusive = false,
    position  = 4,
    persist = true,
    init      = true,
    screen    = 1,
  },
  ["5:games"] = {
    layout    = awful.layout.suit.tile,
    exclusive = false,
    position = 5,
    screen = 1,
    persist = true,
    init      = true,
  },
  ["6:office"] = {
    layout    = awful.layout.suit.tile,
    exclusive = false,
    position = 6,
    screen = 2,
    persist = true,
    init = true,
  },
  ["8:keepass"] = {
    layout    = awful.layout.suit.tile,
    position = 8,
    screen = 1,
    persist = true,
    init      = true,
  },
  ["9:term"] = {
    layout    = awful.layout.suit.tile,
    position = 9,
    screen = 1,
    init      = true,
  },
}

shifty.config.apps = {
  {
    match = {""},
    notagsteal = true,
    buttons = awful.util.table.join(
      awful.button({}, 1, function (c) client.focus = c; c:raise() end),
      awful.button({modkey}, 1, function(c)
                                  client.focus = c
                                  c:raise()
                                  awful.mouse.client.move(c)
                              end),
      awful.button({modkey}, 3, awful.mouse.client.resize)
    )
  },
  {
    match = {
      class = { "^emacs$", "^Emacs[0-9]+$", "^Steam$", },
    },
    tag = "1:sys",
  },
  {
    match = {
      class = { "^emacs$", "^Emacs[0-9]+$", },
    },
    tag = "1:sys",
    honorsizehints = false,
  },
  {
    match = {
      class = { "^Pygtk%-shutdown$", },
    },
    float = true,
  },
  {
    match = {
      class = { "^Browser$", "^Firefox$", "^Navigator$", "Chromium", "Google%-chrome", },
    },
    tag = "2:web",
  },
  {
    match = {
      name = { "^Firefox Preferences$", "^Cookies$", "^Exceptions %- Cookies$", "^Downloads$", "^Remmina$", },
    },
    float = true,
    tag = "2:web",
  },
  {
    match = {
      class = { "^Mail$", "^Thunderbird$", },
    },
    tag = "3:mail",
  },
  {
    match = {
      name = { "^Thunderbird Preferences$", },
    },
    float = true,
    tag = "3:mail",
  },
  {
    match = {
      class = { "^gimp$", "^Gimp$", },
    },
    tag = "1:sys",
    -- float = true,
  },
  {
    match = {
      class = { "^URxvt$", },
    },
    tag = "9:term",
    honorsizehints = false,
  },
  {
    match = {
      class = { "^urxvt%-temp$", },
    },
    nofocus = true,
    nopopup = true,
  },
  {
    match = {
      class = { "^Pidgin$", },
    },
    tag = "1:sys",
    float = true,
  },
  {
    match = {
      class = { "Steam", },
    },
    tag = "5:games",
    float = true,
  },
  {
    match = {
      class = { "^Keepassx$", },
    },
    tag = "8:keepass",
  },
  {
    match = {
      class = { "^libreoffice", },
    },
    tag = "6:office",
  },
  {
    match = {
      class = { "^xfce4%-notifyd$", },
    },
    nofocus = true,
  },
}

else

-- Shifty configured tags.
shifty.config.tags = {
  ["1:sys"] = {
    layout    = awful.layout.suit.tile,
    mwfact    = 0.50,
    exclusive = false,
    position  = 1,
    init      = true,
    screen    = 1,
  },
  ["2:web"] = {
    layout    = awful.layout.suit.tile,
    exclusive   = false,
    position    = 2,
    mwfact    = 0.65,
    init      = true,
  },
  ["3:mail"] = {
    layout    = awful.layout.suit.tile,
    mwfact    = 0.45,
    exclusive = false,
    position  = 3,
    init      = true,
  },
  ["4:media"] = {
    layout    = awful.layout.suit.floating,
    exclusive = false,
    position  = 4,
    persist = true,
    init      = true,
  },
  ["5:games"] = {
    layout    = awful.layout.suit.tile,
    exclusive = false,
    position = 5,
    persist = true,
    init      = true,
  },
  ["6:office"] = {
    layout    = awful.layout.suit.tile,
    exclusive = false,
    position = 6,
    persist = true,
    init      = true,
  },
  ["8:keepass"] = {
    layout    = awful.layout.suit.tile,
    position = 8,
    screen = 1,
    persist = true,
    init      = true,
  },
  ["9:term"] = {
    layout    = awful.layout.suit.tile,
    position = 9,
    init      = true,
  },
}

shifty.config.apps = {
  {
    match = {""},
    notagsteal = true,
    buttons = awful.util.table.join(
      awful.button({}, 1, function (c) client.focus = c; c:raise() end),
      awful.button({modkey}, 1, function(c)
                                  client.focus = c
                                  c:raise()
                                  awful.mouse.client.move(c)
                              end),
      awful.button({modkey}, 3, awful.mouse.client.resize)
    )
  },
  {
    match = {
      class = { "^emacs$", "^Emacs[0-9]+$", "^Steam$", },
    },
    tag = "1:sys",
  },
  {
    match = {
      class = { "^Pygtk%-shutdown$", },
    },
    float = true,
  },
  {
    match = {
      class = { "^emacs$", "^Emacs[0-9]+$", },
    },
    tag = "1:sys",
    honorsizehints = false,
  },
  {
    match = {
      class = { "^Browser$", "^Firefox$", "^Navigator$", "Chromium", "Google%-chrome", },
    },
    tag = "2:web",
  },
  {
    match = {
      name = { "^Firefox Preferences$", "^Cookies$", "^Exceptions %- Cookies$", "^Downloads$", "^Remmina$", },
    },
    float = true,
  },
  {
    match = {
      class = { "^Mail$", "^Thunderbird$", },
    },
    tag = "3:mail",
  },
  {
    match = {
      name = { "^Thunderbird Preferences$", },
    },
    float = true,
    tag = "3:mail",
  },
  {
    match = {
      class = { "^gimp$", "^Gimp$", },
    },
    tag = "1:sys",
    -- float = true,
  },
  -- {
  --   match = {
  --     class = { "^MPlayer$", "^Vlc$", },
  --   },
  --   float = true,
  --   tag = "4:media",
  -- },
  {
    match = {
      class = { "^libreoffice", },
    },
    tag = "6:office",
  },
  {
    match = {
      class = { "^URxvt$", },
    },
    tag = "9:term",
    honorsizehints = false,
  },
  {
    match = {
      class = { "^urxvt%-temp$", },
    },
    nofocus = true,
    nopopup = true,
  },
  {
    match = {
      class = { "^Pidgin$", },
    },
    tag = "1:sys",
    float = true,
  },
  {
    match = {
      class = { "Steam", },
    },
    tag = "5:games",
    float = true,
  },
  {
    match = {
      class = { "^Keepassx$", },
    },
    tag = "8:keepass",
  },
  {
    match = {
      class = { "^xfce4%-notifyd$", },
    },
    nofocus = true,
  },
}

end

shifty.config.defaults = {
  layout = awful.layout.suit.tile,
  ncol = 1,
  mwfact = 0.60,
  guess_name = true,
  guess_position = true,
}

shifty.config.float_bars = false
shifty.config.sloppy = false

-- {{{ Tags
-- Define a tag table which hold all screen tags.
tags = {}
-- for s = 1, screen.count() do
--     -- Each screen has its own tag table.
--     tags[s] = awful.tag({ 1, 2, 3, 4, 5, 6, 7, 8, 9 }, s, layouts[1])
-- end
-- }}}

-- {{{ Menu
-- Create a laucher widget and a main menu
myawesomemenu = {
  { "manual", terminal .. " -e man awesome" },
  { "edit config", editor_cmd .. " " .. awful.util.getdir("config") .. "/rc.lua" },
  { "restart", awesome.restart },
  { "quit", awesome.quit }
}

mymainmenu = awful.menu({ items = { { "awesome", myawesomemenu, beautiful.awesome_icon },
                                    { "Debian", debian.menu.Debian_menu.Debian },
                                    { "open terminal", terminal }
                                  }
                      })

mylauncher = awful.widget.launcher({ image = image(beautiful.awesome_icon),
                                     menu = mymainmenu })
-- }}}

-- {{{ Wibox
-- Create a textclock widget
mytextclock = awful.widget.textclock({ align = "right" })

-- Create a systray
mysystray = widget({ type = "systray" })

-- Create a wibox for each screen and add it
mywibox = {}
mypromptbox = {}
mylayoutbox = {}
mytaglist = {}
mytaglist.buttons = awful.util.table.join(
  awful.button({ }, 1, awful.tag.viewonly),
  awful.button({ modkey }, 1, awful.client.movetotag),
  awful.button({ }, 3, awful.tag.viewtoggle),
  awful.button({ modkey }, 3, awful.client.toggletag)
  -- awful.button({ }, 4, awful.tag.viewnext),
  -- awful.button({ }, 5, awful.tag.viewprev)
)
mytasklist = {}
mytasklist.buttons = awful.util.table.join(
                     awful.button({ }, 1, function (c)
                                              if not c:isvisible() then
                                                  awful.tag.viewonly(c:tags()[1])
                                              end
                                              client.focus = c
                                              c:raise()
                                          end),
                     awful.button({ }, 3, function ()
                                              if instance then
                                                  instance:hide()
                                                  instance = nil
                                              else
                                                  instance = awful.menu.clients({ width=250 })
                                              end
                                          end)
                     -- awful.button({ }, 4, function ()
                     --                          awful.client.focus.byidx(1)
                     --                          if client.focus then client.focus:raise() end
                     --                      end),
                     -- awful.button({ }, 5, function ()
                     --                          awful.client.focus.byidx(-1)
                     --                          if client.focus then client.focus:raise() end
                     --                      end)
                   )

for s = 1, screen.count() do
  -- Create a promptbox for each screen
  mypromptbox[s] = awful.widget.prompt({ layout = awful.widget.layout.horizontal.leftright })
  -- Create an imagebox widget which will contains an icon indicating which layout we're using.
  -- We need one layoutbox per screen.
  mylayoutbox[s] = awful.widget.layoutbox(s)
  mylayoutbox[s]:buttons(awful.util.table.join(
                           awful.button({ }, 1, function () awful.layout.inc(layouts, 1) end),
                           awful.button({ }, 3, function () awful.layout.inc(layouts, -1) end),
                           awful.button({ }, 4, function () awful.layout.inc(layouts, 1) end),
                           awful.button({ }, 5, function () awful.layout.inc(layouts, -1) end)))
  -- Create a taglist widget
  mytaglist[s] = awful.widget.taglist(s, awful.widget.taglist.label.all, mytaglist.buttons)

  -- Create a tasklist widget
  mytasklist[s] = awful.widget.tasklist(function(c)
                                          return awful.widget.tasklist.label.currenttags(c, s)
                                        end, mytasklist.buttons)

  -- Create the wibox
  mywibox[s] = awful.wibox({ position = "top", screen = s, height = "24" })
  -- Add widgets to the wibox - order matters

  mywibox[s].widgets = {
    {
      mylauncher,
      mytaglist[s],
      mypromptbox[s],
      layout = awful.widget.layout.horizontal.leftright
    },
    mylayoutbox[s],
    mytextclock,
    s == 1 and thermal or nil,
    s == 1 and cpuwidget or nil,
    s == 1 and memwidget or nil,
    s == 1 and newmailwidget.textwidget or nil,
    s == 1 and newmailwidget.iconwidget or nil,
    s == 1 and rsscountwidget.textwidget or nil,
    s == 1 and rsscountwidget.iconwidget or nil,
    s == 1 and volumewidget.textwidget or nil,
    s == 1 and volumewidget.iconwidget or nil,
    s == 1 and batterywidget.textwidget or nil,
    s == 1 and batterywidget.iconwidget or nil,
    s == 1 and pkg or nil,
    s == 1 and mysystray or nil,
    mytasklist[s],
    layout = awful.widget.layout.horizontal.rightleft
  }

end
-- }}}

shifty.taglist = mytaglist
shifty.init()

-- {{{ Mouse bindings
root.buttons(awful.util.table.join(
               awful.button({ }, 3, function () mymainmenu:toggle() end),
               awful.button({ }, 4, awful.tag.viewnext),
               awful.button({ }, 5, awful.tag.viewprev)
             )
           )
-- }}}

-- Indexed SSH usernames/hosts
local indexes = require ("indexes")
indexes.load ("ssh", homedir .. "/.config/awesome/indexes/ssh.lua")

--- Finds the first open terminal and returns it
function get_terminal ()
  local client = client
  local clients = client.get ()

  for i, c in pairs(clients) do

    if awful.rules.match(c, {class = "URxvt"}) then
      return c
    end

  end

  return false

end

--- Toggles the visibility of the terminal
function toggle_terminal ()
  local capi = { client = client, mouse = mouse, screen = screen, }
  local sel = capi.client.focus
  local screen = mouse.screen

  if sel and awful.rules.match(sel, {class = "URxvt"}) then

  else

    local terminal = get_terminal()

    if terminal == false then

      awful.util.spawn("urxvtq")

    else

      local ctags = terminal:tags()
      if table.getn(ctags) == 0 then
        local curtag = awful.tag.selected()
        awful.client.movetotag(curtag, terminal)
      else
        tagviewonly.view_tag (ctags[1])
      end

      client.focus = terminal
      terminal:raise ()

    end

  end

end

-- {{{ Key bindings
globalkeys = awful.util.table.join(
  -- awful.key({ modkey,           }, "Left",   awful.tag.viewprev       ),
  -- awful.key({ modkey,           }, "Right",  awful.tag.viewnext       ),

  -- Volume key bindings
  awful.key({ modkey, }, "KP_Insert", function () awful.util.spawn ("volume 0 &") end),
  awful.key({ modkey, }, "KP_End", function () awful.util.spawn ("volume 10 &") end),
  awful.key({ modkey, }, "KP_Down", function () awful.util.spawn ("volume 20 &") end),
  awful.key({ modkey, }, "KP_Next", function () awful.util.spawn ("volume 30 &") end),
  awful.key({ modkey, }, "KP_Left", function () awful.util.spawn ("volume 40 &") end),
  awful.key({ modkey, }, "KP_Begin", function () awful.util.spawn ("volume 50 &") end),
  awful.key({ modkey, }, "KP_Right", function () awful.util.spawn ("volume 60 &") end),
  awful.key({ modkey, }, "KP_Home", function () awful.util.spawn ("volume 70 &") end),
  awful.key({ modkey, }, "KP_Up", function () awful.util.spawn ("volume 80 &") end),
  awful.key({ modkey, }, "KP_Prior", function () awful.util.spawn ("volume 90 &") end),
  awful.key({ modkey, }, "KP_Add", function () awful.util.spawn("volume up &") end),
  awful.key({ modkey, }, "KP_Subtract", function () awful.util.spawn("volume down &") end),
  awful.key({ modkey, }, "KP_Multiply", function () awful.util.spawn("volume mute &") end),

  awful.key({ modkey, }, "Return", toggle_terminal),
  awful.key({ modkey, }, "Escape", awful.tag.history.restore),
  awful.key({ "Mod1", }, "grave", function () lasttag.viewlast() end),
  awful.key({ },         "Print", function () awful.util.spawn("scrot") end),
  awful.key({ },         "XF86AudioLowerVolume", function () awful.util.spawn("volume down &") end),
  awful.key({ },         "XF86AudioRaiseVolume", function () awful.util.spawn("volume up &") end),
  awful.key({ },         "XF86AudioMute", function () awful.util.spawn("volume mute &") end),

  awful.key({ }, "XF86MonBrightnessUp", function () awful.util.spawn("brightness &") end),
  awful.key({ }, "XF86MonBrightnessDown", function () awful.util.spawn("brightness &") end),
  
  awful.key({ modkey, "Mod1", }, "Return", function () awful.util.spawn(terminal) end),

  -- Shifty: keybindings specific to shifty
  awful.key({modkey, "Shift"}, "d", shifty.del), -- delete a tag
  awful.key({modkey, "Shift"}, "n", shifty.send_prev), -- client to prev tag
  awful.key({modkey}, "n", shifty.send_next), -- client to next tag
  awful.key({modkey, "Control"}, "n", function()
                                        shifty.tagtoscr(awful.util.cycle(screen.count(), mouse.screen + 1))
                                    end), -- move client to next tag
  awful.key({modkey}, "a", shifty.add), -- create a new tag
  awful.key({modkey, "Mod1"}, "r", shifty.rename), -- rename a tag
  awful.key({modkey, "Shift"}, "a", -- nopopup new tag
    function()
      shifty.add({nopopup = true})
  end),

  awful.key({ modkey,           }, "j",
            function ()
              awful.client.focus.byidx( 1)
              if client.focus then client.focus:raise() end
          end),                 -- show next client
  awful.key({ modkey,           }, "k",
            function ()
              awful.client.focus.byidx(-1)
              if client.focus then client.focus:raise() end
          end),                 -- show previous client
  awful.key({ modkey,           }, "w", function () mymainmenu:show({keygrabber=true}) end),

  -- Layout manipulation
  awful.key({ modkey, "Shift"   }, "j", function () awful.client.swap.byidx(  1)    end), -- swap to next client
  awful.key({ modkey, "Shift"   }, "k", function () awful.client.swap.byidx( -1)    end), -- swap to previous client
  -- awful.key({ modkey, "Control" }, "j", function () awful.screen.focus_relative( 1) end), -- swap to next screen
  -- awful.key({ modkey, "Control" }, "k", function () awful.screen.focus_relative(-1) end), -- swap to previous screen
  awful.key({ modkey,           }, "u", awful.client.urgent.jumpto), -- jump to urgent client
  awful.key({ modkey,           }, "Tab", -- jump to previous client
            function ()
              awful.client.focus.history.previous()
              if client.focus then
                client.focus:raise()
              end
          end),
  awful.key({ "Mod1",           }, "Tab", -- jump to previous client
            function ()
              awful.client.focus.history.previous()
              if client.focus then
                client.focus:raise()
              end
          end),

  -- Standard program
  -- awful.key({ modkey,           }, "F2", function () awful.util.spawn("runorraise --class emacs emacs") end),
  -- awful.key({ modkey,           }, "F3", function () awful.util.spawn("runorraise --class firefox firefox") end),
  -- awful.key({ modkey,           }, "F4", function () awful.util.spawn("runorraise --class thunderbird thunderbird") end),
  awful.key({ modkey,           }, "F5", function () awful.util.spawn("nautilus --no-desktop") end),
  awful.key({ "Control", "Mod1" }, "l", function () awful.util.spawn("pygtk-shutdown") end),
  -- awful.key({ modkey,           }, "Return", function () awful.util.spawn("runorraise --class urxvt urxvtq") end),
  awful.key({ modkey, "Control" }, "r", awesome.restart),
  -- awful.key({ modkey, "Shift"   }, "q", awesome.quit),
  awful.key({ modkey, "Shift"   }, "q", function () awful.util.spawn("quitawesome") end),

  awful.key({ modkey,           }, "l",     function () awful.tag.incmwfact( 0.05)    end),
  awful.key({ modkey,           }, "h",     function () awful.tag.incmwfact(-0.05)    end),
  awful.key({ modkey, "Shift"   }, "h",     function () awful.tag.incnmaster( 1)      end),
  awful.key({ modkey, "Shift"   }, "l",     function () awful.tag.incnmaster(-1)      end),
  awful.key({ modkey, "Control" }, "h",     function () awful.tag.incncol( 1)         end),
  awful.key({ modkey, "Control" }, "l",     function () awful.tag.incncol(-1)         end),
  awful.key({ modkey,           }, "space", function () awful.layout.inc(layouts,  1) end),
  awful.key({ modkey, "Shift"   }, "space", function () awful.layout.inc(layouts, -1) end),

  awful.key({ modkey, "Control" }, "n", awful.client.restore),

  -- Prompt
  awful.key({ modkey },          "r", function () mypromptbox[mouse.screen]:run() end),
  awful.key({ modkey, "Shift" }, "r",
            function ()
              awful.prompt.run(
                { prompt = "Run in terminal: " },
                mypromptbox[mouse.screen].widget,
                function (...) awful.util.spawn (terminal .. " -t urxvt -e tmux-append " .. ...) end,
                awful.completion.shell,
                awful.util.getdir("cache") .. "/history")
            end
          ),

  awful.key({ modkey }, "s",
            function ()
              awful.prompt.run(
                { prompt = "SSH: " },
                mypromptbox[mouse.screen].widget,
                function (key)
                  if indexes.get_value ("ssh", key) then
                    awful.util.spawn("tmux-append --command 'ssh " .. indexes.get_value ("ssh", key) .. "' --name '@" .. key .. "'")
                  else
                    naughty.notify({ text = "No option found for " .. key })
                  end
                end,
                function (text, cur_pos, ncomp)
                  return awful.completion.generic(text, cur_pos, ncomp, indexes.get_keys ("ssh"))
                end,
                awful.util.getdir("cache") .. "/history_ssh")
          end),

  awful.key({ modkey }, "x",
            function ()
              awful.prompt.run(
                { prompt = "RSS: " },
                mypromptbox[mouse.screen].widget,
                function (number)
                  if number then
                    awful.util.spawn("openrss " .. number)
                  end
                end,
                nil,
                nil
              )
          end)
  -- awful.key({ modkey }, "x", function ()
  --   awful.prompt.run({ prompt = "Run Lua code: " },
  --                    mypromptbox[mouse.screen].widget,
  --                    awful.util.eval, nil,
  --                    awful.util.getdir("cache") .. "/history_eval")
  -- end)
)

globalkeys = awful.util.table.join(globalkeys, aweror.genkeys(modkey))

for i = 1, 9 do

  globalkeys = awful.util.table.join(globalkeys,
    awful.key({modkey}, i, function()
      local capi = { client = client, mouse = mouse, screen = screen, }
      local c = capi.client.focus
      local j = 0

      if not c then return end

      local clients = awful.client.visible(c.screen)

      for k, cl in ipairs(clients) do
        if not (cl.skip_taskbar or cl.hidden or cl.type == "splash" or cl.type == "dock" or cl.type == "desktop") then
          j = j + 1
          if j == i then
            client.focus = cl
            cl:raise ()
            return
          end
        end
      end

    end))

end

clientkeys = awful.util.table.join(

  -- awful.key({ modkey, }, "Return", function (c) toggle_terminal(c) end),

  awful.key ({ modkey, }, "Left", function (c)
    local w = screen[c.screen].workarea
    local g = c:geometry ()
    c.maximized_horizontal = false
    c.maximized_vertical = false
    g.x = 0
    g.y = w.y
    g.width = w.width / 2
    g.height = w.height
    c:geometry (g)
  end),

  awful.key ({ modkey, }, "Right", function (c)
    local w = screen[c.screen].workarea
    local g = c:geometry ()
    c.maximized_horizontal = false
    c.maximized_vertical = false
    g.x = w.width / 2
    g.y = w.y
    g.width = w.width / 2
    g.height = w.height
    c:geometry (g)
  end),

  awful.key ({ modkey, }, "Up", function (c)
    c.maximized_horizontal = not c.maximized_horizontal
    c.maximized_vertical   = not c.maximized_vertical
  end),

  awful.key({ modkey, "Shift"   }, "t",      function (c) if c.titlebar then awful.titlebar.remove(c) else awful.titlebar.add(c) end end),
  awful.key({ modkey,           }, "f",      function (c) c.fullscreen = not c.fullscreen  end),
  awful.key({ modkey, "Shift"   }, "c",      function (c) c:kill()                         end),
  awful.key({ modkey, "Control" }, "space",  awful.client.floating.toggle                     ),
  awful.key({ modkey, "Control" }, "Return", function (c) c:swap(awful.client.getmaster()) end),
  awful.key({ modkey,           }, "o",      function () awful.screen.focus_relative (1) end),
  awful.key({ modkey, "Shift"   }, "r",      function (c) c:redraw()                       end),
  awful.key({ modkey,           }, "t",      function (c) c.ontop = not c.ontop            end),
  awful.key({ modkey,           }, "n",
            function (c)
              -- The client currently has the input focus, so it cannot be
              -- minimized, since minimized clients can't have the focus.
              c.minimized = true
          end),
  awful.key({ modkey,           }, "m",
            function (c)
              c.maximized_horizontal = not c.maximized_horizontal
              c.maximized_vertical   = not c.maximized_vertical
          end)
)

shifty.config.clientkeys = clientkeys
shifty.config.modkey = modkey

for i = 1, (shifty.config.maxtags or 9) do
   globalkeys = awful.util.table.join(globalkeys,
      awful.key({"Mod1"}, i, function()
         tagviewonly.view_idx (i)
         end),
      awful.key({modkey, "Control"}, i, function()
         local t = shifty.getpos(i)
         t.selected = not t.selected
         end),
      awful.key({modkey, "Control", "Shift"}, i, function()
         if client.focus then
           awful.client.toggletag(shifty.getpos(i))
         end
         end),
      -- move clients to other tags
      awful.key({modkey, "Shift"}, i, function()
         if client.focus then
            t = shifty.getpos(i)
            awful.client.movetotag(t)
            awful.tag.viewonly(t)
         end
      end))
   end

clientbuttons = awful.util.table.join(
  awful.button({ }, 1, function (c) client.focus = c; c:raise() end),
  awful.button({ modkey }, 1, awful.mouse.client.move),
  awful.button({ modkey }, 3, awful.mouse.client.resize))

-- Set keys
root.keys(globalkeys)
-- }}}

-- {{{ Rules
awful.rules.rules = {
  -- All clients will match this rule.
  { rule = { },
    properties = { border_width = beautiful.border_width,
                   border_color = beautiful.border_normal,
                   focus = false,
                   keys = clientkeys,
                   buttons = clientbuttons } },
  { rule = { class = "Steam" },
    properties = { border_width = 0, floating = true} },
  { rule = { class = "pinentry" },
    properties = { floating = true } },
    callback = awful.placement.centered,
  { rule = { class = "gimp" },
    properties = { floating = true } },
  { rule = { class = "mplayer2" },
    properties = { floating = true } },
  { rule = { class = "vlc" },
    properties = { floating = true } },
  { rule = { class = "gcr-prompter" },
    properties = { floating = true } },
    callback = awful.placement.centered,
  { rule = { class = "Pygtk-shutdown" },
    callback = awful.placement.centered,
    properties = { floating = true } },
}
-- }}}

-- {{{ Signals
-- Signal function to execute when a new client appears.
client.add_signal("manage", function (c, startup)
    if not startup then
        -- Set the windows at the slave,
        -- i.e. put it at the end of others instead of setting it master.
        -- awful.client.setslave(c)

        -- Put windows in a smart way, only if they does not set an initial position.
        if not c.size_hints.user_position and not c.size_hints.program_position then
            awful.placement.no_overlap(c)
            awful.placement.no_offscreen(c)
        end
    end
end)

client.add_signal("focus", function(c) c.border_color = beautiful.border_focus end)
client.add_signal("unfocus", function(c) c.border_color = beautiful.border_normal end)

-- }}}

config = {}
config.run = {}
config.run.startup = {
  "nitrogen --restore &",
  "urxvtq &",
  "dropbox start &",
  "blueman-applet &",
  "update-notifier &",
  "xset s off",
  "xset -dpms",
}

if hostname == "daedalus" then
  table.insert (config.run.startup, "wicd-gtk --tray &")
else
  table.insert (config.run.startup, "nm-applet &")
end

config.run.restart = {
  "xset s off",
  "xset -dpms",
  "nitrogen --restore",
}

config.startup = function ()

  for i = 1, table.getn (config.run.startup) do
    io.popen (config.run.startup[i])
  end

end

config.restart = function ()

  for i = 1, table.getn (config.run.restart) do
    io.popen (config.run.restart[i])
  end

end

config.restart ()