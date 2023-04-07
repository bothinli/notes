window.$docsify = {
  name: "这人有点东西",
  repo: "true",
  corner: {
    url: "https://github.com/bothinli/note/tree/master/docs",
    icon: "github"
  },
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
  loadSidebar: true,
  alias: {
    '/.*/_sidebar.md': '/_sidebar.md', //do not request sidebar from subdirectories
  },
  subMaxLevel: 3,
  sidebarDisplayLevel: 1, // set sidebar display level
  autoHeader: true,
  coverpage: true,
  auto2top: true,
  plugins: [
    EditOnGithubPlugin.create(
      "https://github.com/bothinli/note/tree/master/docs/",
      null,
      "Edit on github"
    ),
  ],
  requestHeaders: {
    'cache-control': 'max-age=10',
  },
};
