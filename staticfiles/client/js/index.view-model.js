/**
 * The Index Models
 */

var index = require('./models/searchresult');
var buildURL = require('./utils/buildURLs');
var vndJSON = require('./utils/requestVndApiJson');
var process = require('./utils/processJsonApi');

// Set the view model for the index
index.vm = (function(){
  var vm = {};
  vm.init = function(){

    // A running list of Search Results
    vm.results = new index.SearchResultList();

    // A slot to store the result string before it's searched for.
    vm.searchQuery = m.prop("");

    // Add the results.
    vm.search = function() {

      // Fetch the results and put them in the list.
      if (vm.searchQuery()) {

        var externalResults = m.prop([]);
        var callback = function(){
          index.vm.results = process.searchResults(externalResults());
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
      index.vm.searchQuery(e.target.value);
      e.preventDefault();
      if (e.keyCode === 13) index.vm.search();
    };
  };
  return vm;
}());

module.exports = index;
