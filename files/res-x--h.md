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

=========== Start file H.res
```
@val external null: Jsx.element = "null"

external float: float => Jsx.element = "%identity"
external int: int => Jsx.element = "%identity"
external string: string => Jsx.element = "%identity"
external array: array<Jsx.element> => Jsx.element = "%identity"

@module("./vendor/hyperons.js")
external renderToString: Jsx.element => promise<string> = "render"

@module("./vendor/hyperons.js")
external renderToStream: (Jsx.element, ~onChunk: string => unit=?) => promise<unit> = "render"

module Context = {
  type t<'context>

  type props<'context> = {
    value: 'context,
    children: Jsx.element,
  }

  @module("./vendor/hyperons.js")
  external createContext: 'context => t<'context> = "createContext"

  @module("./vendor/hyperons.js")
  external useContext: t<'context> => 'context = "useContext"

  @get external provider: t<'context> => Jsx.component<props<'context>> = "Provider"
}

module Fragment = {
  type fragmentProps = {children: Jsx.element}
  @module("./vendor/hyperons.js")
  external make: fragmentProps => Jsx.element = "Fragment"
}

```
=========== End file