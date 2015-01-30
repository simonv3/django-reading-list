/**
 * The Search Module.

   Has a SearchResult and SearchResultList model.

   Supplies a view-model (vm) which has a .performSearch and a .fireOnEnter
   function.

   Builds a view with a search box and an input.
 */

var buildURL = require('../utils/buildURLs');
var vndJSON = require('../utils/requestVndApiJson');
var process = require('../utils/processJsonApi');

var searchModule = function(){
  var search = {};

  search.SearchResult = function(data){
    this.title = m.prop(data.title);
    this.authors = m.prop(data.authors);
    this.summary = m.prop(data.summary);
    this.id = m.prop(data.id);
  };

  search.SearchResultList = Array;

  // Set the view model for the search
  search.vm = (function(){
    var vm = {};
    vm.init = function(){
      // A running list of Search Results
      vm.results = new search.SearchResultList();

      // A slot to store the result string before it's searched for.
      vm.searchQuery = m.prop("");

      // Add the results.
      vm.performSearch = function() {

        // Fetch the results and put them in the list.
        if (vm.searchQuery()) {

          var externalResults = m.prop([]);
          var callback = function(){
            search.vm.results = process.searchResults(externalResults());
          };

          var url = buildURL('search/external', {q: vm.searchQuery()});
          m.request({ method: 'GET',
                      url: url,
                      config: vndJSON })
            .then(externalResults)
            .then(callback);
        }
      };

      // Make sure we catch enters as well.
      vm.fireOnEnter = function(e) {
        search.vm.searchQuery(e.target.value);
        e.preventDefault();
        if (e.keyCode === 13) search.vm.performSearch();
      };
    };
    return vm;
  }());

  search.view = function(controller) {
    return m("div", {class:"search"}, [
          m("input", {type:"text",
              onkeyup:search.vm.fireOnEnter,
              value:search.vm.searchQuery()}),
          m("input", {type:"submit",
              onclick:search.vm.performSearch,
              value:"Search"}),
          m("ul", {class:"search_results"}, [
            search.vm.results.map(function(result, index) {
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
  return search;
}

module.exports = searchModule;
