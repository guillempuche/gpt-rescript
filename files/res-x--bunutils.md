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

=========== Start file BunUtils.res
```
external process: 'process = "process"

let isDev = process["env"]["NODE_ENV"] !== "production"

type globConfig = {
  dot?: bool,
  cwd?: string,
}

@module("fast-glob")
external glob: (array<string>, globConfig) => promise<array<string>> = "glob"

let loadStaticFiles = async (~root=?) => {
  await glob(
    switch isDev {
    | true => ["public/**/*", "assets/**/*"]
    | false => ["dist/**/*"]
    },
    {
      dot: true,
      cwd: switch root {
      | None => process["cwd"]()
      | Some(cwd) => cwd
      },
    },
  )
}

let staticFiles = ref(None)

let serveStaticFile = async request => {
  open Bun

  let staticFiles = switch staticFiles.contents {
  | None =>
    let files = await loadStaticFiles()
    let files =
      files
      ->Array.map(f => {
        (
          switch isDev {
          | true if f->String.startsWith("public/") => f->String.sliceToEnd(~start=7)
          | false if f->String.startsWith("dist/") => f->String.sliceToEnd(~start=5)
          | _ => f
          },
          f,
        )
      })
      ->Map.fromArray
    staticFiles := Some(files)
    files
  | Some(s) => s
  }

  let url = request->Request.url->URL.make
  let pathname = url->URL.pathname

  let path = pathname->String.split("/")->Array.filter(p => p !== "")
  let joined = path->Array.joinWith("/")

  switch staticFiles->Map.get(joined) {
  | None => None
  | Some(fileLoc) =>
    let bunFile = Bun.file("./" ++ fileLoc)

    Some(
      switch bunFile->BunFile.size {
      | 0. => Response.make("", ~options={status: 404})
      | _ => Response.makeFromFile(bunFile)
      },
    )
  }
}

let runDevServer = (~port) => {
  let _devServer = Bun.serveWithWebSocket({
    port: port + 1,
    development: true,
    websocket: {
      open_: _v => {
        ()
      },
    },
    fetch: async (request, server) => {
      open Bun

      if server->Server.upgrade(request) {
        Response.defer
      } else {
        Response.make("", ~options={status: 404})
      }
    },
  })
}

module URLSearchParams = {
  let copy = search =>
    URLSearchParams.makeWithInit(
      search
      ->URLSearchParams.entries
      ->Dict.fromIterator
      ->Object,
    )
}

```
=========== End file

=========== Start file BunUtils.resi
```
let serveStaticFile: Request.t => promise<option<Response.t>>

let runDevServer: (~port: int) => unit

let isDev: bool

module URLSearchParams: {
  let copy: URLSearchParams.t => URLSearchParams.t
}

```
=========== End file