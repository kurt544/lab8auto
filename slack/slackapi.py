from slack_sdk.webhook import WebhookClient
url = "https://hooks.slack.com/services/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"
webhook = WebhookClient(url)

response = WebhookClient(url)

response = webhook.send(text="Hello")
assert response.status_code == 200
assert response.body == "ok"
