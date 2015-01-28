/*
 * A utility method for building and abstracting the
 * building of the URLs needed to access the API.
 */

module.exports = function(endpoint, parameters){
  var url = '';
  if (endpoint === 'search/external'){
    url = '/books/api/' + endpoint + '/' + parameters.q + '/';
  }
  return url;
};
