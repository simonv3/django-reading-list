
processJsonApi = function(){

  var isArray = function(aVar){
    if( Object.prototype.toString.call( aVar ) === '[object Array]' ) {
      return true;
    }
    return false;
  };

  // searchInLinked's this is the 'linked' list pertaining
  // to key for the object. So for the `authors` key, it will be
  // results.linked.authors.
  var searchInLinked = function(linked_id){
    var self = this;
    var wanted = self.filter(function(item){
      return item.id === linked_id;
    })[0];
    return wanted;
  };

  var searchResults = function(results){
    results.data.forEach(function(datum){
      var links,
          newLinks;
      for (var linkKey in datum.links){
        links = datum.links[linkKey];

        // Some linkKey objects won't exist in the linked
        // array.
        if (results.linked[linkKey]){
          if (isArray(links)) {
            newLinks = links.map(searchInLinked, results.linked[linkKey]);
          }
          else {
            newLinks = searchInLinked(links, results.linked[linkKey]);
          }
          datum.links[linkKey] = newLinks;
        }

      }
    });
    console.log(results.data);
    return results.data;
  };
  return {
    'searchResults': searchResults
  };
};

module.exports = processJsonApi();
