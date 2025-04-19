const path = require('path');
const { version } = require('./package.json');

module.exports = {
  entry: './static/js/index.js',
  output: {
    path: path.resolve(__dirname, 'static/js'),
    filename: `bundle.${version}.js`,
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-react']
          }
        }
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      }
    ]
  },
  resolve: {
    extensions: ['.js', '.jsx']
  }
}; 