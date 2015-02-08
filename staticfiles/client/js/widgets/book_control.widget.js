/**
 * Book Control Widget.

   Books are controlled in a fairly standard way

 */

var bookControlWidget = function(book, vm){
  return m("span", { class: "control" }, [
    m("i", { class:'fa fa-eye view',
        onclick: vm.view.bind(vm, book)
      }),
    m("i", { class:'fa edit' + (book.editing() ? ' fa-check' : ' fa-edit'),
        onclick: vm.edit.bind(vm, book)
      }),
    m("i", { class:'fa fa-trash delete',
        onclick: vm.remove.bind(vm, book)
      })

  ]);
};

module.exports = bookControlWidget;
