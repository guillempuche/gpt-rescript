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

=========== Start file entryRes.server.res
```
module ResponseInit = {
  type t

  external make: {..} => t = "%identity"
}

module BodyInit = {
  open Webapi.Fetch
  external makeWithPipeapleStream: NodeJs.Stream.PassThrough.t<
    NodeJs.Buffer.t,
    NodeJs.Buffer.t,
  > => BodyInit.t = "%identity"
}

@module("isbot") external isbot: string => bool = "default"

module ReactDOMServer = {
  type pipe = NodeJs.Stream.PassThrough.t<
    NodeJs.Buffer.t,
    NodeJs.Buffer.t,
  > => NodeJs.Stream.writable<NodeJs.Buffer.t>
  type abort = unit => unit

  type pipeableStream = {
    abort: abort,
    pipe: pipe,
  }

  @get external pipe: pipeableStream => pipe = "pipe"
  @get external abort: pipeableStream => abort = "abort"

  @module("react-dom/server")
  external renderToPipeableStream: (React.element, 'options) => pipeableStream =
    "renderToPipeableStream"
}

// TODO: Swap out for Webapi.Fetch.Response when it supports construction
// See https://github.com/tinymce/rescript-webapi/issues/63
@new
external makeResponse: (Webapi.Fetch.BodyInit.t, ResponseInit.t) => Webapi.Fetch.Response.t =
  "Response"

type onAllReady = {
  onAllReady: unit => unit,
  onShellError: exn => unit,
  onError: exn => unit,
}
type onShellReady = {
  onShellReady: unit => unit,
  onShellError: exn => unit,
  onError: exn => unit,
}
type ready = AllReady(onAllReady) | ShellReady(onShellReady)

@live
let default = (request, responseStatusCode, responseHeaders, remixContext) => {
  open Webapi
  let abortDelay = 5000

  let maybeCallbackName =
    request
    ->Fetch.Request.headers
    ->Fetch.Headers.get("User-Agent")
    ->Belt.Option.map(isbot)
    ->Belt.Option.map(onAllReady => onAllReady ? "onAllReady" : "onShellReady")

  Promise.make((resolve, reject) => {
    let onAllReadyOptions = pipe => {
      let callbackFn = () => {
        let body = NodeJs.Stream.PassThrough.make()

        request->Fetch.Request.headers->Fetch.Headers.set("Content-Type", "text/html")

        let response = BodyInit.makeWithPipeapleStream(body)->makeResponse(
          ResponseInit.make({
            "status": responseStatusCode,
            "headers": responseHeaders,
          }),
        )

        resolve(. response)
        pipe(body)->ignore
      }
      {
        onAllReady: callbackFn,
        onShellError: err => reject(. err),
        onError: err => Js.Console.error(err),
      }
    }
    let onShellReadyOptions = pipe => {
      let callbackFn = () => {
        let body = NodeJs.Stream.PassThrough.make()

        request->Fetch.Request.headers->Fetch.Headers.set("Content-Type", "text/html")

        let response = BodyInit.makeWithPipeapleStream(body)->makeResponse(
          ResponseInit.make({
            "status": responseStatusCode,
            "headers": responseHeaders,
          }),
        )

        resolve(. response)
        pipe(body)->ignore
      }
      {
        onShellReady: callbackFn,
        onShellError: err => reject(. err),
        onError: err => Js.Console.error(err),
      }
    }

    // This is hacky because we can't access the return in params in rescript
    open ReactDOMServer
    if maybeCallbackName->Belt.Option.getWithDefault("") === "onAllReady" {
      let allStream = renderToPipeableStream(
        <Remix.RemixServer context={remixContext} url={request->Fetch.Request.url} />,
        onAllReadyOptions(%raw(`allStream`)->pipe),
      )
      let _ = NodeJs.Timers.setTimeout(allStream.abort, abortDelay)
    } else if maybeCallbackName->Belt.Option.getWithDefault("") === "onShellReady" {
      let {abort, pipe} = renderToPipeableStream(
        <Remix.RemixServer context={remixContext} url={request->Fetch.Request.url} />,
        onShellReadyOptions(%raw(`pipe`)),
      )

      let _ = NodeJs.Timers.setTimeout(abort, abortDelay)
    }
  })
}

```
=========== End file