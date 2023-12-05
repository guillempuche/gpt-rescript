Rescript v10

Repo: https://github.com/ShenaniganDApp/brightid-discord-bot

=========== Start file package.json (part or full code)
```
{
  "name": "root",
  "private": true,
  "devDependencies": {
    "patch-package": "^6.4.7"
  },
  "dependencies": {
    "@rescript/core": "^0.2.0",
    "brightid_sdk": "^1.0.1",
    "canvas": "^2.9.0",
    "concurrently": "^7.1.0",
    "dotenv": "^8.2.0",
    "find-up": "^6.3.0",
    "rescript": "^10.1.0-rc.5",
    "rescript-discordjs": "^0.3.0",
    "rescript-nodejs": "^14.3.1",
    "uuid": "^8.3.0"
  },
  "scripts": {
    "bot": "yarn workspace @brightidbot/bot",
    "web": "yarn workspace @brightidbot/web",
    "utils": "yarn workspace @brightidbot/utils",
    "scripts": "yarn workspace @brightidbot/scripts",
    "shared": "yarn workspace @brightidbot/shared",
    "re:build": "yarn shared re:build && yarn utils re:build && yarn bot re:build && yarn web re:build && yarn scripts re:build"
  },
  "workspaces": [
    "apps/*",
    "packages/*"
  ]
}

```
=========== End file

=========== Start file ReactProSidebar.res
```
module ProSidebar = {
  @react.component @module("react-pro-sidebar")
  external make: (
    ~children: React.element,
    ~className: string=?,
    ~breakPoint: string,
    ~onToggle: bool => unit,
    ~collapsed: bool=?,
    ~toggled: bool=?,
  ) => React.element = "ProSidebar"
}

module Menu = {
  @react.component @module("react-pro-sidebar")
  external make: (~children: React.element=?, ~iconShape: string) => React.element = "Menu"
}
module MenuItem = {
  @react.component @module("react-pro-sidebar")
  external make: (
    ~children: React.element=?,
    ~className: string=?,
    ~icon: React.element=?,
  ) => React.element = "MenuItem"
}
module SidebarHeader = {
  @react.component @module("react-pro-sidebar")
  external make: (~children: React.element=?, ~className: string=?) => React.element =
    "SidebarHeader"
}
module SidebarContent = {
  @react.component @module("react-pro-sidebar")
  external make: (~children: React.element, ~className: string=?) => React.element =
    "SidebarContent"
}
module SidebarFooter = {
  @react.component @module("react-pro-sidebar")
  external make: (~children: React.element=?, ~className: string=?) => React.element =
    "SidebarFooter"
}
```
=========== End file