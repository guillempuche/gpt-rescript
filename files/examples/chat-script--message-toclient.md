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

=========== Start file Message__ToClient.res
```
open Message__JSON

type t = {
  from: string,
  message: string,
  timestamp: float,
}

let getServerUsername = () => "server"

let create = (~from, ~message) => {
  let timestamp = Date.now()
  let message = {
    from,
    message,
    timestamp,
  }

  message
}

let encode = (message) => {
  [
    ("from", String(message.from)),
    ("message", String(message.message)),
    ("timestamp", Number(message.timestamp)),
  ]
  -> Dict.fromArray
  -> Object
}

let serializeOne = (payload) => {
  payload
  -> encode
  -> stringify
}

let serializeMany = (payload) => {
  payload
  -> Array.map(encode)
  -> Array
  -> stringify
}

let decode = (json) => {
  switch json {
    | Object(dict) => {
      let from = Dict.get(dict, "from")
      let message = Dict.get(dict, "message")
      let timestamp = Dict.get(dict, "timestamp")

      switch (from, message, timestamp) {
        | (
          Some(String(from)),
          Some(String(message)),
          Some(Number(timestamp)),
        ) if from !== "" && message !== "" => Ok({ from, message, timestamp })
        | _ => Error("Expected non empty string from, string message and number timestamp")
      }
    }
    | _ => Error("Expected an object")
  }
}

let deserializeOne = (payload) => {
  switch parse(payload) {
    | Error(errMsg) => Error("Error parsing JSON: " ++ errMsg)
    | Ok(json) => decode(json)
  }
}

let deserializeMany = (payload) => {
  switch parse(payload) {
    | Error(errMsg) => Error("Error parsing JSON: " ++ errMsg)
    | Ok(Array(jsons)) => {
      let decodedJsons = Array.map(jsons, decode)
      let successes = []
      let failures = []
      
      Array.forEach(decodedJsons, (json) => switch json {
        | Error(error) => Array.push(failures, error)
        | Ok(json) => Array.push(successes, json)
      })

      if Array.length(failures) > 0 {
        failures
        -> Array.joinWith(", ")
        -> Error
      } else {
        Ok(successes)
      }
    }
    | _ => Error("Expected an array")
  }
}

```
=========== End file

=========== Start file Message_ToClient.resi
```
type t = {
  from: string,
  message: string,
  timestamp: float,
}

let getServerUsername: () => string

let create: (~from: string, ~message: string) => t

let serializeOne: (t) => result<string, string>

let serializeMany: (array<t>) => result<string, string>

let deserializeOne: (string) => result<t, string>

let deserializeMany: (string) => result<array<t>, string>
```
=========== End file