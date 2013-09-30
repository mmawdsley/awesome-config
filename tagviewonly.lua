local awful = require ("awful")
local mousecoords = require ("mousecoords")
local shifty = require ("shifty")

module ("tagviewonly")

function view_idx (idx)
  view_tag (shifty.getpos (idx))
end

function view_tag (tag)
  mousecoords.history_update ()

  awful.screen.focus (tag.screen)
  awful.tag.viewonly (tag)

  mousecoords.history_restore ()
end