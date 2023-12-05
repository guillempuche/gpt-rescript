Rescript v10

Repo: https://github.com/skonky/fullstack

=========== Start file package.json (part or full code)
```
{
  "name": "rescript-web",
  "version": "0.0.0",
  "author": "skonky",
  "private": true,
  "license": "Apache-2.0",
  "dependencies": {
    "next": "10.2.3",
    "react": "17.0.1",
    "react-dom": "17.0.1"
  },
  "scripts": {
    "dev": "concurrently \"next dev -p 5000\" \"rescript build -w\"",
    "debug": "NODE_OPTIONS='--inspect' next",
    "build": "rescript && next build",
    "now-build": "rescript && next build",
    "export": "next export",
    "start": "next start -p $PORT",
    "res:build": "rescript",
    "res:clean": "rescript clean",
    "res:start": "rescript build -w"
  },
  "devDependencies": {
    "@rescript/react": "0.10.3",
    "autoprefixer": "10.1.0",
    "concurrently": "^7.6.0",
    "cssnano": "5.0.5",
    "daisyui": "^2.51.3",
    "gentype": "4.1",
    "next-transpile-modules": "7.1.2",
    "postcss": "8.2.15",
    "postcss-cli": "8.3.1",
    "rescript": "9.1",
    "tailwindcss": "^3.0.23"
  }
}

```
=========== End file

=========== Start file Examples.res
```
type todo = {
  id: int,
  title: string,
  isDone: bool,
}

type state = {newTodoValue: string, todos: array<todo>}

let initialState: state = {
  newTodoValue: "",
  todos: [
    {
      id: 1,
      title: "Initial todo",
      isDone: false,
    },
  ],
}

type actions =
  | CreateTodo
  | InputChanged(string)
  | RemoveTodo(int)
  | ClearCompleted
  | ToggleTodoStatus(int)

let reducer = (state, action) => {
  switch action {
  | CreateTodo => {
      newTodoValue: "",
      todos: Js.Array.concat(
        [
          {
            title: state.newTodoValue,
            isDone: false,
            id: state.todos->Js.Array2.length + 1,
          },
        ],
        state.todos,
      ),
    }
  | InputChanged(newTodoValue) => {
      ...state,
      newTodoValue: newTodoValue,
    }
  | RemoveTodo(id) => {
      ...state,
      todos: state.todos->Js.Array2.filter(t => t.id != id),
    }
  | ClearCompleted => {
      ...state,
      todos: state.todos->Js.Array2.filter(todo => !todo.isDone),
    }
  | ToggleTodoStatus(id) => {
      ...state,
      todos: state.todos->Js.Array2.map(todo => {
        if todo.id == id {
          {
            ...todo,
            isDone: !todo.isDone,
          }
        } else {
          todo
        }
      }),
    }
  }
}

let default = () => {
  open Js.Array2

  let (state, dispatch) = React.useReducer(reducer, initialState)
  let handleClearAllCompletedTodos = _ => dispatch(ClearCompleted)

  let noTodosCompleted = state.todos->Js.Array2.find(todo => todo.isDone)->Belt.Option.isNone

  let handleChange = event => {
    let value = ReactEvent.Form.target(event)["value"]
    dispatch(InputChanged(value))
  }

  let handleCreateTodo = _ => {
    dispatch(CreateTodo)
  }

  let handleDelete = (id, _) => {
    dispatch(RemoveTodo(id))
  }

  let handleToggleTodoStatus = (id, _) => {
    dispatch(ToggleTodoStatus(id))
  }

  <div className="p-6">
    <input
      value=state.newTodoValue
      onChange={handleChange}
      className="input input-bordered mr-5"
      placeholder="Type here"
    />
    <button onClick={handleCreateTodo} className="btn btn-primary mr-3">
      {"Create"->React.string}
    </button>
    <button
      disabled=noTodosCompleted onClick={handleClearAllCompletedTodos} className="btn btn-success">
      {"Clear completed"->React.string}
    </button>
    <div className="overflow-x-auto">
      <table className="table w-full mt-6">
        <thead>
          <tr>
            <th> {"#"->React.string} </th>
            <th> {"Name"->React.string} </th>
            <th className="text-right"> {"Controls"->React.string} </th>
          </tr>
        </thead>
        <tbody>
          {state.todos
          ->map(todo => {
            let todoClassName = todo.isDone ? "p-3 line-through opacity-50" : "p-3"
            <tr key={Belt.Int.toString(todo.id)}>
              <td> {Belt.Int.toString(todo.id)->React.string} </td>
              <td className=todoClassName> {todo.title->React.string} </td>
              <td className="text-right">
                <button onClick={handleToggleTodoStatus(todo.id)} className="btn ml-3">
                  {"toggle"->React.string}
                </button>
                <button onClick={handleDelete(todo.id)} className="btn btn-error ml-3">
                  {"delete"->React.string}
                </button>
              </td>
            </tr>
          })
          ->React.array}
        </tbody>
      </table>
    </div>
  </div>
}

```
=========== End file

=========== Start file Examples.resi
```
let default: unit => React.element
```
=========== End file