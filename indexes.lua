local io = io
local assert = assert
local loadstring = loadstring
local pairs = pairs
local table = table

module ("indexes")

local indexes = {}

--- Reads in the indexes from the configuration file
function load (name, path)

  local fh, err = assert (io.open (path, "rb"))

  if err then
    return false
  end

  local content = fh:read ("*all")
  fh:close ()

  local config, err = assert (loadstring (content))

  if err then
    return false
  end

  indexes[name] = config ()

  return true

end

--- Returns the keys from a loaded list
--- @param string name list name
--- @return list
function get_keys (name)
  local values = {}

  if indexes[name] == nil then
    return values
  end

  for k, v in pairs (indexes["ssh"]) do
    table.insert(values, k)
  end

  return values
end

--- Returns the value of a key
--- @param string name list name
--- @param string key
--- @return string
function get_value (name, key)

  if indexes[name] == nil then
    return
  end

  return indexes[name][key]

end