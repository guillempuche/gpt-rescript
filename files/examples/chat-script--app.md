Rescript v11

Repo: https://github.com/Exegetech/chat-rescript

=========== Start file package.json (part or full code)
```
{
  "name": "frontend",
  "scripts": {
    "res:build": "rescript",
    "res:clean": "rescript clean",
    "res:dev": "rescript build -w",
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "@rescript/core": "0.5.0",
    "@rescript/react": "0.11.0",
    "shared": "workspace:*",
    "daisyui": "3.9.2",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "rescript": "11.0.0-rc.4"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "4.0.0",
    "autoprefixer": "10.4.15",
    "postcss": "8.4.28",
    "tailwindcss": "3.3.3",
    "vite": "4.4.9"
  }
}
```
=========== End file


// =========== Start App.res file
module ChatBox = Chat__Box

@react.component
let make = () => {
  let (username, setUsername) = React.useState(() => "")
  let (chats, setChats) = React.useState(() => [])
  let socket = React.useRef(None)

  React.useEffect1(() => {
    let run = async () => {
      switch username {
        | "" => ()
        | username => {
          let chatHistory = await Util.fetchChatHistory(username)
          switch chatHistory {
            | Error(error) => {
              Console.error(error)
            }
            | Ok(chatHistory) => setChats((_prev) => chatHistory)
          }

          let url = `ws://localhost:3000/room?username=${username}`
          let ws = WebSocket.create(url)

          ws->WebSocket.set_onOpen(() => {
            Console.log("Connected to websocket")
          })

          ws->WebSocket.set_onMessage((event) => {
            let payload = Message.ToClient.deserializeOne(event.data)
            switch payload {
              | Error(error) => {
                Console.error(error)
              }
              | Ok(payload) => {
                setChats((prev) => {
                  let newArr = Array.copy(prev)
                  Array.push(newArr, payload)

                  newArr
                })
              }
            }
          })

          socket.current = Some(ws)
        }
      }
    }

    let _ = run()

    Some(() => {
      switch socket.current {
        | None => ()
        | Some(ws) => WebSocket.close(ws)
      }
    })
  }, [username])

  let handleUsernameSubmit = (username) => {
    setUsername((_prev) => username)
  }

  let handleChatSubmit = (from, message) => {
    switch socket.current {
      | None => ()
      | Some(ws) => {
        open Message

        let payload = ToServer.create(~from, ~message)
          -> Message.ToServer.serialize

        switch payload {
          | Error(errMsg) => Console.error(errMsg)
          | Ok(payload) => ws->WebSocket.send(payload)
        }
      }
    }
  }

  <div className=`
    container
    mx-auto
    h-screen
    w-1/3
    flex
    flex-col
  `>
    <div className="mt-8">
      {switch username {
        | "" => (
          <Login
            onSubmit={handleUsernameSubmit}
          />
        )
        | username => (
          <ChatBox
            chats={chats}
            currentUser={username}
            onSubmit={handleChatSubmit}
          />
        )
      }}
    </div>
  </div>
}
// =========== End file

// =========== Start file App.resi
@react.component
let make: unit => Jsx.element
// =========== End file
