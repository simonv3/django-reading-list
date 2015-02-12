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
      vm.book.editing = m.prop(false);
      vm.book.viewing = m.prop(false);
    };

    var trimString = function(string){
      return string.trim();
    };

    var filterEmptyString = function(string){
      return string === '' ? false : true;
    };

    vm.view = function(book){
      book.editing(false);
      book.viewing(!book.viewing());
    }

    var sendTags = function(tags){
      var data = {
        tags: tags,
      };
      m.request({ method: 'PATCH',
                  url: vm.book.savesHref(),
                  data: data,
                  config: csrfToken
                })
        .then(function(response){
          vm.book.tags(response.tags);
          vm.tagsInput('');
        });
    }

    vm.removeTag = function(index, book){
      tempTags = _.cloneDeep(book.tags());
      tempTags.splice(index, 1);
      sendTags(tempTags.map(function(tag) {
                              return tag.name;
                            }));
    };

    vm.processTags = function(e){
      var tags = [];
      vm.tagsInput(e.target.value);
      e.preventDefault();
      if (e.keyCode === 13) {
        tags = vm.tagsInput().split(',')
                  .map(trimString)
                  .filter(filterEmptyString);
        var simpleTags = vm.book.tags().map(function(tag) {
                                              return tag.name;
                                            });
        sendTags(simpleTags.concat(tags));
      }
    };

    return vm;
  })();

  var showTagsView = function(book){
    return book.tags ? m("span", { class: "tags" }, [
      book.tags().map(function(tag, index){
        return m("span", [
          tag.name,
          book.editing() ? m("span", { class: "fa fa-close delete",
                                       onclick: detail.vm
                                                  .removeTag
                                                    .bind(tag, index, book)
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
    // if (book.editing && book.reading && book.editing() && book.is_reading()){
    //   return m("span", { class: 'mark-as-read' }, ["Done reading?"]);
    // }
  };

  var inverseReading = function(){
    this.reading(!this.reading());
  }

  var showReviewsView = function(book){
    if (book.viewing && book.viewing() &&
        book.reviews && book.reviews().length > 0){
      return m("div", { class: "reviews" }, [
        m("h1", "Reviews"),
        m("ul", { class: "reviews" },
          book.reviews().map(function(review, index){
            return m("li", [
              m("span", { class: "name", }, review.name),
              " by ",
              m("span", { class: "author", }, review.author),
              " ",
              m("a", { href: review.source_url,
                       target: "_blank" },
                [
                "read review",
                m("i", { class: "fa fa-external-link" })
                ]),
              " "
              ]);

          })
        )
      ]);
    }
  };

  detail.view = function(){
    return m("span", { class: "book-details" }, [
      m("span", { class: "title",
                  // onclick: detail.vm.view.bind(detail.vm, detail.vm.book)
                 }, [detail.vm.book.title()]),
      " by ",
      showAuthorsView(detail.vm.book),
      markAsReadView(detail.vm.book),
      showTagsView(detail.vm.book),
      editTagsView(detail.vm.book),
      showReviewsView(detail.vm.book)
    ]);
  };

  return detail;
};

module.exports = bookDetailWidget;
