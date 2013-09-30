local capi = { mouse = mouse, screen = screen }
local tagger = require ("awful.tag")
local tagviewonly = require ("tagviewonly")
local last_tag
local current_tag

module ("lasttag")

--- Updates the tag history
function update ()
  local selected = tagger.selected (capi.mouse.screen)

  last_tag = current_tag
  current_tag = selected

end

--- Views the last selected from all screens
function viewlast ()

  if last_tag then
    tagviewonly.view_tag (last_tag)
  end

end

for s = 1, capi.screen.count () do
  capi.screen[s]:add_signal ("tag::history::update", update)
end