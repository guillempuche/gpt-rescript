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

=========== Start file Client.res
```
module Actions: {
  type t

  @tag("kind")
  type target = This | CssSelector({selector: string})

  @tag("kind")
  type action =
    | ToggleClass({target: target, className: string})
    | RemoveClass({target: target, className: string})
    | AddClass({target: target, className: string})
    | RemoveElement({target: target})

  let make: array<action> => t
} = {
  type t = string

  @tag("kind")
  type target = This | CssSelector({selector: string})

  @tag("kind")
  type action =
    | ToggleClass({target: target, className: string})
    | RemoveClass({target: target, className: string})
    | AddClass({target: target, className: string})
    | RemoveElement({target: target})

  external stringifyActions: array<action> => string = "JSON.stringify"

  let make = actions => stringifyActions(actions)
}

module ValidityMessage: {
  type config = {
    badInput?: string,
    patternMismatch?: string,
    rangeOverflow?: string,
    rangeUnderflow?: string,
    stepMismatch?: string,
    tooLong?: string,
    tooShort?: string,
    typeMismatch?: string,
    valueMissing?: string,
  }

  type t

  let make: config => t
} = {
  type config = {
    badInput?: string,
    patternMismatch?: string,
    rangeOverflow?: string,
    rangeUnderflow?: string,
    stepMismatch?: string,
    tooLong?: string,
    tooShort?: string,
    typeMismatch?: string,
    valueMissing?: string,
  }

  type t = string

  external stringifyConfig: config => string = "JSON.stringify"

  let make = config => stringifyConfig(config)
}

```
=========== End file