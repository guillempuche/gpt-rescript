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

=========== Start file Chat__Box.res
```
module Bubble = Chat__Bubble
module Input = Chat__Input

@react.component
let make = (
  ~chats: array<Message.ToClient.t>,
  ~currentUser: string,
  ~onSubmit: (string, string) => (),
) => {
  let bottomRef = React.useRef(Nullable.null)

  React.useEffect1(() => {
    switch Nullable.toOption(bottomRef.current) {
      | Some(dom) => dom->AppDom.scrollIntoView
      | None => ()
    }

    None
  }, [chats]);

  let usersColor = Util.makeUsersColorDict(currentUser, chats)

  let handleSubmit = (message) => {
    onSubmit(currentUser, message)
  }

  <div>
    <div className=`
      bg-slate-100
      p-4
      h-[40rem]
      overflow-y-scroll
      rounded-t-lg
    `>
      {Array.mapWithIndex(chats, (chat, idx) => {
        <Bubble
          key={Int.toString(idx)}
          usersColor
          currentUser
          chat
        />
      })->React.array}

      <div ref={ReactDOM.Ref.domRef(bottomRef)} />
    </div>

    <Input
      onSubmit={handleSubmit}
    />
  </div>
}


```
=========== End file

=========== Start file Chat__Box.resi
```
@react.component
let make: (
  ~chats: array<Message.ToClient.t>,
  ~currentUser: string,
  ~onSubmit: (string, string) => (),
) => Jsx.element
```
=========== End file