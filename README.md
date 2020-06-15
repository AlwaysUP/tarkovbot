# Tarkov Kill count bot

###### Brought to you by: small pp (pain problems) production

### Setting Up
Note:This is meant to run on heroku, please modify code accordingly to run it locally or somewhere else

1. `heroku create --stack=container --manifest tarkovbot`
2. `heroku addons:create heroku-postgresql:hobby-dev --app tarkovbot`
3. update the token in `constants.py` with your discord client token
5. `git remote set-url heroku https://git.heroku.com/tarkovbot.git` if fails please run `git remote add heroku https://git.heroku.com/tarkovbot.git`
6. `git commit -a -m "update discord token"`
7. `git push heroku master`

### Clean Up
`heroku destroy tarkovbot`
