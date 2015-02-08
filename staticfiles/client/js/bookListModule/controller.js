/**
 * The Book Module.

   Has a Book and a BookList model

 */

var bookDetailWidget = require('../widgets/book_detail.widget.js');
var bookControlWidget = require('../widgets/book_control.widget.js');
var bookReviewsWidget = require('../widgets/book_reviews.widget.js');

var buildURL = require('../utils/buildURLs');
var vndJSON = require('../utils/requestVndApiJson');
var csrfToken = require('../utils/requestWithCSRFToken');
var process = require('../utils/processJsonApi');

var bookListModule = function(){
  var books = {};

  books.Book = (function(data){
    this.title = m.prop(data.title);
    this.href = data.href; // Won't change
    this.authors = m.prop(data.authors);
    this.summary = m.prop(data.summary);
    this.tags = m.prop([]);
    this.is_reading = m.prop(false);
    this.id = m.prop(data.id);
    this.saveId = m.prop(data.saveId);
    this.editing = m.prop(false);
    this.viewing = m.prop(false);
  });

  books.BookList = Array;

  // Set the view model for the search
  books.vm = (function(){
    var vm = {};
    vm.init = function(data){

      // a list of books
      vm.books = new books.BookList();

      var url = buildURL(data.endpoint, data);

      m.request({ method: 'GET',
                  url: url,
                  config: vndJSON })
        .then(function(response){
          response.saves.forEach(function(save){
            m.request({ method: 'GET',
                        url: save.href,
                        config: vndJSON })
              .then(function(response){
                response.edition.saveId = response.id;
                var book = new books.Book(response.edition);

                book.detailWidget = new bookDetailWidget();
                book.detailWidget.vm.init(book);

                book.tags(response.tags);
                if (response.tags.length > 0){
                  book.is_reading(response.tags.reduce(function(a, tag){
                    return tag.slug === "currently-reading" || a;
                  }, false));
                }
                vm.books.push(book);
              });
          });
        });
    };

    vm.add = function(object){
      var book = new books.Book(object);
      vm.books.push(book);
    };

    vm.remove = function(removingBook){
      m.request({ method: 'DELETE',
                  url: '/api/saves/' + removingBook.saveId(),
                  config: csrfToken })
        .then(function(response){
          vm.books.forEach(function(book, index){
            if (book.id == removingBook.id){
              vm.books.splice(index, 1);
            }
          });
        });
    };

    vm.edit = function(editingBook){
      editingBook.editing(!editingBook.editing());
      editingBook.viewing(false);
    };

    vm.view = function(viewingBook){
      viewingBook.editing(false);
      viewingBook.viewing(!viewingBook.viewing());
    };

    vm.removeTag = function(viewingBook){

    };

    return vm;
  }());

  books.view = function(controller) {
    return m("ul", {class:'book-list'}, [
      books.vm.books.map(function(book, index) {
        return m("li", { class: "book-item" +
                                (book.editing() ? " editing" : "") +
                                (book.viewing() ? " viewing" : "") }, [
            book.detailWidget.view(),
            // bookDetailWidget(book),
            bookControlWidget(book, books.vm),
            bookReviewsWidget(book)
        ]);
      })
    ]);
  };
  return books;
};

module.exports = bookListModule;
