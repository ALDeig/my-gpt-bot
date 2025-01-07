 const path = require('path');

 module.exports = {
   entry: {
     app: './static/js/index.js',
   },
   output: {
     filename: '[name].bundle.js',
     //filename: 'main.js',
     path: path.resolve(__dirname, 'static/js/'),
     //clean: true,
   },
 };
