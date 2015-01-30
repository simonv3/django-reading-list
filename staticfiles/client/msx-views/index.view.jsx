/**
 * The Index Views
 * @jsx m
 */

var searchResults = require('./searchResults/controller');
var index = require('./index.controller');

index.view = function(controller) {
  return <html>
    <body>
      <div>
        <h1>Reading List</h1>
        {searchResults.view(controller.searchResults)}
      </div>
    </body>
  </html>;
};

module.exports = index;
