- life scienes + supply chain
- can you deliver rapidly
- how do you think about scaling that


# Prompt email

Hey Tim, 

Please see attached exercise. There are two API calls required as part of the exercise. The creds needed for the API calls are below.
POST https://apis.fedex.com/track/v1/trackingnumbers | Oauth2 - use client_id and secret to generate a Bearer token
client_id: l7d63c7891050f4a5782aee9775f916f53
client_secret: 3a7adcf8253545d887571456559b49b7
token_url: https://apis.fedex.com/oauth/token
If you get hung up with the OAuth2, send me an email and I'll send a Bearer token that is good for 1 hour. 
GET https://oainsightapi.onasset.com/rest/2/sentry500s/864499064808214/reports?from=2025-01-08T15:46:00Z&to=2025-01-10T22:46:00Z | Bearer Token
Bearer imc9tvgvmtShp-tPYqoHYhhseMWi_TNNTn1etxJ2WIGxn2GHSN51UUTjyz4pm0vnjnZp95-xSPJ2GBN6ccN1bACUipKpLs7wb3bYyxqXU1BtgTFBT1B-nCa3eNsVDvmva97PBi69s95lrxb-teffh4FKoMGlky3ehTL3iFtiJwZVnZWXEBgZG1MlWPCxjfKtqS7l4ab-mfbdJ5Cda6eO20SGV7e6-WxrjWlRdnuqlwmuvK74fCWyXHRTOBLNwXVVgGCd3GH9ZsevEskKMP-_hvMDqE_wVpUzBEOYO7dY5thCzf49kk-h2g8Hf3Kkn9V-VapcLBxh6oBLInQh9pflRKn2W56pZBwQ_yhegrIeNnc9fg7m7RaAXSFYZiHFCiCFDieisz4-XW9qctaC88C2mw
For security purposes, these creds will work during the exercise, but will no longer work afterward. I've attached a postman collection for these two calls for reference - the Postman collection isn't required for completing the exercise, but may help get the calls working.

I'll keep an eye on my email for any questions, and I'll jump on the google meet at 3PM central time to debrief. If you're done early, let me know! Please confirm receipt.

Thank you,
Rob
