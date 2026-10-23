// The explorer models under Node, for the question tests: loads the core and every kind
// file of docs/javascripts/explorer/ and returns the merged models (see core.js).
const fs = require("fs");
const path = require("path");

const dir = path.join(__dirname, "..", "docs", "javascripts", "explorer");
require(path.join(dir, "core.js"));
for (const file of fs.readdirSync(dir).sort()) {
  if (file.endsWith(".js") && file !== "core.js") require(path.join(dir, file));
}
module.exports = globalThis.dvqExplorers.models;
