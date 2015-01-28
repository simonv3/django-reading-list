/**
 * The Index Views
 * @jsx m
 */

index = require('./index.controller');

index.view = function(controller) {
  return m("html", [
    m("body", [
      m("div", [
        m("h1", ["Reading List"]),
        m("div", {class:"search"}, [
        m("input",
            {type:"text",
            onkeyup:index.vm.fireOnEnter,
            value:index.vm.searchQuery()}),
        m("input", {type:"submit",
            onclick:index.vm.search,
            value:"Search"}),
        m("ul", {class:"search_results"}, [
          index.vm.results.map(function(result, index) {
            return m("li", [
                m("span", {class:"title"}, [result.title]), " -",
                m("span", {class:"authors"}, [result.links.authors.map(function(author, index) {
                  return author.name
                })])
              ])
          })
        ])
        ])
      ])
    ])
  ]);
};

module.exports = index;
