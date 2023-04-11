window.$docsify = {
  name: "这人有点东西",
  repo: "true",
  // corner: {
  //   url: "https://github.com/bothinli/notes/tree/master/docs",
  //   icon: "github"
  // },
  // themeColor: '#3F51B5',
  // routerMode: 'history',
  pagination: {
    crossChapter: true
  },
  "flexible-alerts": {
    style: "flat", //default callout
    tip: {
      label: "提示"
    },
    warning: {
      label: "注意"
    },
    attention: {
      label: "警告"
    }
  },
  loadNavbar: true,
  loadSidebar: true,
  alias: {
    '/.*/_sidebar.md': '/_sidebar.md', //do not request sidebar from subdirectories
  },
  subMaxLevel: 3,
  sidebarDisplayLevel: 1, // set sidebar display level
  autoHeader: true,
  coverpage: false,
  auto2top: true,
  plugins: [
    EditOnGithubPlugin.create(
      "https://github.com/bothinli/notes/blob/master/docs/",
      null,
      "Edit on github"
    ),
  ],
  requestHeaders: {
    'cache-control': 'max-age=10',
  },
};
