# Discord Stocks Webhook

A python script to report stocks values into a discord webhook.

## Usage

To install dependencies run,

```bash
pip install -r requirements.txt
```

You would need then to copy the ID and the TOKEN from the webhook url in the
`.env` file. It should look something like this. The ID is the first value
in the url and the token the last.

```
WEBHOOK_ID="<ID>"
WEBHOOK_TOKEN="<TOKEN>"
```

Then add the script into the crontab using `crontab -e`. In the example, the
script runs once a day at 4pm.

```bash
0 16 * * 1-5 /path/to/stocks_webhook.py TSLA
2 16 * * 1-5 /path/to/stocks_webhook.py AMD
5 16 * * 1-5 /path/to/stocks_webhook.py BABA
```
