/**
 * The Index Views
 * @jsx m
 */

var searchResults = require('./searchResults/controller');
var index = require('./index.controller');

index.view = function(controller) {
  return m("html", [
    m("body", [
      m("div", [
        m("h1", ["Reading List"]),
        searchResults.view(controller.searchResults)
      ])
    ])
  ]);
};

module.exports = index;
