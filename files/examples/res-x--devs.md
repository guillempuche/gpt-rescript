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

=========== Start file Dev.res
```
module React = ResX__React
module ReactDOM = ResX__ReactDOM

let getScript = (~port) =>
  `(() => {
let hasMadeInitialConnection = false;
let timeout;
let socket = null;
let reconnectInterval;
let debugging = true;

let debug = (...msg) => {
  if (debugging) {
    console.log(...msg)
  }
}

function reload() {
  clearTimeout(timeout)
  timeout = setTimeout(() => {
    window.location.reload()
  }, 200)
}

function connect() {
  clearInterval(reconnectInterval)
  reconnectInterval = setInterval(() => {
    if (socket == null || socket.readyState === 2 || socket.readyState === 3) {
      bootSocket()
    } else if (socket != null && (socket.readyState === 0 || socket.readyState === 1)) {
      clearInterval(reconnectInterval)
    }
  }, 200)
}

function updateContent() {
  fetch(document.location.href).then(async res => {
    let text = await res.text()
    try {
      let domParser = new DOMParser()
      let fromDom = document.documentElement
      let toDom = domParser.parseFromString(text, "text/html").querySelector("html")
      morphdom(fromDom, toDom, {
        onBeforeElUpdated: function(fromEl, toEl) {
          if (fromEl.isEqualNode(toEl)) {
            return false;
          }
          
          if (fromEl.tagName === 'INPUT') {
            if (fromEl.type === 'checkbox' || fromEl.type === 'radio') {
              toEl.checked = fromEl.checked;
            } else {
              toEl.value = fromEl.value;
            }
          } else if (fromEl.tagName === 'TEXTAREA') {
            toEl.value = fromEl.value;
          }

          if (fromEl.tagName === 'SELECT') {
            toEl.selectedIndex = fromEl.selectedIndex;
          }

          return true;
        }
      })
      debug("[dev] Content reloaded.")
    } catch(e) {
      console.warn("[dev] Error morphing DOM. Doing full reload.")
      console.error(e)
      document.documentElement.innerHTML = text

    }
  })
}

function bootSocket() {
  socket = new WebSocket("ws://localhost:${(port + 1)->Int.toString}")
  socket.addEventListener("close", event => {
    debug("[dev] Server restarting")
    if (event.isTrusted) {
      socket = null
      connect()
    }
  })
  socket.addEventListener("open", event => {
    debug("[dev] Server connection opened.")
    if (hasMadeInitialConnection) {
      updateContent()
    }
    hasMadeInitialConnection = true
  })
}

bootSocket()
})()
`

@react.component
let make = (~port=4444) => {
  if BunUtils.isDev {
    [
      <script dangerouslySetInnerHTML={{"__html": getScript(~port)}} />,
      <script src="https://unpkg.com/morphdom/dist/morphdom-umd.js" />,
      <script type_="module" src="http://localhost:9000/@vite/client" />,
    ]->H.array
  } else {
    H.null
  }
}

```
=========== End file