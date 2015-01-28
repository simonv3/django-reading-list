/**
 * The Index Module for Reading List
 * @jsx m
 */

var index = {}

// This will set up a series of calls to build the index view.
index = require('./index.view');

m.route.mode = 'hash'

//define a route
m.route(document.body, '/', {
    '/': index
});
