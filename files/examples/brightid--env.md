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

=========== Start file Env.res
```
exception EnvError(string)
@module("find-up") external findUpSync: (string, 'options) => string = "findUpSync"
@module("dotenv") external createEnv: {"path": string} => unit = "config"

let nodeEnv = Node.Process.process["env"]

let createEnv = () => {
  let path = switch nodeEnv->Dict.get("ENV_FILE") {
  | None => ".env.local"->findUpSync()
  | Some(envFile) => envFile->findUpSync()
  }
  createEnv({"path": path})
}

let env = name =>
  switch Dict.get(nodeEnv, name) {
  | Some(value) => Ok(value)
  | None => Error(`Environment variable ${name} is missing`)
  }

let getConfig = () =>
  switch (
    env("DISCORD_API_TOKEN"),
    env("DISCORD_CLIENT_ID"),
    env("UUID_NAMESPACE"),
    env("GIST_ID"),
    env("GITHUB_ACCESS_TOKEN"),
    env("SPONSORSHIP_KEY"),
    env("SPONSORSHIPS_WHITELIST"),
    env("DISCORD_LOG_CHANNEL_ID"),
  ) {
  // Got all vars
  | (
      Ok(discordApiToken),
      Ok(discordClientId),
      Ok(uuidNamespace),
      Ok(gistId),
      Ok(githubAccessToken),
      Ok(sponsorshipKey),
      Ok(sponsorshipsWhitelist),
      Ok(discordLogChannelId),
    ) =>
    Ok({
      "discordApiToken": discordApiToken,
      "discordClientId": discordClientId,
      "uuidNamespace": uuidNamespace,
      "gistId": gistId,
      "githubAccessToken": githubAccessToken,
      "sponsorshipKey": sponsorshipKey,
      "sponsorshipsWhitelist": sponsorshipsWhitelist,
      "discordLogChannelId": discordLogChannelId,
    })
  // Did not get one or more vars, return the first error
  | (Error(_) as err, _, _, _, _, _, _, _)
  | (_, Error(_) as err, _, _, _, _, _, _)
  | (_, _, Error(_) as err, _, _, _, _, _)
  | (_, _, _, Error(_) as err, _, _, _, _)
  | (_, _, _, _, Error(_) as err, _, _, _)
  | (_, _, _, _, _, Error(_) as err, _, _)
  | (_, _, _, _, _, _, Error(_) as err, _)
  | (_, _, _, _, _, _, _, Error(_) as err) => err
  }

```
=========== End file