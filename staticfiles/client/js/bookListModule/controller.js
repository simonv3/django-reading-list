/**
 * The Book Module.

   Has a Book and a BookList model

 */

var buildURL = require('../utils/buildURLs');
var vndJSON = require('../utils/requestVndApiJson');
var csrfToken = require('../utils/requestWithCSRFToken');
var process = require('../utils/processJsonApi');

var bookListModule = function(){
  var books = {};

  books.Book = (function(data){
    this.title = m.prop(data.title);
    this.authors = m.prop(data.authors);
    this.summary = m.prop(data.summary);
    this.id = m.prop(data.id);
    this.saveId = m.prop(data.saveId);
    this.editing = m.prop(false);
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
    };

    return vm;
  }());

  books.view = function(controller) {
    return m("ul", {class:'book-list'}, [
      books.vm.books.map(function(book, index) {
        return m("li", { class: "book-item" + (book.editing() ? " editing" : "" )}, [
            m("span", { class: "book-details" }, [
              m("span", { class: "title" }, [book.title()]),
              " by ",
              m("span", { class: "authors" }, [
                book.authors().map(function(author, index){
                  return author.name;
                })]
              ),
            ]),
            m("span", { class: "control" }, [
              m("i", { class:'fa fa-edit edit',
                  onclick: books.vm.edit.bind(books.vm, book)
                }),
              m("i", { class:'fa fa-trash delete',
                  onclick: books.vm.remove.bind(books.vm, book)
                })
            ])

        ]);
      })
    ]);
  };
  return books;
};

module.exports = bookListModule;
