/**
 * The Search Module.

   Has a SearchResult and SearchResultList model.

   Supplies a view-model (vm) which has a .performSearch and a .fireOnEnter
   function.

   Builds a view with a search box and an input.
 */

var buildURL = require('../utils/buildURLs');
var vndJSON = require('../utils/requestVndApiJson');
var csrfToken = require('../utils/requestWithCSRFToken');
var process = require('../utils/processJsonApi');

var searchModule = function(){
  var search = {};

  search.SearchResult = (function(data){
    // This returns the actual book
    this.title = m.prop(data.title);
    this.editions = m.prop(data.editions);
    this.authors = m.prop(data.authors);
    this.summary = m.prop(data.summary);
    this.id = m.prop(data.id);
  });

  search.SearchResultList = Array;

  // Set the view model for the search
  search.vm = (function(){
    var vm = {};
    vm.init = function(data){

      if (data && data.selectedFunction){
        vm.selectedFunction = data.selectedFunction;
      }

      if (data && data.tags){
        vm.tagsOnAdd = data.tags;
      }

      // A running list of Search Results
      vm.results = new search.SearchResultList();

      // A slot to store the result string before it's searched for.
      vm.searchQuery = m.prop('');

      vm.selectedResult = m.prop('');

      // Add the results.
      vm.performSearch = function() {
        vm.results = new search.SearchResultList();
        // Fetch the results and put them in the list.
        if (vm.searchQuery()) {
          var url = buildURL('search/external', {q: vm.searchQuery()});
          m.request({ method: 'GET',
                      url: url
                      })
            .then(function(response){
              response.forEach(function(result){
                var searchResult = new search.SearchResult(result);
                vm.results.push(searchResult);
              });
          });
        }
      };

      // Make sure we catch enters as well.
      vm.fireOnEnter = function(e) {
        search.vm.searchQuery(e.target.value);
        e.preventDefault();
        if (e.keyCode === 13) search.vm.performSearch();
      };

      vm.add = function(result) {
        var data = {
          'edition': result.editions()[0].id,
          'reader': USER_ID,
          'tags':[vm.tagsOnAdd]
        };
        vm.searchQuery('');
        m.request({ method: 'POST',
                    url: '/api/saves/',
                    data: data,
                    config: csrfToken
                  })
          .then(function(response){
            response.edition.saveId = response.id;
            vm.selectedFunction(response.edition);
          });
        vm.results = new search.SearchResultList();
      };
    };
    return vm;
  }());

  search.view = function(controller) {
    return m("div", {class:"search"}, [
          m("input", {type:"search",
              onkeyup: search.vm.fireOnEnter,
              value: search.vm.searchQuery()}),
          m("input", {type:"submit",
              onclick: search.vm.performSearch,
              value:"Search"}),
          m("ul", {class: search.vm.results.length > 0 ? "search_results" : ''}, [
            search.vm.results.map(function(result, index) {
              return m("li",
                       { onclick: search.vm.add.bind(search.vm, result) }, [
                  m("span", { class:"title" }, result.title()),
                  " - ",
                  m("span", {class:"authors"}, [result.authors().map(function(author, index) {
                    return author.name;
                  })])
                ]);
            })
          ])
        ]);
  };
  return search;
};

module.exports = searchModule;
