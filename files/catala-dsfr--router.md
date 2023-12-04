Rescript v10

Repo: https://github.com/CatalaLang/catala-dsfr

=========== Start file package.json (part or full code)
```
{
  "name": "catala-dsfr",
  "version": "0.1.1",
  "repository": "https://github.com/CatalaLang/catala-dsfr",
  "scripts": {
    "clean": "rescript clean -with-deps",
    "build": "yarn run pre && vite build",
    "deploy": "yarn run build --base=/demos/catala/ && rsync -rv --delete-before dist/*",
    "serve": "vite preview",
    "dev": "yarn run pre && vite",
    "re:build": "rescript build -with-deps",
    "re:watch": "yarn run pre && rescript build -w -with-deps",
    "assets": "rsync -r node_modules/@catala-lang/catala-web-assets/assets/* assets",
    "postinstall": "copy-dsfr-to-public",
    "pre": "yarn run re:build && only-include-used-icons && yarn run assets"
  },
  "keywords": [
    "rescript"
  ],
  "author": "Emile Rolley <emile.rolley@tuta.io>",
  "license": "Apache-2.0",
  "dependencies": {
    "@catala-lang/catala-explain": "^0.2.2",
    "@catala-lang/catala-web-assets": "^0.8.9",
    "@catala-lang/french-law": "^0.8.3-b.3",
    "@catala-lang/rescript-catala": "^0.8.1-b.0",
    "@codegouvfr/react-dsfr": "^0.78.2",
    "@rescript/core": "^0.5.0",
    "@rescript/react": "^0.11.0",
    "@rjsf/core": "^5.1.0",
    "@rjsf/utils": "^5.1.0",
    "@rjsf/validator-ajv8": "^5.1.0",
    "file-saver": "^2.0.5",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-loader-spinner": "^5.4.5",
    "rescript-docx": "^0.1.5",
    "tslib": "^2.6.2"
  },
  "devDependencies": {
    "@jihchi/vite-plugin-rescript": "^5.1.0",
    "@originjs/vite-plugin-commonjs": "^1.0.3",
    "@vitejs/plugin-react": "^3.1.0",
    "jsdom": "^21.1.0",
    "rescript": "^10.1.4",
    "tailwindcss": "^3.2.6",
    "vite": "^4.4.9"
  }
}

```
=========== End file

=========== Start file Router.res
```
@react.component
let make = () => {
  switch Nav.getCurrentURL().path {
  | list{route} if route == AllocationsFamiliales.FormInfos.url => <AllocationsFamiliales />
  | list{route} if route == AidesLogement.FormInfos.url => <AidesLogement />
  | list{route, "sources"} if route == AllocationsFamiliales.FormInfos.url =>
    <SourceCode
      html={WebAssets.allocationsFamilialesAssets.html}
      simulatorUrl={AllocationsFamiliales.FormInfos.url}
    />
  | list{route, "sources"} if route == AidesLogement.FormInfos.url =>
    <SourceCode
      html={WebAssets.aidesLogementAssets.html} simulatorUrl={AidesLogement.FormInfos.url}
    />
  | _ => <Home />
  }
}

module Link = {
  @react.component
  let make = (~href: string, ~children) => {
    <a
      href={href}
      onClick={evt => {
        evt->ReactEvent.Mouse.preventDefault
        href->Nav.goTo
      }}>
      children
    </a>
  }
}

```
=========== End file