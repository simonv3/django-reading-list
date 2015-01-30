/**
 * The Index Views
 * @jsx m
 */

searchResults.view = function(controller) {
  return m("div", {class:"search"}, [
      m("input", {type:"text",
          onkeyup:searchResults.vm.fireOnEnter,
          value:searchResults.vm.searchQuery()}),
      m("input", {type:"submit",
          onclick:searchResults.vm.search,
          value:"Search"}),
      m("ul", {class:"search_results currently_reading"}, [
        searchResults.vm.results.map(function(result, index) {
          return m("li", [
              m("span", {class:"title"}, [result.title]), " -",
              m("span", {class:"authors"}, [result.links.authors.map(function(author, index) {
                return author.name
              })])
            ])
        })
      ])
    ]);
};

module.exports = searchResults;
