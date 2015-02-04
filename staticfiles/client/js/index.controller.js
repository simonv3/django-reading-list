/**
 * The Index Models
 */

var buildURL = require('./utils/buildURLs');
var vndJSON = require('./utils/requestVndApiJson');
var searchModule = require('./searchModule/controller');
var bookListModule = require('./bookListModule/controller');

var index = {};

index.controller = function() {
  index.vm.init();
  index.vm.currentlyReadingBookList.vm.init({
    endpoint: 'readers',
    id: USER_ID,
    tags: 'currently-reading'
  });
  index.vm.currentlyReadingSearch.vm.init({
    selectedFunction: index.vm.currentlyReadingBookList.vm.add,
    tags: 'currently-reading'
  });
  index.vm.savedBookList.vm.init({
    endpoint: 'readers',
    id: USER_ID
  });
  index.vm.savedSearch.vm.init({
    selectedFunction: index.vm.savedBookList.vm.add
  });

};

// Set the view model for the index
index.vm = (function(){
  var vm = {};
  vm.init = function(){
    // Whatever we need to init the flow here.
    this.currentlyReadingBookList = new bookListModule();
    this.currentlyReadingSearch = new searchModule();
    this.savedSearch = new searchModule();
    this.savedBookList = new bookListModule();
  };
  return vm;
}());

index.view = function(controller) {
  return m("div", {class: 'content index'}, [
    m("h1", ["Reading List"]),
    m("h2", ["Currently Reading"]),
    index.vm.currentlyReadingSearch.view(),
    index.vm.currentlyReadingBookList.view(),
    m("h2", ["Saved Books"]),
    index.vm.savedSearch.view(),
    index.vm.savedBookList.view()
  ]);
};

module.exports = index;
