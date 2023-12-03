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

=========== Start file Services_Sponsor.res
```
open Discord
open NodeFetch

let {brightIdVerificationEndpoint, brightIdAppDeeplink, brightIdLinkVerificationEndpoint} = module(
  Endpoints
)

let {makeCanvasFromUri, createMessageAttachmentFromCanvas, makeBeforeSponsorActionRow} = module(
  Commands_Verify
)

@val @scope("globalThis")
external fetch: (string, 'params) => promise<Response.t<JSON.t>> = "fetch"

let sleep: int => promise<unit> = _ms => %raw(` new Promise((resolve) => setTimeout(resolve, _ms))`)

Env.createEnv()

let envConfig = switch Env.getConfig() {
| Ok(config) => config
| Error(err) => err->Env.EnvError->raise
}

exception RetryAsync(string)
let rec retry = async (fn, n) => {
  try {
    let _ = await sleep(1000)
    await fn()
  } catch {
  | _ =>
    if n > 0 {
      await retry(fn, n - 1)
    }
  }
  RetryAsync(j`Failed $fn retrying $n times`)->raise
}

let noUnusedSponsorshipsOptions = () =>
  {
    "content": "There are no sponsorhips available in the Discord pool. Please try again later.",
    "ephemeral": true,
  }

let unsuccessfulSponsorMessageOptions = async uuid => {
  let verifyUrl = `${brightIdLinkVerificationEndpoint}/${uuid}`
  let row = makeBeforeSponsorActionRow("Retry Sponsor", verifyUrl)
  {
    "content": "Your sponsor request failed. \n\n This is often due to the BrightID App not being linked to Discord. Please scan the previous QR code in the BrightID mobile app then retry your sponsorship request.\n\n",
    "ephemeral": true,
    "components": [row],
  }
}
let sponsorRequestSubmittedMessageOptions = async () => {
  let nowInSeconds = Math.round(Date.now() /. 1000.)
  let fifteenMinutesAfter = 15. *. 60. +. nowInSeconds
  let content = `You sponsor request has been submitted! \n\n Make sure you have scanned this QR code in the BrightID mobile app to confirm your sponsor and link Discord to BrightID. \n This process will timeout <t:${fifteenMinutesAfter->Float.toString}:R>.\n\n`
  {
    "content": content,
    "ephemeral": true,
  }
}

let makeAfterSponsorActionRow = label => {
  let verifyButton =
    MessageButton.make()
    ->MessageButton.setCustomId("verify")
    ->MessageButton.setLabel(label)
    ->MessageButton.setStyle("PRIMARY")

  MessageActionRow.make()->MessageActionRow.addComponents([verifyButton])
}

let successfulSponsorMessageOptions = async uuid => {
  let uri = `${brightIdAppDeeplink}/${uuid}`
  let canvas = await makeCanvasFromUri(uri)
  let attachment = await createMessageAttachmentFromCanvas(canvas)
  let row = makeAfterSponsorActionRow("Assign BrightID Verified Role")
  {
    "content": "You have succesfully been sponsored \n\n If you are verified in BrightID you are all done. Click the button below to assign your role.\n\n",
    "files": [attachment],
    "ephemeral": true,
    "components": [row],
  }
}

exception HandleSponsorError(string)
type sponsor = SponsorSuccess(Shared.BrightId.Sponsorships.sponsor)
type handleSponsor =
  | SponsorshipUsed
  | RetriedCommandDuring
  | NoUnusedSponsorships
  | TimedOut

type sponsorship = Sponsorship(Shared.BrightId.Sponsorships.t)
let checkSponsor = async uuid => {
  open Shared.Decode
  let endpoint = `https://app.brightid.org/node/v5/sponsorships/${uuid}`
  let params = {
    "method": "GET",
    "headers": {
      "Accept": "application/json",
      "Content-Type": "application/json",
    },
    "timeout": 60000,
  }
  let res = await fetch(endpoint, params)
  let json = await Response.json(res)

  switch (
    json->Json.decode(Decode_BrightId.Sponsorships.data),
    json->Json.decode(Decode_BrightId.Error.data),
  ) {
  | (Ok({data}), _) => Sponsorship(data)
  | (_, Ok(error)) => error->Exceptions.BrightIdError->raise
  | (Error(err), _) => err->Json.Decode.DecodeError->raise
  }
}

@raises([HandleSponsorError, Exn.Error, Json.Decode.DecodeError])
let rec handleSponsor = async (
  ~maybeHash=None,
  ~maybeLogMessage=None,
  interaction,
  uuid,
  endTimeInSeconds,
) => {
  open Shared.BrightId
  open Shared.Decode

  let guildId = interaction->Interaction.getGuild->Guild.getGuildId
  let secondsBetweenAttempts = 15 //Probably won't need this if whe are using our own node
  // 10 second buffer for Webhook expiry
  let hasWebhookExpired = endTimeInSeconds - Helpers.nowInSeconds() < 10
  switch hasWebhookExpired {
  | true =>
    if maybeLogMessage->Option.isSome {
      let _ = await CustomMessages.editSponsorshipMessage(
        maybeLogMessage->Option.getExn,
        interaction,
        CustomMessages.Status.Failed,
        uuid,
        maybeHash,
      )
    }
    TimedOut
  | _ =>
    try {
      let json = await sponsor(
        ~key=envConfig["sponsorshipKey"],
        ~context="Discord",
        ~contextId=uuid,
      )
      switch json->Json.decode(Decode_BrightId.Sponsorships.sponsor) {
      | Ok({hash}) =>
        let options = await sponsorRequestSubmittedMessageOptions()
        let _ = await Interaction.editReply(interaction, ~options, ())
        Console.log2(
          `A sponsor request has been submitted`,
          {"guild": guildId, "contextId": uuid, "hash": hash},
        )
        let maybeLogMessage = await CustomMessages.sponsorshipRequested(
          interaction,
          uuid,
          Some(hash),
        )
        await handleSponsor(
          interaction,
          uuid,
          ~maybeHash=Some(hash),
          ~maybeLogMessage,
          endTimeInSeconds,
        )
      | Error(err) => Json.Decode.DecodeError(err)->raise
      }
    } catch {
    | Exn.Error(error) =>
      try {
        let brightIdError =
          JSON.stringifyAny(error)
          ->Option.map(JSON.parseExn)
          ->Option.map(Json.decode(_, Decode_BrightId.Error.data))

        switch brightIdError {
        | None =>
          HandleSponsorError(
            "Handle Sponsor Error: There was a problem JSON parsing the error from sponsor()",
          )->raise
        | Some(Error(err)) => err->Json.Decode.DecodeError->raise
        | Some(Ok({errorNum})) =>
          switch (errorNum, maybeHash) {
          //No Sponsorships in the Discord App
          | (38, _) =>
            if maybeLogMessage->Option.isSome {
              let _ = await CustomMessages.editSponsorshipMessage(
                maybeLogMessage->Option.getExn,
                interaction,
                CustomMessages.Status.Error(
                  "No Sponsorships available in the BrightID Discord App",
                ),
                uuid,
                maybeHash,
              )
            }
            NoUnusedSponsorships
          //Sponsorship already assigned
          | (_, None) => RetriedCommandDuring
          | (39, Some(hash)) =>
            let Sponsorship({spendRequested, appHasAuthorized}) = await checkSponsor(uuid)
            if spendRequested && appHasAuthorized {
              if maybeLogMessage->Option.isSome {
                let _ =
                  maybeLogMessage->Option.map(async logMessage =>
                    await CustomMessages.editSponsorshipMessage(
                      logMessage,
                      interaction,
                      CustomMessages.Status.Successful,
                      uuid,
                      Some(hash),
                    )
                  )
              }
              let options = successfulSponsorMessageOptions(uuid)
              let _ = await Interaction.editReply(interaction, ~options, ())
              SponsorshipUsed
            } else {
              let _ = await sleep(secondsBetweenAttempts * 1000)
              await handleSponsor(~maybeHash, ~maybeLogMessage, interaction, uuid, endTimeInSeconds)
            }
          //App authorized before
          | (45, Some(hash)) =>
            let Sponsorship({spendRequested, appHasAuthorized}) = await checkSponsor(uuid)
            if spendRequested && appHasAuthorized {
              if maybeLogMessage->Option.isSome {
                let _ = await CustomMessages.editSponsorshipMessage(
                  maybeLogMessage->Option.getExn,
                  interaction,
                  CustomMessages.Status.Successful,
                  uuid,
                  Some(hash),
                )
              }
              let options = successfulSponsorMessageOptions(uuid)
              let _ = {await Interaction.editReply(interaction, ~options, ())}
              SponsorshipUsed
            } else {
              let _ = await sleep(secondsBetweenAttempts * 1000)
              await handleSponsor(~maybeHash, ~maybeLogMessage, interaction, uuid, endTimeInSeconds)
            }

          // Spend Request Submitted
          | (46, Some(hash)) =>
            let Sponsorship({spendRequested, appHasAuthorized}) = await checkSponsor(uuid)
            if spendRequested && appHasAuthorized {
              if maybeLogMessage->Option.isSome {
                let _ = await CustomMessages.editSponsorshipMessage(
                  maybeLogMessage->Option.getExn,
                  interaction,
                  CustomMessages.Status.Successful,
                  uuid,
                  Some(hash),
                )
              }
              let options = await successfulSponsorMessageOptions(uuid)
              let _ = await interaction->Interaction.editReply(~options, ())
              SponsorshipUsed
            } else {
              let _ = await sleep(secondsBetweenAttempts * 1000)
              await handleSponsor(~maybeHash, ~maybeLogMessage, interaction, uuid, endTimeInSeconds)
            }

          // Sponsored Request Recently
          | (47, Some(_)) =>
            let Sponsorship({spendRequested, appHasAuthorized}) = await checkSponsor(uuid)
            if spendRequested && appHasAuthorized {
              if maybeLogMessage->Option.isSome {
                let _ = await CustomMessages.editSponsorshipMessage(
                  maybeLogMessage->Option.getExn,
                  interaction,
                  CustomMessages.Status.Successful,
                  uuid,
                  maybeHash,
                )
              }
              let options = successfulSponsorMessageOptions(uuid)
              let _ = await Interaction.editReply(interaction, ~options, ())
              SponsorshipUsed
            } else {
              let _ = await sleep(secondsBetweenAttempts * 1000)
              await handleSponsor(~maybeHash, ~maybeLogMessage, interaction, uuid, endTimeInSeconds)
            }

          | _ =>
            let _ = await sleep(secondsBetweenAttempts * 1000)
            await handleSponsor(~maybeHash, ~maybeLogMessage, interaction, uuid, endTimeInSeconds)
          }
        }
      } catch {
      | Exceptions.BrightIdError(_) =>
        let _ = await sleep(secondsBetweenAttempts * 1000)
        await handleSponsor(interaction, uuid, ~maybeHash, ~maybeLogMessage, endTimeInSeconds)
      | Json.Decode.DecodeError(msg) =>
        if msg->String.includes("503 Service Temporarily Unavailable") {
          let _ = await sleep(secondsBetweenAttempts * 1000)
          await handleSponsor(~maybeHash, ~maybeLogMessage, interaction, uuid, endTimeInSeconds)
        } else {
          HandleSponsorError(msg)->raise
        }
      | Exn.Error(obj) =>
        switch Exn.name(obj) {
        | Some("FetchError") =>
          let _ = await sleep(3000)
          await handleSponsor(~maybeHash, ~maybeLogMessage, interaction, uuid, endTimeInSeconds)
        | _ =>
          switch Exn.message(obj) {
          | Some(msg) =>
            if maybeLogMessage->Option.isSome {
              let _ = await CustomMessages.editSponsorshipMessage(
                maybeLogMessage->Option.getExn,
                interaction,
                CustomMessages.Status.Error(msg),
                uuid,
                maybeHash,
              )
            }
            HandleSponsorError(msg)->raise
          | None =>
            Console.error(obj)
            if maybeLogMessage->Option.isSome {
              let _ = await CustomMessages.editSponsorshipMessage(
                maybeLogMessage->Option.getExn,
                interaction,
                CustomMessages.Status.Error("Something went wrong"),
                uuid,
                maybeHash,
              )
            }
            HandleSponsorError("Handle Sponsor: Unknown Error")->raise
          }
        }
      }
    }
  }
}

```
=========== End file