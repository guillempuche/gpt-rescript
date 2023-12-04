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

=========== Start file StaticExporter.res
```
open Bun

external process: 'a = "process"
external fetch: string => promise<Response.t> = "fetch"

let debugging = true

let debug = s =>
  if debugging {
    Console.log2("[debug]", s)
  }

let log = s => Console.log2("[info]", s)

let run = async (server: Server.t, ~urls: array<string>) => {
  let serverUrl = `http://${server->Server.hostname}:${server->Server.port->Int.toString}`
  log(`Exporting ${urls->Array.length->Int.toString} URLs.`)

  let _ = await Promise.all(
    urls->Array.map(async url => {
      log(`[export] ${url} - Exporting...`)
      let res = await fetch(serverUrl ++ url)

      switch res->Response.status {
      | 200 =>
        let structure =
          url
          ->String.split("/")
          ->Array.filter(p => p !== "")
          ->Array.toReversed

        let (sliceStart, fileName) = switch structure->Array.get(0) {
        | None | Some("") => (0, "index.html")
        | Some(f) => (1, f ++ ".html")
        }

        structure->Array.push("dist")

        let dirStructure = structure->Array.sliceToEnd(~start=sliceStart)->Array.toReversed

        switch dirStructure {
        | [] => ()
        | dirStructure =>
          await Fs.mkdir(dirStructure->Array.joinWith("/"), ~options={recursive: true})
        }

        dirStructure->Array.push(fileName)
        let filePath = dirStructure->Array.joinWith("/")

        await Fs.writeFile(filePath, await res->Response.text)
        log(`[export] ${url} - Wrote ${filePath}.`)

      | otherStatus => Console.error(url ++ " gave status " ++ otherStatus->Int.toString)
      }
    }),
  )

  log("Done.")

  server->Server.stop(~closeActiveConnections=true)
  process["exit"](0)
}

```
=========== End file