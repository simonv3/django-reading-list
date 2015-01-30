/**
 * The Index Views
 * @jsx m
 */

searchResults.view = function(controller) {
  return <div class="search">
      <input type="text"
          onkeyup={searchResults.vm.fireOnEnter}
          value={searchResults.vm.searchQuery()}/>
      <input type="submit"
          onclick={searchResults.vm.search}
          value="Search"/>
      <ul class="search_results currently_reading">
        {searchResults.vm.results.map(function(result, index) {
          return <li>
              <span class="title">{result.title}</span> -
              <span class="authors">{result.links.authors.map(function(author, index) {
                return author.name
              })}</span>
            </li>
        })}
      </ul>
    </div>;
};

module.exports = searchResults;
