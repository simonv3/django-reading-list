/**
 * The Index Models
 */

var searchModule = require('./searchModule/controller');
var bookListModule = require('./bookListModule/controller');

var index = {};

index.controller = function() {
  index.vm.init();
  index.vm.currentlyReadingSearch.vm.init();
  index.vm.onYourShelfBookList.vm.init({books: []});
  index.vm.onYourShelfSearch.vm.init();
};

// Set the view model for the index
index.vm = (function(){
  var vm = {};
  vm.init = function(){
    // Whatever we need to init the flow here.
    this.currentlyReadingSearch = new searchModule();
    this.onYourShelfSearch = new searchModule();
    this.onYourShelfBookList = new bookListModule();
  };
  return vm;
}());

index.view = function(controller) {
  return m("div", [
    m("h1", ["Reading List"]),
    m("h2", ["Currently Reading"]),
    index.vm.currentlyReadingSearch.view(),
    m("h2", ["On Your Shelf"]),
    index.vm.onYourShelfSearch.view(),
    index.vm.onYourShelfBookList.view()
  ]);
};

module.exports = index;
