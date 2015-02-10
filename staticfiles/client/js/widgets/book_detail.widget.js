/**
 * Book Detail Widget.

   Books are displayed in a fairly standard way.

 */
var csrfToken = require('../utils/requestWithCSRFToken');

var bookDetailWidget = function(){
  var detail = {};

  detail.vm = (function(){
    var vm = {};
    vm.init = function(book){
      vm.tagsInput = m.prop('');
      vm.book = book;
    };

    var trimString = function(string){
      return string.trim();
    };

    var filterEmptyString = function(string){
      return string === '' ? false : true;
    };

    vm.removeTag = function(tag, book){
      // Shell to remove tags.
    };

    vm.processTags = function(e){
      var tags = [];
      vm.tagsInput(e.target.value);
      e.preventDefault();
      if (e.keyCode === 13) {
        tags = vm.tagsInput().split(',')
                  .map(trimString)
                  .filter(filterEmptyString);
        var simpleTags = vm.book.tags().map(function(tag) { return tag.name });

        console.log(simpleTags.concat(tags));
        // vm.book.tags(vm.book.tags() + tags);
        var data = {
          tags: simpleTags.concat(tags),
        };
        m.request({ method: 'PATCH',
                    url: vm.book.savesHref(),
                    data: data,
                    config: csrfToken
                  })
          .then(function(response){
            console.log(response);
          });
      }
    };

    vm.addTag = function(tag){
      console.log(vm.book.href);
    };

    return vm;
  })();

  var showTagsView = function(book){
    return book.tags ? m("span", { class: "tags" }, [
      book.tags().map(function(tag, index){
        return m("span", [
          tag.name,
          book.editing() ? m("span", { class: "fa fa-close delete",
                                       onclick: detail.vm.removeTag.bind(tag, book)
                                     }, '') : ''
          ]);
      })
    ]) : '';
  };

  var editTagsView = function(book){
    if (book.editing && book.editing()){
      return m("div", { class: "add-tags" }, [
        m("label", ["Add tags",
                    m("small", "(comma separated)"),
                    ":"]),
        m("input", { type: "text",
                     placeholder: "Economics, Design, Comics, etc",
                     value: detail.vm.tagsInput(),
                     onkeyup: detail.vm.processTags }),
        m("input", { type: "submit",
                     class: "small",
                     value: "Add Tags",
                     onclick: detail.vm.processTags })
      ]);
    }
  };

  var showAuthorsView = function(book){
    return m("span", { class: "authors" }, [
      book.authors().map(function(author, index){
        var len = book.authors().length - 1;
        return author.name + ( len > index ? ", " : "");
      })
    ]);
  };

  var markAsReadView = function(book){
    if (book.editing && book.reading && book.editing() && book.is_reading()){
      return m("span", { class: 'mark-as-read' }, ["Done reading?"]);
    }
  };

  detail.view = function(){
    return m("span", { class: "book-details" }, [
      m("span", { class: "title" }, [detail.vm.book.title()]),
      " by ",
      showAuthorsView(detail.vm.book),
      markAsReadView(detail.vm.book),
      showTagsView(detail.vm.book),
      editTagsView(detail.vm.book)
    ]);
  };

  return detail;
};

module.exports = bookDetailWidget;
