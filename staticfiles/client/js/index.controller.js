/**
 * The Index Controller
 * @jsx m
 */

index = require('./index.view-model');

index.controller = function() {
  index.vm.init();
};

module.exports = index;
