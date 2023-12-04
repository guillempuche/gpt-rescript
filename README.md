# ReScript GPT

Experience ReScript coding like never before with our custom GPT assistant at [ReScript GPT](https://chat.openai.com/g/g-6WNsS1jVM-rescript).

ReScript GPT is a custom GPT assistant designed for generating ReScript code, tailored for both frontend and backend development in ReScript versions 10 and 11. This project leverages the capabilities of [OpenAI's custom GPTs](https://openai.com/blog/introducing-gpts), introduced on November 6, 2023, to provide specialized code generation in the latest ReScript versions.

## Why Custom GPT for ReScript?

The generic GPT-4 showed limitations in coding with ReScript, especially for versions 10 and 11. To address this, we trained a custom model to understand and generate code more accurately in these specific versions.

## Training Material

We used up-to-date ReScript code (versions 10 and 11) sourced from GitHub:

- **Offical Website**: [rescript-lang.org](https://rescript-lang.org/) that has the markdown files on this [repository](https://github.com/rescript-association/rescript-lang.org/).
- **Generic Code**: `path:package.json rescript "11.0"`. Try it [here](https://github.com/search?utf8=%E2%9C%93&q=path%3Apackage.json+rescript+%2211.0%22&type=code).
- **Frontend Code**: `path:package.json rescript "11.0" "rescript/react" tailwind`, `path:rescript.json react`
- **Backend Code**: `path:package.json rescript "11.0" rescript-bun`, `path:rescript.json rescript-bun`

The model is currently trained with files from the `files-v1` directory, each following the `template.md` format.

## Instructions

We prompt GPT this:
```md
You're an expert of ReScript (versions 11 and 10) React and Typescript.

Requirements:
- You always code in Rescript v11
- If you receive Javascript or Typescript code to transform to Rescript, don't make errors on small details.
- If the solution is short, provide two solutions. Else one.
- Just list the Rescript techniques used.
- Always try to use the latest code of the dependencies required. Example: React 18, Next 13
- If you need other  files than `res`, just do it
```

## Resources and References

- [ReScript Compiler Releases](https://github.com/rescript-lang/rescript-compiler/releases) and [Official Blog](https://rescript-lang.org/blog) for new version features.
- Relevant OpenAI Articles:
  - [Introducing Custom GPTs](https://openai.com/blog/introducing-gpts)
  - [New Models and Developer Products Announced at DevDay](https://openai.com/blog/new-models-and-developer-products-announced-at-devday)
