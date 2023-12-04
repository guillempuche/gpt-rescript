Rescript v11

Repo: https://github.com/zth/res-x

=========== Start file package.json (part or full code)
```
{
  "name": "rescript-x",
  "version": "0.1.0-alpha.7",
  "scripts": {
    "res:build": "rescript",
    "res:clean": "rescript clean",
    "res:dev": "rescript build -w"
  },
  "keywords": [
    "rescript"
  ],
  "files": [
    "README.md",
    "CHANGELOG.md",
    "rescript.json",
    "src/**/*",
    "res-x-vite-plugin.mjs"
  ],
  "author": "Gabriel Nordeborn",
  "license": "MIT",
  "peerDependencies": {
    "rescript": ">=11.0.0-rc.5",
    "@rescript/core": ">=0.5.0",
    "vite": ">=4.4.11",
    "rescript-bun": ">=0.1.0"
  },
  "devDependencies": {
    "@rescript/core": "^0.5.0",
    "fast-glob": "^3.3.1",
    "rescript": "11.0.0-rc.5",
    "rescript-bun": "0.1.0"
  },
  "dependencies": {
    "fast-glob": "^3.3.1"
  }
}


```
=========== End file

=========== Start file Handlers.res
```
type htmxHandlerConfig<'ctx> = {
  request: Request.t,
  context: 'ctx,
  headers: Headers.t,
  requestController: RequestController.t,
}

type htmxHandler<'ctx> = htmxHandlerConfig<'ctx> => promise<Jsx.element>

type renderConfig<'ctx> = {
  request: Request.t,
  headers: Headers.t,
  context: 'ctx,
  path: list<string>,
  url: URL.t,
  requestController: RequestController.t,
}

type t<'ctx> = {
  handlers: array<(method, string, htmxHandler<'ctx>)>,
  requestToContext: Request.t => promise<'ctx>,
  asyncLocalStorage: AsyncHooks.AsyncLocalStorage.t<renderConfig<'ctx>>,
}

type hxGet = string
type hxPost = string
type hxPut = string
type hxPatch = string
type hxDelete = string

let make = (~requestToContext) => {
  handlers: [],
  requestToContext,
  asyncLocalStorage: AsyncHooks.AsyncLocalStorage.make(),
}

let useContext = t => t.asyncLocalStorage->AsyncHooks.AsyncLocalStorage.getStoreUnsafe

let defaultRenderTitle = segments => segments->Array.joinWith(" | ")

let renderWithDocType = async (
  el,
  ~requestController: RequestController.t,
  ~renderTitle=defaultRenderTitle,
) => {
  let (content, appendToHead) = await Promise.all2((
    H.renderToString(el),
    requestController->RequestController.getAppendedHeadContent,
  ))

  // TODO: Escape? Hyperons has something

  let appendToHead = switch (appendToHead, requestController->RequestController.getTitleSegments) {
  | (appendToHead, []) => appendToHead
  | (Some(appendToHead), titleSegments) =>
    let titleElement = `<title>${renderTitle(titleSegments)}</title>`
    Some(appendToHead ++ titleElement)
  | (None, titleSegments) => Some(`<title>${renderTitle(titleSegments)}</title>`)
  }

  let content = switch appendToHead {
  | None => content
  | Some(appendToHead) => content->String.replace("</head>", appendToHead ++ "</head>")
  }

  requestController->RequestController.getDocHeader ++ content
}
let defaultHeaders = [("Content-Type", "text/html")]

type handleRequestConfig<'ctx> = {
  request: Request.t,
  server: Bun.Server.t,
  render: renderConfig<'ctx> => promise<Jsx.element>,
  setupHeaders?: unit => Headers.t,
  renderTitle?: array<string> => string,
  experimental_stream?: bool,
}

let handleRequest = async (t, {request, render, ?experimental_stream} as config) => {
  let stream = experimental_stream->Option.getWithDefault(false)

  let url = request->Request.url->URL.make
  let pathname = url->URL.pathname
  let targetHandler = t.handlers->Array.findMap(((handlerType, path, handler)) =>
    if handlerType === request->Request.method && path === pathname {
      Some(handler)
    } else {
      None
    }
  )

  let ctx = await t.requestToContext(request)
  let requestController = RequestController.make()

  let headers = switch config.setupHeaders {
  | Some(setupHeaders) => setupHeaders()
  | None => Headers.make(~init=FromArray(defaultHeaders))
  }
  let renderConfig = {
    context: ctx,
    headers,
    request,
    path: pathname
    ->String.split("/")
    ->Array.filter(s => s->String.trim !== "")
    ->List.fromArray,
    url,
    requestController,
  }

  await t.asyncLocalStorage->AsyncHooks.AsyncLocalStorage.run(renderConfig, async _token => {
    let content = switch targetHandler {
    | None => await render(renderConfig)
    | Some(handler) =>
      await handler({
        request,
        context: ctx,
        headers,
        requestController,
      })
    }

    if stream {
      let {readable, writable} = TransformStream.make({
        transform: (chunk, controller) => {
          controller->TransformStream.Controller.enqueue(chunk)
        },
      })
      let writer = writable->WritableStream.getWriter
      let textEncoder = TextEncoder.make()

      H.renderToStream(content, ~onChunk=chunk => {
        let encoded = textEncoder->TextEncoder.encode(chunk)
        writer->WritableStream.WritableStreamDefaultWriter.write(encoded)->Promise.done
      })
      ->Promise.thenResolve(_ => {
        writer->WritableStream.WritableStreamDefaultWriter.close
      })
      ->Promise.done

      Response.makeFromReadableStream(
        readable,
        ~options={
          status: 200,
          headers: FromArray([("Content-Type", "text/html")]),
        },
      )
    } else {
      let content = await renderWithDocType(
        content,
        ~requestController,
        ~renderTitle=?config.renderTitle,
      )
      switch (
        requestController->RequestController.getCurrentRedirect,
        requestController->RequestController.getCurrentStatus,
      ) {
      | (Some(url, status), _) => Response.makeRedirect(url, ~status?)
      | (None, status) => Response.makeWithHeaders(content, ~options={headers, status})
      }
    }
  })
}

let hxGet = (t, path, ~handler) => {
  t.handlers->Array.push((GET, path, handler))
  path
}
let makeHxGetIdentifier = path => {
  path
}
let implementHxGetIdentifier = (t, path, ~handler) => {
  let _: hxGet = hxGet(t, path, ~handler)
}

let hxPost = (t, path, ~handler) => {
  t.handlers->Array.push((POST, path, handler))
  path
}
let makeHxPostIdentifier = path => {
  path
}
let implementHxPostIdentifier = (t, path, ~handler) => {
  let _: hxPost = hxPost(t, path, ~handler)
}

let hxPut = (t, path, ~handler) => {
  t.handlers->Array.push((PUT, path, handler))
  path
}
let makeHxPutIdentifier = path => {
  path
}
let implementHxPutIdentifier = (t, path, ~handler) => {
  let _: hxPut = hxPut(t, path, ~handler)
}

let hxDelete = (t, path, ~handler) => {
  t.handlers->Array.push((DELETE, path, handler))
  path
}
let makeHxDeleteIdentifier = path => {
  path
}
let implementHxDeleteIdentifier = (t, path, ~handler) => {
  let _: hxDelete = hxDelete(t, path, ~handler)
}

let hxPatch = (t, path, ~handler) => {
  t.handlers->Array.push((PATCH, path, handler))
  path
}
let makeHxPatchIdentifier = path => {
  path
}
let implementHxPatchIdentifier = (t, path, ~handler) => {
  let _: hxPatch = hxPatch(t, path, ~handler)
}

module Internal = {
  let getHandlers = t => t.handlers
}

```
=========== End file

=========== Start file Handlers.resi
```
type htmxHandlerConfig<'ctx> = {
  request: Request.t,
  context: 'ctx,
  headers: Headers.t,
  requestController: RequestController.t,
}

type htmxHandler<'ctx> = htmxHandlerConfig<'ctx> => promise<Jsx.element>

type t<'ctx>

type hxGet
type hxPost
type hxPut
type hxPatch
type hxDelete

let make: (~requestToContext: Request.t => promise<'ctx>) => t<'ctx>

let hxGet: (t<'ctx>, string, ~handler: htmxHandler<'ctx>) => hxGet
let makeHxGetIdentifier: string => hxGet
let implementHxGetIdentifier: (t<'ctx>, hxGet, ~handler: htmxHandler<'ctx>) => unit

let hxPost: (t<'ctx>, string, ~handler: htmxHandler<'ctx>) => hxPost
let makeHxPostIdentifier: string => hxPost
let implementHxPostIdentifier: (t<'ctx>, hxPost, ~handler: htmxHandler<'ctx>) => unit

let hxPut: (t<'ctx>, string, ~handler: htmxHandler<'ctx>) => hxPut
let makeHxPutIdentifier: string => hxPut
let implementHxPutIdentifier: (t<'ctx>, hxPut, ~handler: htmxHandler<'ctx>) => unit

let hxDelete: (t<'ctx>, string, ~handler: htmxHandler<'ctx>) => hxDelete
let makeHxDeleteIdentifier: string => hxDelete
let implementHxDeleteIdentifier: (t<'ctx>, hxDelete, ~handler: htmxHandler<'ctx>) => unit

let hxPatch: (t<'ctx>, string, ~handler: htmxHandler<'ctx>) => hxPatch
let makeHxPatchIdentifier: string => hxPatch
let implementHxPatchIdentifier: (t<'ctx>, hxPatch, ~handler: htmxHandler<'ctx>) => unit

type renderConfig<'ctx> = {
  request: Request.t,
  headers: Headers.t,
  context: 'ctx,
  path: list<string>,
  url: URL.t,
  requestController: RequestController.t,
}

let useContext: t<'ctx> => renderConfig<'ctx>

type handleRequestConfig<'ctx> = {
  request: Request.t,
  server: Bun.Server.t,
  render: renderConfig<'ctx> => promise<Jsx.element>,
  setupHeaders?: unit => Headers.t,
  renderTitle?: array<string> => string,
  experimental_stream?: bool,
}

let handleRequest: (t<'ctx>, handleRequestConfig<'ctx>) => promise<Response.t>

module Internal: {
  let getHandlers: t<'ctx> => array<(method, string, htmxHandler<'ctx>)>
}

```
=========== End file