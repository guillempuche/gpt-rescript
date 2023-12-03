Rescript v11

Repo: https://github.com/Exegetech/chat-rescript

=========== Start file package.json (part or full code)
```
{
  "name": "shared",
  "scripts": {
    "res:build": "rescript",
    "res:clean": "rescript clean",
    "res:dev": "rescript build -w"
  },
  "dependencies": {
    "@rescript/core": "0.5.0",
    "rescript": "11.0.0-rc.4"
  }
}

```
=========== End file

=========== Start file Message__JSON.res
```
@unboxed
type rec json =
  | @as(false) False
  | @as(true) True
  | @as(null) Null
  | String(string)
  | Number(float)
  | Object(Dict.t<json>)
  | Array(array<json>)

@val
@scope("JSON")
external parseExn: string => json = "parse"

@val
@scope("JSON")
external stringifyExn: json => string = "stringify"

let parse = (payload: string): result<json, string> => {
  try {
    payload
    -> parseExn
    -> Ok
  } catch {
    | Exn.Error(obj) => {
      switch Exn.message(obj) {
        | Some(msg) => Error(msg)
        | None => Error("Unknown error")
      }
    }
  }
}

let stringify = (payload: json): result<string, string> => {
  try {
    payload
    -> stringifyExn
    -> Ok
  } catch {
    | Exn.Error(obj) => {
      switch Exn.message(obj) {
        | Some(msg) => Error(msg)
        | None => Error("Unknown error")
      }
    }
  }
}

```
=========== End file

=========== Start file Message__JSON.resi
```
@unboxed
type rec json =
  | @as(false) False
  | @as(true) True
  | @as(null) Null
  | String(string)
  | Number(float)
  | Object(Dict.t<json>)
  | Array(array<json>)

let parse: (string) => result<json, string> 
let stringify: (json) => result<string, string>

```
=========== End file