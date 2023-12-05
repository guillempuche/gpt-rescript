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

=========== Start file RemixAuth.res
```
module User = {
  type t
  type profile
  @get external getAccessToken: t => string = "accessToken"
  @get external getProfile: t => profile = "profile"
  @get external getId: profile => string = "id"
}

module DiscordStrategy = {
  type t
  module CreateDiscordStategyOptions = {
    type t
    @obj
    external make: (
      ~clientID: string,
      ~clientSecret: string,
      ~callbackURL: string,
      // Provide all the scopes you want as an array
      ~scope: array<string>,
      unit,
    ) => t = ""
  }

  // module CreateVerifyFunctionOptions = {
  //   type t
  //   @obj
  //   external make: (
  //     ~accessToken: string,
  //     ~refreshToken: string,
  //     ~extraParams: 'a,
  //     ~profile: 'b,
  //     unit,
  //   ) => t = ""
  // }
  type verifyFunctionParams<'a, 'b> = {
    accessToken: string,
    refreshToken: string,
    extraParams: 'a,
    profile: 'b,
  }

  @module("remix-auth-socials") @new
  external make: (
    CreateDiscordStategyOptions.t,
    verifyFunctionParams<'a, 'b> => Js.Promise.t<'a>,
  ) => t = "DiscordStrategy"
}

// module SocialsProvider = {
//   type t = [#Discord]

// }

module CreateAuthenticateOptions = {
  type t

  @obj external make: (~successRedirect: string=?, ~failureRedirect: string=?, unit) => t = ""
}

module Authenticator = {
  type t
  @module("remix-auth") @new external make: Remix.SessionStorage.t => t = "Authenticator"
  @send external use: (t, DiscordStrategy.t) => unit = "use"
  @send
  external authenticate: (t, string, Webapi.Fetch.Request.t) => Js.Promise.t<User.t> =
    "authenticate"

  @send
  external authenticateWithOptions: (
    t,
    string,
    Webapi.Fetch.Request.t,
    ~options: CreateAuthenticateOptions.t,
  ) => Js.Promise.t<User.t> = "authenticate"
  @send
  external isAuthenticated: (t, Webapi.Fetch.Request.t) => Js.Promise.t<Js.Nullable.t<User.t>> =
    "isAuthenticated"
  @send
  external isAuthenticatedWithOptions: (
    t,
    Webapi.Fetch.Request.t,
    ~options: CreateAuthenticateOptions.t,
  ) => Js.Promise.t<Js.Nullable.t<User.t>> = "isAuthenticated"

  @send
  external logout: (t, Webapi.Fetch.Request.t, ~options: 'option) => Js.Promise.t<unit> = "logout"
}

```
=========== End file