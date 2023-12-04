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

=========== Start file Form.res
```
/*
  Binding for the React component [JSONSchemaForm.default] of the package
  [react-jsonschema-form].

  The component is capable of building HTML forms out of a JSON schema.
*/
module RjsfFormDsfrLazy = {
  @react.component @module("./RjsfFormDsfrLazy.tsx")
  external make: (
    ~onChange: Js.Dict.t<Js.Json.t> => unit=?,
    ~onSubmit: Js.Dict.t<Js.Json.t> => unit=?,
    ~onError: _ => unit=?,
    ~schema: Js.Json.t,
    ~uiSchema: Js.Json.t=?,
    ~formData: Js.Json.t=?,
  ) => React.element = "default"
}

// Function to download or import a JSON object
@val external downloadJSONstring: string => unit = "downloadJSONstring"
%%raw(`
const downloadJSONstring = (data) => {
  const blob = new Blob([data],{type:'application/json'});
  const href = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = href;
  link.download = "data.json";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
`)

// Function to read a file and get its contents as string
@val external readFileAsJSON: (Js.Json.t, Js.Json.t => 'a) => unit = "readFileAsJSON"
%%raw(`
const readFileAsJSON = (file, callback) => {
  var reader = new FileReader();
  var contents = ""
  reader.onload = function(evt) {
    contents = evt.target.result;
    var json;
    try {
      json = JSON.parse(contents)
    } catch (error) {
      console.log(error)
      json = null;
    }
    callback(json);
  };
  reader.readAsText(file);
};
`)

/*
  Builds a React component from provided information.
*/
module Make = (
  FormInfos: {
    let webAssets: WebAssets.t
    let name: string
    let resultLabel: string
    let formDataPostProcessing: option<Js.Json.t => Js.Json.t>
    let computeAndPrintResult: Js.Json.t => React.element
    let url: string
  },
) => {
  @react.component
  let make = () => {
    let currentPath = Nav.getCurrentURL().path
    let (formData, setFormData) = React.useState(_ => FormInfos.webAssets.initialData)
    let (eventsOpt, setEventsOpt) = React.useState(_ => None)

    React.useEffect2(() => {
      setEventsOpt(_ => {
        let events = {
          try {CatalaFrenchLaw.retrieveEventsSerialized()->CatalaRuntime.deserializedEvents} catch {
          | _ => []
          }
        }
        if 0 == events->Belt.Array.size {
          None
        } else {
          Some(events)
        }
      })
      None
    }, (formData, setEventsOpt))

    let (uploadedFile, setUploadedFile) = React.useState(_ => {
      Js.Json.object_(Js.Dict.empty())
    })

    let fileChangeHandler = (_event: ReactEvent.Form.t) => {
      setUploadedFile(%raw(`_event.target.files[0]`))
    }

    let retrieveFileContents = _ => {
      if %raw(`uploadedFile instanceof File`) {
        readFileAsJSON(uploadedFile, form_data => setFormData(_ => Some(form_data)))
      }
    }

    let form_footer = {
      let priority = "tertiary"
      <Dsfr.ButtonsGroup
        inlineLayoutWhen="always"
        className="text-left"
        buttonsEquisized=true
        buttonsSize="medium"
        alignment="center"
        buttons=[
          {
            children: `Réinitialiser le formulaire`->React.string,
            onClick: _ => {
              Console.debug("Resetting form data")
              setFormData(_ => FormInfos.webAssets.initialData)
            },
            iconId: "fr-icon-refresh-line",
            priority,
          },
          {
            children: `Exporter les données au format JSON`->React.string,
            onClick: _ => {
              let data_str = Js.Json.stringify(formData->Belt.Option.getWithDefault(Js.Json.null))
              downloadJSONstring(data_str)
            },
            iconId: "fr-icon-upload-line",
            priority,
          },
          {
            children: <>
              <input
                className="hidden w-100" id="file-upload" type_="file" onChange={fileChangeHandler}
              />
              <label htmlFor="file-upload" className="cursor-pointer">
                {`Importer les données au format JSON `->React.string}
              </label>
              <p />
            </>,
            onClick: retrieveFileContents,
            iconId: "fr-icon-download-line",
            priority,
          },
          {
            children: {"Code source du programme"->React.string},
            onClick: {_ => currentPath->List.concat(list{`sources`})->Nav.goToPath},
            iconId: "fr-icon-code-s-slash-line",
            priority,
          },
        ]
      />
    }

    let form_result =
      <Dsfr.CallOut>
        {switch formData {
        | None => `En attente de la confirmation du formulaire...`->React.string
        | Some(formData) =>
          try {
            <div className="flex flex-col">
              <div>
                {FormInfos.resultLabel->React.string}
                {": "->React.string}
                {FormInfos.computeAndPrintResult(formData)}
              </div>
              <Dsfr.Button
                onClick={_ => {
                  let doc = CatalaExplain.generate(
                    // NOTE(@EmileRolley): we assume that the events exist,
                    // because we have a result.
                    ~events=eventsOpt->Option.getExn,
                    ~userInputs=formData,
                    ~schema=FormInfos.webAssets.schema,
                    ~opts={
                      title: `Calcul des ${FormInfos.name}`,
                      // Contains an explicatory text about the computation and the catala program etc...
                      description: `Explication du détail des étapes de calcul établissant l'éligibilité et le montant des ${FormInfos.name} pour votre demande`,
                      creator: `catala-dsfr`,
                      keysToIgnore: FormInfos.webAssets.keysToIgnore,
                      selectedOutput: FormInfos.webAssets.selectedOutput,
                      sourcesURL: `${Constants.host}/${FormInfos.url}/sources`,
                    },
                  )

                  doc
                  ->Docx.Packer.toBlob
                  ->Promise.thenResolve(blob => {
                    FileSaver.saveAs(
                      blob,
                      `explication-decision-${FormInfos.name->String.replaceRegExp(
                          %re("/\s/g"),
                          "_",
                        )}.docx`,
                    )
                  })
                  ->ignore
                }}
                iconPosition="left"
                iconId="fr-icon-newspaper-line"
                priority="secondary">
                {`Télécharger une explication du calcul`->React.string}
              </Dsfr.Button>
            </div>
          } catch {
          | err =>
            <>
              <Lang.String english="Computation error: " french={`Erreur de calcul : `} />
              {err
              ->Js.Exn.asJsExn
              ->Belt.Option.map(Js.Exn.message)
              ->Belt.Option.getWithDefault(Some(""))
              ->Belt.Option.getWithDefault("unknwon error, please retry the computation")
              ->React.string}
            </>
          }
        }}
      </Dsfr.CallOut>

    <>
      <div className="fr-container--fluid">
        <div className="fr-grid-row fr-grid-row--gutters fr-grid-row--center">
          <Dsfr.Notice
            title={`Les données collectées par ce formulaire ne sont envoyées nulle part, et sont gérées uniquement par votre navigateur internet. \
            Les données sont traitées localement par un programme Javascript qui a été transmis avec le reste de ce site Internet. \
            Ainsi, ce site ne collecte aucune donnée de ses utilisateurs.`}
            isClosable=true
          />
          <div className="fr-col">
            <React.Suspense fallback={Spinners.loader}>
              <RjsfFormDsfrLazy
                schema={FormInfos.webAssets.schema}
                uiSchema={FormInfos.webAssets.uiSchema}
                formData={formData->Belt.Option.getWithDefault(Js.Json.null)}
                onSubmit={t => {
                  setFormData(_ => {
                    let formData = t->Js.Dict.get("formData")
                    switch (FormInfos.formDataPostProcessing, formData) {
                    | (Some(f), Some(formData)) => {
                        let newFormData = f(formData)
                        Some(newFormData)
                      }
                    | _ => formData
                    }
                  })
                }}
              />
            </React.Suspense>
          </div>
          <div
            className="w-full fr-m-1w border-2 border-solid rounded-full border-[var(--border-default-grey)]"
          />
          <div className="fr-col"> form_result </div>
        </div>
        form_footer
      </div>
    </>
  }
}

```
=========== End file