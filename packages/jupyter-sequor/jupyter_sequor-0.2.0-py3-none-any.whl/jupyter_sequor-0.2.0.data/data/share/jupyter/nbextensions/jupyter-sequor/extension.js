define(function() { return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/extension.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/extension.js":
/*!**************************!*\
  !*** ./src/extension.js ***!
  \**************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/**\n * Jupyter Sequor.\n *\n * This file contains the javascript that is run when the notebook is loaded.\n * It contains some requirejs configuration and the `load_ipython_extension`\n * which is required for any notebook extension.\n *\n * @link   https://github.com/CermakM/jupyter-sequor#readme\n * @file   This file loads the Jupyter extension for following cell outputs.\n * @author Marek Cermak <macermak@redhat.com>\n * @since  0.0.0\n */\n\n/* eslint-disable */\n\nconst __extension__ = \"jupyter-sequor\"\n\n// Some static assets may be required by the custom widget javascript. The base\n// url for the notebook is not known at build time and is therefore computed\n// dynamically.\n__webpack_require__.p = document.querySelector( \"body\" ).getAttribute( 'data-base-url' ) + 'nbextensions/jupyter-nbrequirements/';\n\n// Load the extension\nif ( window.require ) {\n    window.require.config( {\n        map: {\n            \"*\": {\n                [ __extension__ ]: `nbextensions/${ __extension__ }/index`\n            }\n        }\n    } );\n    window.require( [ __extension__ ], ( module ) => {\n        // Require it right ahead so that it is loaded immediately\n        module.setup()\n\n        console.log( \"Loaded extension: \", __extension__ )\n    } )\n}\n\n// Export the required load_ipython_extension\nmodule.exports = {\n    load_ipython_extension: function () {\n        window.require( [\n            \"base/js/namespace\",\n            \"base/js/events\"\n        ], ( Jupyter, events ) => {\n\n            // Wait for the required extension to be loaded\n            events.one( \"notebook_loaded.Notebook\", () => {\n\n                // TODO: Initialize existing output areas\n            } )\n        } )\n\n    }\n};\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiLi9zcmMvZXh0ZW5zaW9uLmpzLmpzIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vLy4vc3JjL2V4dGVuc2lvbi5qcz8xNWU4Il0sInNvdXJjZXNDb250ZW50IjpbIi8qKlxuICogSnVweXRlciBTZXF1b3IuXG4gKlxuICogVGhpcyBmaWxlIGNvbnRhaW5zIHRoZSBqYXZhc2NyaXB0IHRoYXQgaXMgcnVuIHdoZW4gdGhlIG5vdGVib29rIGlzIGxvYWRlZC5cbiAqIEl0IGNvbnRhaW5zIHNvbWUgcmVxdWlyZWpzIGNvbmZpZ3VyYXRpb24gYW5kIHRoZSBgbG9hZF9pcHl0aG9uX2V4dGVuc2lvbmBcbiAqIHdoaWNoIGlzIHJlcXVpcmVkIGZvciBhbnkgbm90ZWJvb2sgZXh0ZW5zaW9uLlxuICpcbiAqIEBsaW5rICAgaHR0cHM6Ly9naXRodWIuY29tL0Nlcm1ha00vanVweXRlci1zZXF1b3IjcmVhZG1lXG4gKiBAZmlsZSAgIFRoaXMgZmlsZSBsb2FkcyB0aGUgSnVweXRlciBleHRlbnNpb24gZm9yIGZvbGxvd2luZyBjZWxsIG91dHB1dHMuXG4gKiBAYXV0aG9yIE1hcmVrIENlcm1hayA8bWFjZXJtYWtAcmVkaGF0LmNvbT5cbiAqIEBzaW5jZSAgMC4wLjBcbiAqL1xuXG4vKiBlc2xpbnQtZGlzYWJsZSAqL1xuXG5jb25zdCBfX2V4dGVuc2lvbl9fID0gXCJqdXB5dGVyLXNlcXVvclwiXG5cbi8vIFNvbWUgc3RhdGljIGFzc2V0cyBtYXkgYmUgcmVxdWlyZWQgYnkgdGhlIGN1c3RvbSB3aWRnZXQgamF2YXNjcmlwdC4gVGhlIGJhc2Vcbi8vIHVybCBmb3IgdGhlIG5vdGVib29rIGlzIG5vdCBrbm93biBhdCBidWlsZCB0aW1lIGFuZCBpcyB0aGVyZWZvcmUgY29tcHV0ZWRcbi8vIGR5bmFtaWNhbGx5LlxuX193ZWJwYWNrX3B1YmxpY19wYXRoX18gPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCBcImJvZHlcIiApLmdldEF0dHJpYnV0ZSggJ2RhdGEtYmFzZS11cmwnICkgKyAnbmJleHRlbnNpb25zL2p1cHl0ZXItbmJyZXF1aXJlbWVudHMvJztcblxuLy8gTG9hZCB0aGUgZXh0ZW5zaW9uXG5pZiAoIHdpbmRvdy5yZXF1aXJlICkge1xuICAgIHdpbmRvdy5yZXF1aXJlLmNvbmZpZygge1xuICAgICAgICBtYXA6IHtcbiAgICAgICAgICAgIFwiKlwiOiB7XG4gICAgICAgICAgICAgICAgWyBfX2V4dGVuc2lvbl9fIF06IGBuYmV4dGVuc2lvbnMvJHsgX19leHRlbnNpb25fXyB9L2luZGV4YFxuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfSApO1xuICAgIHdpbmRvdy5yZXF1aXJlKCBbIF9fZXh0ZW5zaW9uX18gXSwgKCBtb2R1bGUgKSA9PiB7XG4gICAgICAgIC8vIFJlcXVpcmUgaXQgcmlnaHQgYWhlYWQgc28gdGhhdCBpdCBpcyBsb2FkZWQgaW1tZWRpYXRlbHlcbiAgICAgICAgbW9kdWxlLnNldHVwKClcblxuICAgICAgICBjb25zb2xlLmxvZyggXCJMb2FkZWQgZXh0ZW5zaW9uOiBcIiwgX19leHRlbnNpb25fXyApXG4gICAgfSApXG59XG5cbi8vIEV4cG9ydCB0aGUgcmVxdWlyZWQgbG9hZF9pcHl0aG9uX2V4dGVuc2lvblxubW9kdWxlLmV4cG9ydHMgPSB7XG4gICAgbG9hZF9pcHl0aG9uX2V4dGVuc2lvbjogZnVuY3Rpb24gKCkge1xuICAgICAgICB3aW5kb3cucmVxdWlyZSggW1xuICAgICAgICAgICAgXCJiYXNlL2pzL25hbWVzcGFjZVwiLFxuICAgICAgICAgICAgXCJiYXNlL2pzL2V2ZW50c1wiXG4gICAgICAgIF0sICggSnVweXRlciwgZXZlbnRzICkgPT4ge1xuXG4gICAgICAgICAgICAvLyBXYWl0IGZvciB0aGUgcmVxdWlyZWQgZXh0ZW5zaW9uIHRvIGJlIGxvYWRlZFxuICAgICAgICAgICAgZXZlbnRzLm9uZSggXCJub3RlYm9va19sb2FkZWQuTm90ZWJvb2tcIiwgKCkgPT4ge1xuXG4gICAgICAgICAgICAgICAgLy8gVE9ETzogSW5pdGlhbGl6ZSBleGlzdGluZyBvdXRwdXQgYXJlYXNcbiAgICAgICAgICAgIH0gKVxuICAgICAgICB9IClcblxuICAgIH1cbn07XG4iXSwibWFwcGluZ3MiOiJBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Iiwic291cmNlUm9vdCI6IiJ9\n//# sourceURL=webpack-internal:///./src/extension.js\n");

/***/ })

/******/ })});;