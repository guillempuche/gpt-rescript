Rescript v11

Repo: https://github.com/Exegetech/chat-rescript

=========== Start file package.json (part or full code)
```
{
  "name": "backend",
  "scripts": {
    "res:build": "rescript",
    "res:clean": "rescript clean",
    "res:dev": "rescript build -w",
    "dev": "NODE_ENV=dev nodemon src/Server.bs.mjs",
    "build": "node scripts/build.js"
  },
  "dependencies": {
    "@fastify/cors": "8.4.0",
    "@fastify/static": "6.11.2",
    "@fastify/websocket": "8.2.0",
    "@rescript/core": "0.5.0",
    "fastify": "4.24.1",
    "rescript": "11.0.0-rc.4",
    "shared": "workspace:*"
  },
  "devDependencies": {
    "esbuild": "0.19.5",
    "nodemon": "3.0.1"
  }
}
```
=========== End file

=========== Start file Server.res
```
open Fastify

let env = Dict.get(Node.Process.env, "NODE_ENV")

@val external importMetaUrl: string = "import.meta.url"

let dirname = importMetaUrl
  -> Node.Url.fileURLToPath
  -> Node.Path.dirname

let fastify = create({ logger: true })

switch env {
  | None => {
    fastify->registerStatic(fastifyStatic, {
      root: Node.Path.join(dirname, "public"),
    })
  }
  | _ => ()
}

fastify->register(fastifyCors)
fastify->register(fastifyWebsocket)

fastify->addHook(PreValidation, async (request, reply) => {
  let path = request.routeOptions.url
  let username = Dict.get(request.query, "username")

  switch (path, username) {
    | ("/chat", None) => reply
      ->HTTP.code(Forbidden)
      ->HTTP.send("Connection rejected")
    | _ => ()
  }
})

fastify->httpGet("/chat", async (_request, reply) => {
  let payload = Chat.getChatHistory()
    -> Message.ToClient.serializeMany

  switch payload {
    | Error(error) => fastify.log->Log.logError(error)
    | Ok(payload) => reply
      ->HTTP.code(Okay)
      ->HTTP.send(payload)
  }
})

fastify->register(async (fastify) => {
  fastify->socketGet("/room", (connection, request) => {
    let username = request.query
      -> Dict.get("username")
      -> Option.getExn
    
    Chat.handleClient(~username, ~socket=connection.socket, ~onError=(errMsg) => {
      fastify.log->Log.logError(errMsg)
    })
  })
})

let start = async () => {
  try {
    await fastify->listen({ port: 3000 })
  } catch {
    | Exn.Error(obj) =>
      switch Exn.message(obj) {
        | Some(m) => fastify.log->Log.logError(m)
	| None => ()
      }

      Node.Process.exit(1)
  }
}

let _ = await start()
```
=========== End file