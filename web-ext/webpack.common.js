/* eslint-env node */

const path = require('path')
const webpack = require('webpack')

module.exports = {
  entry: {
    // Each entry in here would declare a file that needs to be transpiled
    // and included in the extension source.
    // For example, you could add a background script like:
    background: 'background/main.js',
    dashboard: 'dashboard/main.js',
    'do-not-close-page': 'do-not-close-page/main.js',
    'inject-collect-feed': 'inject/collect-feed.js',
    'inject-home-check-login': 'inject/home-check-login.js',
    'inject-profile-page-check-following':
      'inject/profile-page-check-following.js',
    'resource-retreive-ig-user-data':
      'accessible-resources/retreive-ig-user-data.js',
    'resource-retreive-donor-is-following':
      'accessible-resources/retreive-donor-is-following.js',
  },
  output: {
    // This copies each source entry into the extension dist folder named
    // after its entry config key.
    path: path.join(__dirname, 'extension', 'dist'),
    filename: '[name].js',
  },
  optimization: {
    minimize: false,
  },
  module: {
    rules: [
      {
        exclude: ['/node_modules/'],
        test: /\.js$/,
        use: [
          // This transpiles all code (except for third party modules) using Babel.
          {
            // Babel options are in .babelrc
            loader: 'babel-loader',
          },
        ],
      },
    ],
  },
  resolve: {
    // This allows you to import modules just like you would in a NodeJS app.
    extensions: ['.js', '.jsx'],
    modules: [path.join(__dirname, 'src'), 'node_modules'],
  },
  plugins: [
    // Since some NodeJS modules expect to be running in Node, it is helpful
    // to set this environment var to avoid reference errors.
    new webpack.DefinePlugin({
      'process.env.BACKEND_URL': JSON.stringify(
        process.env.BACKEND_URL || 'http://localhost:8000'
      ),
    }),
  ],
}
