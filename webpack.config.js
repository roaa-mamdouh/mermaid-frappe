const path = require('path');
const { VueLoaderPlugin } = require('vue-loader');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const TerserPlugin = require('terser-webpack-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');

module.exports = {
  mode: process.env.NODE_ENV === 'production' ? 'production' : 'development',
  entry: {
    app: './mermaid/public/frontend/src/main.js',
  },
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, 'mermaid/public/frontend/dist'),
  },
  resolve: {
    extensions: ['.ts', '.tsx', '.js', '.jsx', '.vue', '.json'],
    alias: {
      '@': path.resolve(__dirname, 'mermaid/public/frontend/src'),
      '~icons': path.resolve(__dirname, 'node_modules/lucide/dist/esm/icons'),
    },
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          compilerOptions: {
            isCustomElement: tag => tag.startsWith('mermaid-')
          }
        }
      },
      {
        test: /\.tsx?$/,
        use: [
          {
            loader: 'babel-loader',
            options: {
              presets: [
                ['@babel/preset-env', {
                  targets: {
                    node: 'current',
                    browsers: '> 0.25%, not dead'
                  },
                  useBuiltIns: 'usage',
                  corejs: 3,
                  modules: false,
                  shippedProposals: true,
                  loose: true
                }],
                '@babel/preset-typescript'
              ],
              plugins: [
                '@babel/plugin-transform-runtime',
                '@babel/plugin-transform-async-generator-functions'
              ]
            },
          },
          {
            loader: 'ts-loader',
            options: {
              appendTsSuffixTo: [/\.vue$/],
              transpileOnly: true,
              compilerOptions: {
                module: 'esnext',
                target: 'es2020'
              },
            },
          },
        ],
        include: [
          path.resolve(__dirname, 'mermaid/public/frontend/src'),
          path.resolve(__dirname, 'node_modules/frappe-ui'),
        ],
      },
      {
        test: /\.js$/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              ['@babel/preset-env', {
                targets: {
                  node: 'current',
                  browsers: '> 0.25%, not dead'
                },
                useBuiltIns: 'usage',
                corejs: 3,
                modules: false,
                shippedProposals: true,
                loose: true
              }]
            ],
            plugins: [
              '@babel/plugin-transform-runtime',
              '@babel/plugin-transform-async-generator-functions'
            ]
          },
        },
        include: [
          path.resolve(__dirname, 'mermaid/public/frontend/src'),
          path.resolve(__dirname, 'node_modules/frappe-ui'),
        ],
      },
      {
        test: /\.css$/,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1
            }
          },
          'postcss-loader',
        ],
      },
    ],
  },
  plugins: [
    new VueLoaderPlugin(),
    new MiniCssExtractPlugin({
      filename: '[name].css',
    }),
  ],
  optimization: {
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          format: {
            comments: false,
          },
          ecma: 2020,
          compress: {
            drop_console: process.env.NODE_ENV === 'production',
          },
        },
        extractComments: false,
      }),
      new CssMinimizerPlugin(),
    ],
    splitChunks: {
      chunks: 'all',
      name: 'vendor',
    },
  },
  performance: {
    hints: false,
  },
};
