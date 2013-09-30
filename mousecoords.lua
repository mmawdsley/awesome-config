local capi = { mouse = mouse, screen = screen }
local mouse_coords = {}
local tagger = require ("awful.tag")

module ("mousecoords")

function history_update ()
  local curtag = tagger.selected ()
  local coords = capi.mouse.coords ()
  mouse_coords[curtag.screen] = { x = coords.x, y = coords.y }
end

function history_restore ()
  local curtag = tagger.selected ()
  local coords = mouse_coords[curtag.screen]
  capi.mouse.coords (coords, true)
end

for s = 1, capi.screen.count() do
  mouse_coords[s] = { x = capi.screen[s].geometry.x, y = capi.screen[s].geometry.y }
end
