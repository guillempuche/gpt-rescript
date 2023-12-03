# ReScript GPT

Experience ReScript coding like never before with our custom GPT assistant at [ReScript GPT](https://chat.openai.com/g/g-6WNsS1jVM-rescript).

ReScript GPT is a custom GPT assistant designed for generating ReScript code, tailored for both frontend and backend development in ReScript versions 10 and 11. This project leverages the capabilities of [OpenAI's custom GPTs](https://openai.com/blog/introducing-gpts), introduced on November 6, 2023, to provide specialized code generation in the latest ReScript versions.

## Why Custom GPT for ReScript?

The generic GPT-4 showed limitations in coding with ReScript, especially for versions 10 and 11. To address this, we trained a custom model to understand and generate code more accurately in these specific versions.

## Training Material

We used up-to-date ReScript code (versions 10 and 11) sourced from GitHub:

- **Generic Code**: `path:package.json rescript "11.0"`
- **Frontend Code**: `path:package.json rescript "11.0" "rescript/react" tailwind`, `path:rescript.json react`
- **Backend Code**: `path:package.json rescript "11.0" rescript-bun`, `path:rescript.json rescript-bun`

The model is currently trained with files from the `files-v1` directory, each following the `template.md` format.

## Resources and References

- [ReScript Compiler Releases](https://github.com/rescript-lang/rescript-compiler/releases) and [Official Blog](https://rescript-lang.org/blog) for new version features.
- Relevant OpenAI Articles:
  - [Introducing Custom GPTs](https://openai.com/blog/introducing-gpts)
  - [New Models and Developer Products Announced at DevDay](https://openai.com/blog/new-models-and-developer-products-announced-at-devday)