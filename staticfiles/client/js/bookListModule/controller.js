

var bookListModule = function(){
  var books = {};

  books.Book = function(data){
    this.title = m.prop(data.title);
    this.authors = m.prop(data.authors);
    this.summary = m.prop(data.summary);
    this.id = m.prop(data.id);
  };

  books.BookList = Array;

  // Set the view model for the search
  books.vm = (function(){
    var vm = {};
    vm.init = function(data){
      // A list of books
      console.log(data);
      vm.books = new books.BookList(data.books || []);
    };
    return vm;
  }());

  books.view = function(controller) {
    return m("ul", {class:""}, [
      books.vm.books.map(function(book, index) {
        return m("li", [
            m("span", {class:"title"}, [book.title]), " -",
            m("span", {class:"authors"}, [book.links ? book.links.authors.map(function(author, index) {
              return author.name;
            }) : []])
          ]);
      })
    ]);
  };
  return books;
};

module.exports = bookListModule;
