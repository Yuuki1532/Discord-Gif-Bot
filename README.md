# A Discord Bot Based on discord.py

## Main Features
- Manage uploaded GIFs by storing their URLs and tags in a google spreadsheet
    - Actually, other contents are also supported, whatever a google spreadsheet cell can save
- Post the corresponding GIF (content) when queried

## Prerequisites
- A google spreadsheet
    - With its sheet ID
    - A worksheet named `content_db` with columns: [id, uploader, nickname, content, tags, ...]
- A google service account
    - With its json key
- A discord Bot
    - With its token
- Python packages
    - `discord.py`
    - dotenv
    - googleapiclient
    - google.oauth2

## Usage
> The following commands should be called with a prefix `!`

- `help`
    - Show help message
- `echo` <u>CONTENT</u>
    - Echo `CONTENT`, use quotes/double quotes to prevent whitespaces in `CONTENT` being parsed as delimiters
- `add` <u>TAGS ...</u> <u>CONTENT</u>
    - Add `CONTENT` to database with tags `TAGS`
    - At least one `TAGS` should be provided
    - Use quotes/double quotes to prevent whitespaces in `CONTENT` being parsed as delimiters
- `ls` [<u>TAGS ...</u>] [uploader=<u>UPLOADER</u>] [nickname=<u>NICKNAME</u>]
    - List rows in the database with its tags covers `TAGS`, uploader=`UPLOADER`, nickname=`NICKNAME`
    - `UPLOADER` is the user's discord name
    - `NICKNAME` is the user's display name in the channel they added the content
    - All parameters are optional while `ls` without parameter is not provided
- `show` [<u>ID</u>] [<u>TAGS ...</u>]
    - Show the content filtered by TAGS in the database
    - At least one `TAG` or `ID` should be provided
    - When an `ID` is provided, search directly by `ID` instead of `TAGS`
- <u>`TAGS ...`</u>
    - A shortcut command to `show TAGS ...` when none of the commands are matched by the first `TAG` in `TAGS`
