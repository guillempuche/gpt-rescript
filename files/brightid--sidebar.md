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

=========== Start file Sidebar.res
```
module ConnectButton = {
  @react.component @module("@rainbow-me/rainbowkit")
  external make: (
    ~children: React.element=?,
    ~style: ReactDOM.Style.t=?,
    ~className: string=?,
  ) => 'b = "ConnectButton"
}

@react.component
let make = (~isSidebarVisible, ~handleIsSidebarVisible, ~guilds, ~loadingGuilds) => {
  open ReactProSidebar

  let icon = ({id, icon}: Types.oauthGuild) => {
    switch icon {
    | None => "/assets/brightid_logo_white.png"
    | Some(icon) => `https://cdn.discordapp.com/icons/${id}/${icon}.png`
    }
  }

  let sidebarElements = {
    switch (guilds, loadingGuilds) {
    | (_, true) =>
      let intersection = guilds->Belt.Array.map((guild: Types.oauthGuild) => {
        <Menu iconShape="square" key={guild.id}>
          <MenuItem
            className="bg-extraDark"
            icon={<img
              className=" bg-extraDark rounded-lg border-1 border-white" src={guild->icon}
            />}>
            <Remix.Link
              className="font-semibold text-xl" to={`/guilds/${guild.id}`} prefetch={#intent}>
              {guild.name->React.string}
            </Remix.Link>
          </MenuItem>
        </Menu>
      })
      let loading = Belt.Array.range(0, 4)->Belt.Array.map(i => {
        <Menu iconShape="square" key={(i + 1)->Belt.Int.toString}>
          <MenuItem
            className="flex animate-pulse flex-row h-full bg-extraDark "
            icon={<img
              className=" bg-extraDark  rounded-lg" src="/assets/brightid_logo_white.png"
            />}>
            <div className="flex flex-col space-y-3">
              <div className="w-36 bg-gray-300 h-6 rounded-md " />
            </div>
          </MenuItem>
        </Menu>
      })
      intersection->Belt.Array.concat(loading)->React.array
    | ([], false) => <p className="text-white"> {"Couldn't Load Discord Servers"->React.string} </p>
    | (_, false) =>
      switch guilds->Belt.Array.length {
      | 0 => <p className="text-white"> {"No Guilds"->React.string} </p>
      | _ =>
        guilds
        ->Belt.Array.map((guild: Types.oauthGuild) => {
          <Menu iconShape="square" key={guild.id}>
            <MenuItem
              className="bg-extraDark"
              icon={<img
                className=" bg-extraDark rounded-lg border-1 border-white" src={guild->icon}
              />}>
              <Remix.Link
                className="font-semibold text-xl" to={`/guilds/${guild.id}`} prefetch={#intent}>
                {guild.name->React.string}
              </Remix.Link>
            </MenuItem>
          </Menu>
        })
        ->React.array
      }
    }
  }

  <ProSidebar
    className="bg-dark scrollbar-hide"
    breakPoint="md"
    onToggle={handleIsSidebarVisible}
    toggled={isSidebarVisible}>
    <SidebarHeader
      className="p-2 flex justify-around items-center top-0 sticky bg-dark z-10 scrollbar-hide">
      <InviteButton />
    </SidebarHeader>
    <SidebarContent className="scrollbar-hide">
      <Menu iconShape="square" key={0->Belt.Int.toString} />
      {sidebarElements}
    </SidebarContent>
    <SidebarFooter className="bg-extraDark bottom-0 sticky scrollbar-hide list-none">
      <Remix.Link to={""}>
        <MenuItem>
          <img src={"/assets/brightid_reversed.svg"} />
        </MenuItem>
      </Remix.Link>
    </SidebarFooter>
  </ProSidebar>
}

```
=========== End file