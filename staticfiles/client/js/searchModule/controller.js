/**
 * The Search Module.

   Has a SearchResult and SearchResultList model.

   Supplies a view-model (vm) which has a .performSearch and a .fireOnEnter
   function.

   Builds a view with a search box and an input.
 */

var bookDetailWidget = require('../widgets/book_detail.widget.js');

var buildURL = require('../utils/buildURLs');
var vndJSON = require('../utils/requestVndApiJson');
var csrfToken = require('../utils/requestWithCSRFToken');
var process = require('../utils/processJsonApi');

var searchModule = function(){
  var search = {};

  search.SearchResult = (function(data){
    this.title = m.prop(data.title);
    this.editions = m.prop(data.editions);
    this.authors = m.prop(data.authors);
    this.summary = m.prop(data.summary);
    this.id = m.prop(data.id);
    this.tags = undefined;
    this.detailWidget = new bookDetailWidget();
    this.detailWidget.vm.init(this);
  });

  search.SearchResultList = Array;

  // Set the view model for the search
  search.vm = (function(){
    var vm = {};
    vm.init = function(data){

      if (data && data.onSelectedFunction){
        vm.onSelectedFunction = data.onSelectedFunction;
      }

      if (data && data.onTypeFunction){
        vm.onTypeFunction = data.onTypeFunction;
      }

      if (data && data.tags){
        vm.tagsOnAdd = data.tags;
      }

      // A running list of Search Results
      vm.results = new search.SearchResultList();

      // A slot to store the result string before it's searched for.
      vm.searchQuery = m.prop('');
      vm.isSearching = m.prop(false);
      vm.placeholder = m.prop(data.placeholder || 'Search For Books')

      vm.selectedResult = m.prop('');

      // Add the results.
      vm.performSearch = function() {
        console.log('redrawing');
        vm.isSearching(true);
        // Figure out why this is needed and remove it:
        m.redraw();
        vm.results = new search.SearchResultList();
        // Fetch the results and put them in the list.
        if (vm.searchQuery()) {
          var url = buildURL('search/external', {q: vm.searchQuery()});
          m.request({ method: 'GET',
                      url: url
                      })
            .then(function(response){
              vm.isSearching(false);
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
        vm.onTypeFunction(search.vm.searchQuery());
        if (e.keyCode === 13) search.vm.performSearch(e);
      };

      vm.clearSearch = function(e){
        // This is a bit of a hack, but there's a timeout because
        // otherwise the blur would make the list disappear when the user
        // has clicked on the list item.
        setTimeout(function() {
          vm.results = new search.SearchResultList();
        }, 500);
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
            vm.onSelectedFunction(response.edition);
          });
        vm.results = new search.SearchResultList();
      };
    };
    return vm;
  }());

  var searchingIndicator = function(){
    if (search.vm.isSearching() === true){
      return m("li",
             { class: "searching" },
             [m("i", { class: "fa fa-spinner fa-spin"})]);
    } else {
      return '';
    }
  }

  search.view = function(controller) {
    return m("div", {class:"search"}, [
          m("input", {type:"search",
              onkeyup: search.vm.fireOnEnter,
              onblur: search.vm.clearSearch,
              value: search.vm.searchQuery(),
              placeholder: search.vm.placeholder()
            }),

          m("input", {type:"submit",
              onclick: search.vm.performSearch,
              value:"Search"}),
          m("small", { class: "input-extra" }, "Click search or press enter to search outside your saved books"),
          m("ul", { class: "search-results" +
                    (search.vm.results.length > 0 || search.vm.isSearching() ? " show" : '')},
            [
            searchingIndicator(),
            search.vm.results.map(function(result, index) {
              return m("li", {
                        class: "book-item",
                        onclick: search.vm.add.bind(search.vm, result)
                      }, [
                      result.detailWidget.view()
                  // m("span", { class: "book-details" }, [
                  //   m("span", { class: "title",
                  //               // onclick: detail.vm.view.bind(detail.vm, detail.vm.book)
                  //              }, [result.title()]),
                  //   " by ",
                  //   m("span", { class: "authors" }, [
                  //     result.authors().map(function(author, index){
                  //       var len = result.authors().length - 1;
                  //       return author.name + ( len > index ? ", " : "");
                  //     })
                  //   ])
                  // ])
                ])
            })
          ])
        ]);
  };
  return search;
};

module.exports = searchModule;
