module.exports = {
  branches: ['main'],
  repositoryUrl: 'https://github.com/interworks/vl-convert-service',
  plugins: [
    '@semantic-release/commit-analyzer',
    '@semantic-release/release-notes-generator',
    '@semantic-release/github',
    [
      'semantic-release-exec',
      {
        prepareCmd: 'echo ${nextRelease.version} > .release-version',
      },
    ],
  ],
};
