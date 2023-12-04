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

=========== Start file AuthServer.res
```
let clientID = Remix.process["env"]["DISCORD_CLIENT_ID"]
let clientSecret = Remix.process["env"]["DISCORD_CLIENT_SECRET"]
let baseUrl = Remix.process["env"]["BASE_URL"]
let uuidNamespace = Remix.process["env"]["UUID_NAMESPACE"]

let cookieOptions = Remix.CreateCookieOptions.make(
  ~sameSite=#lax,
  ~path="/",
  ~httpOnly=true,
  ~secrets=[uuidNamespace],
  ~secure=Remix.process["env"]["NODE_ENV"] === "production",
  (),
)

let cookie = Remix.createCookieWithOptions("__session", cookieOptions)

let sessionStorage =
  cookie
  ->Remix.CreateCookieSessionStorageOptions.make(~cookie=_)
  ->Remix.createCookieSessionStorageWithOptions(~options=_)

let authenticator = sessionStorage->RemixAuth.Authenticator.make

let discordStrategy = RemixAuth.DiscordStrategy.CreateDiscordStategyOptions.make(
  ~clientID,
  ~clientSecret,
  ~callbackURL=baseUrl ++ "/auth/discord/callback",
  ~scope=["identify", "guilds", "guilds.join"],
  (),
)->RemixAuth.DiscordStrategy.make(({accessToken, profile}) => {
  {"accessToken": accessToken, "profile": profile}->Promise.resolve
})

authenticator->RemixAuth.Authenticator.use(discordStrategy)

```
=========== End file