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

=========== Start file Dsfr.res
```
type linkProps = {"href": string, "title": string}

module Spa = {
  type startReactDsfrParams<'props> = {
    defaultColorScheme: [#light | #dark | #system],
    verbose?: bool,
    @as("Link") link: 'props => React.element,
    useLang?: unit => [#fr | #en],
  }

  @module("@codegouvfr/react-dsfr/spa")
  external startReactDsfr: startReactDsfrParams<'props> => unit = "startReactDsfr"
}

module Badge = {
  type severity = [#success | #info | #warning | #error]
  type tag = [#span | #div | #p]
  @react.component @module("@codegouvfr/react-dsfr/Badge")
  external make: (
    ~className: string=?,
    ~children: React.element,
    ~noIcon: bool=?,
    ~small: bool=?,
    ~severity: severity=?,
    @as("as") ~as_: tag=?,
  ) => React.element = "default"
}

module Breadcrumb = {
  type segment = {label: string, linkProps: linkProps}
  @react.component @module("@codegouvfr/react-dsfr/Breadcrumb")
  external make: (
    ~id: string=?,
    ~className: string=?,
    ~homeLinkProps: linkProps=?,
    ~segments: array<segment>,
    ~currentPageLabel: string=?,
  ) => React.element = "default"
}

module Button = {
  type options = {
    disabled?: bool,
    iconId?: string,
    iconPosition?: string,
    onClick: JsxEvent.Mouse.t => unit,
    priority?: string,
    size?: string,
    children: React.element,
  }

  @react.component @module("@codegouvfr/react-dsfr/Button")
  external make: (
    ~children: React.element,
    ~disabled: bool=?,
    ~iconId: string=?,
    ~iconPosition: string=?,
    ~onClick: JsxEvent.Mouse.t => unit,
    ~priority: string=?,
    ~size: string=?,
  ) => React.element = "default"
}

module ButtonsGroup = {
  @react.component @module("@codegouvfr/react-dsfr/ButtonsGroup")
  external make: (
    ~alignment: string=?,
    ~buttonsSize: string=?,
    ~buttonsIconPosition: string=?,
    ~buttonsEquisized: bool=?,
    ~buttons: array<Button.options>,
    ~inlineLayoutWhen: string=?,
    ~className: string=?,
  ) => React.element = "default"
}

module CallOut = {
  @react.component @module("@codegouvfr/react-dsfr/CallOut")
  external make: (~title: string=?, ~children: React.element, ~iconId: string=?) => React.element =
    "default"
}

module Card = {
  @react.component @module("@codegouvfr/react-dsfr/Card")
  external make: (
    ~title: string,
    ~desc: string,
    ~linkProps: linkProps,
    ~enlargeLink: bool=?,
    ~size: string=?,
  ) => React.element = "default"
}

module Header = {
  @react.component @module("@codegouvfr/react-dsfr/Header")
  external make: (
    ~brandTop: React.element=?,
    ~homeLinkProps: linkProps,
    ~serviceTagline: string,
    ~operatorLogo: {"alt": string, "imgUrl": string, "orientation": string}=?,
    ~serviceTitle: React.element,
  ) => React.element = "default"
}

module Footer = {
  @react.component @module("@codegouvfr/react-dsfr/Footer")
  external make: (
    ~accessibility: string,
    ~brandTop: React.element=?,
    ~contentDescription: React.element=?,
    ~homeLinkProps: linkProps=?,
    ~bottomItems: array<'button>=?,
    ~license: React.element=?,
  ) => React.element = "default"
}

module Display = {
  @module("@codegouvfr/react-dsfr/Display")
  external headerFooterDisplayItem: 'button = "headerFooterDisplayItem"
}

module Notice = {
  @react.component @module("@codegouvfr/react-dsfr/Notice")
  external make: (~title: string, ~isClosable: bool=?) => React.element = "default"
}

```
=========== End file