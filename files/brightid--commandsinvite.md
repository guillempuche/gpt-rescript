Rescript v10

Repo: https://github.com/ShenaniganDApp/brightid-discord-bot

=========== Start file package.json (part or full code)
```
{
  "name": "root",
  "private": true,
  "devDependencies": {
    "patch-package": "^6.4.7"
  },
  "dependencies": {
    "@rescript/core": "^0.2.0",
    "brightid_sdk": "^1.0.1",
    "canvas": "^2.9.0",
    "concurrently": "^7.1.0",
    "dotenv": "^8.2.0",
    "find-up": "^6.3.0",
    "rescript": "^10.1.0-rc.5",
    "rescript-discordjs": "^0.3.0",
    "rescript-nodejs": "^14.3.1",
    "uuid": "^8.3.0"
  },
  "scripts": {
    "bot": "yarn workspace @brightidbot/bot",
    "web": "yarn workspace @brightidbot/web",
    "utils": "yarn workspace @brightidbot/utils",
    "scripts": "yarn workspace @brightidbot/scripts",
    "shared": "yarn workspace @brightidbot/shared",
    "re:build": "yarn shared re:build && yarn utils re:build && yarn bot re:build && yarn web re:build && yarn scripts re:build"
  },
  "workspaces": [
    "apps/*",
    "packages/*"
  ]
}

```
=========== End file

=========== Start file Commands_Invite.res
```
open Discord
open Promise
open Exceptions

@module("../updateOrReadGist.mjs")
external updateGist: (string, 'a) => promise<unit> = "updateGist"

let urlRe = %re(
  "/(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})/"
)

let execute = (interaction: Interaction.t) => {
  let guild = interaction->Interaction.getGuild
  let member = interaction->Interaction.getGuildMember
  let isAdmin = member->GuildMember.getPermissions->Permissions.has(Permissions.Flags.administrator)
  let commandOptions = interaction->Interaction.getOptions
  interaction
  ->Interaction.deferReply(~options={"ephemeral": true}, ())
  ->then(_ => {
    switch isAdmin {
    | false =>
      interaction
      ->Interaction.editReply(
        ~options={"content": "Only administrators can change the invite link"},
        (),
      )
      ->ignore
      InviteCommandError("Commands_Invite: User does not have Administrator permissions")->raise
    | true => {
        let inviteLink = commandOptions->CommandInteractionOptionResolver.getString("invite")
        switch inviteLink->Nullable.toOption {
        | None =>
          interaction
          ->Interaction.editReply(
            ~options={"content": "I didn't receive an invite link. (For some unexplained reason)"},
            (),
          )
          ->ignore
          InviteCommandError("Commands_Invite: Invite Link returned null or undefined")->reject
        | Some(inviteLink) =>
          switch urlRe->RegExp.test(inviteLink) {
          | false => {
              interaction
              ->Interaction.editReply(
                ~options={"content": "The invite link is not a valid URL"},
                (),
              )
              ->ignore
              InviteCommandError("Commands_Invite: Invite Link is not a valid URL")->reject
            }

          | true => {
              updateGist(
                guild->Guild.getGuildId,
                {
                  "inviteLink": inviteLink,
                },
              )->ignore

              interaction
              ->Interaction.editReply(
                ~options={
                  "content": `Successfully update server invite link to ${inviteLink}`,
                  "ephemeral": true,
                },
                (),
              )
              ->ignore
              resolve()
            }
          }
        }
      }
    }->catch(e => {
      switch e {
      | InviteCommandError(msg) => Console.error(msg)
      | Exn.Error(obj) =>
        switch Exn.message(obj) {
        | Some(msg) => Console.error(msg)
        | None => Console.error("Must be some non-error value")
        }
      | _ => Console.error("Some unknown error")
      }
      resolve()
    })
  })
}

let data =
  SlashCommandBuilder.make()
  ->SlashCommandBuilder.setName("invite")
  ->SlashCommandBuilder.setDescription("Add an invite link to be displayed for this server")
  ->SlashCommandBuilder.addStringOption(option => {
    open SlashCommandStringOption
    option
    ->setName("invite")
    ->setDescription("Enter an invite link to this server")
    ->setRequired(true)
  })

```
=========== End file