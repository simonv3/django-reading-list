/**
 * JSX version of the Mithril Getting Started documentation's TODO example.
 * http://lhorie.github.io/mithril/getting-started.html
 * @jsx m
 */

//a sample module
var dashboard = {
    controller: function() {
        this.id = m.route.param("userID");
    },
    view: function(controller) {
        return <div>he {controller.id}</div>;
    }
}

//setup routes to start w/ the `#` symbol
m.route.mode = "hash";

console.log(document)

//define a route
m.route(document.body, "/dashboard/johndoe", {
    "/dashboard/:userID": dashboard
});
