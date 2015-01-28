/**
 * The Index Views
 * @jsx m
 */

index = require('./index.controller');

index.view = function(controller) {
  return <html>
    <body>
      <div>
        <h1>Reading List</h1>
        <div class="search">
        <input
            type="text"
            onkeyup={index.vm.fireOnEnter}
            value={index.vm.searchQuery()}/>
        <input type="submit"
            onclick={index.vm.search}
            value="Search"/>
        <ul class="search_results">
          {index.vm.results.map(function(result, index) {
            return <li>
                <span class="title">{result.title}</span> -
                <span class="authors">{result.links.authors.map(function(author, index) {
                  return author.name
                })}</span>
              </li>
          })}
        </ul>
        </div>
      </div>
    </body>
  </html>;
};

module.exports = index;
