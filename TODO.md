# To-Do

## API

The API is where the client will make requests.

Everything (except `/auth/register` and `/auth/login`)
requires `master_key`

- [ ] /auth
    - [x] /register
    - [x] /login
    - [ ] /password (change password)

- [ ] /users
    - [ ] /update

- [ ] /users/<user_id>
    - [ ] /info

---

- [ ] /guilds
    - [x] /create
    - [ ] /update

- [ ] /guilds/<guild_id>/roles
    - [ ] /create

- [ ] /guilds/<guild_id>/channels
    - [ ] /create

- [ ] /guilds/<guild_id>/channels/<channel_id>/messages/
    - [ ] /send
    - [ ] /info/<message_id>
    - [ ] /edit/<message_id>

---

- [ ] /groups
    - [ ] /create
    - [ ] /update

- [ ] /groups/<group_id>/messages/
    - [ ] /send
    - [ ] /info/<message_id>
    - [ ] /edit/<message_id>

---

- [ ] /attachments
    - [ ] /upload
