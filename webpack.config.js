const path = require("path");

module.exports = {
  mode: "production",
  entry: "./static/js/index.js",
  output: {
    filename: "main.js",
    path: path.resolve(__dirname, "static/js"),
  },
};
