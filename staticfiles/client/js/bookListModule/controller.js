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
    this.book_id = m.prop(data.book); // refers to the book, not the edition
    this.title = m.prop(data.title);
    this.href = data.href; // Won't change
    this.authors = m.prop(data.authors);
    this.summary = m.prop(data.summary);
    this.reviews = m.prop([]);
    this.tags = m.prop([]);
    this.is_reading = m.prop(false);
    this.id = m.prop(data.id);
    this.saveId = m.prop(data.saveId);
    this.editing = m.prop(false);
    this.viewing = m.prop(false);
    this.savesHref = m.prop('');

    // This is a bad place for these to be.
    // Ideally we want the creation of the book model
    // to hook onto this for these specific modules
    this.detailWidget = new bookDetailWidget();
    this.detailWidget.vm.init(this);
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

                book.savesHref(response.href);
                book.tags(response.tags);

                fetchReviewsForBook(book);

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

    // Local methods

    var fetchReviewsForBook = function(book){
      m.request({ method: 'GET',
                  url: '/api/reviews/?book_id=' + book.book_id() })
        .then(function(response){
          response.forEach(function(review){
            review.reading = m.prop(false);
          });
          book.reviews(response);
        });
    };

    return vm;
  }());

  books.view = function(controller) {
    return m("ul", {class:'book-list'}, [
      books.vm.books.sort(function(a, b){
        return a.title() > b.title();
      }).map(function(book, index) {
        return m("li", { class: "book-item" +
                                (book.editing() ? " editing" : "") +
                                (book.viewing() ? " viewing" : "") }, [
            book.detailWidget.view(),
            bookControlWidget(book, books.vm),
            bookReviewsWidget(book)
        ]);
      })
    ]);
  };
  return books;
};

module.exports = bookListModule;
