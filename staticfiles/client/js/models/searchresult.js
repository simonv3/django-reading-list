/** @jsx m */
SearchResult = function(data){
  this.title = m.prop(data.title);
  this.authors = m.prop(data.authors);
  this.summary = m.prop(data.summary);
  this.id = m.prop(data.id);
};

module.exports.SearchResult = SearchResult;
module.exports.SearchResultList = Array;
