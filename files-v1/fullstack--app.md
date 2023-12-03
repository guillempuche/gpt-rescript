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

=========== Start file App.res
```
// This type is based on the getInitialProps return value.
// If you are using getServerSideProps or getStaticProps, you probably
// will never need this
// See https://nextjs.org/docs/advanced-features/custom-app
type pageProps

module PageComponent = {
  type t = React.component<pageProps>
}

type props = {
  @as("Component")
  component: PageComponent.t,
  pageProps: pageProps,
}

// We are not using `@react.component` since we will never
// use <App/> within our ReScript code.
// It's only used within `pages/_app.js`
let default = (props: props): React.element => {
  let {component, pageProps} = props

  let router = Next.Router.useRouter()

  let content = React.createElement(component, pageProps)

  switch router.route {
  | "/examples" => <MainLayout> content </MainLayout>
  | _ => <MainLayout> content </MainLayout>
  }
}
```
=========== End file

=========== Start file App.resi
```
type props
let default: props => React.element

```
=========== End file