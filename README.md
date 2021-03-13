# MinecraftBot
Бот-саппорт для оповещения в телеграмме


# Install

To install all dependencies use command
```
make install-deps
```


For tests
```
make run-tests
```

Linters
```
make run-linter
```

# Usage

Make sure that all environment variables is set right, you have to set following
 variables:
```
export DATABASE_URL='Your postgresql database url'
export TELEGRAM_TOKEN='telegram token accuired from botfather'
export XBOX_CLIENT_ID='xbox client id from azure'
export XBOX_CLIENT_SECRET='xbox sercret from your application'
export XBOX_TOKEN='bearer token for your xbox app'
```

To start bot use following command
```
make start-bot
```


There is also cron task for tracking who is online right now
```
make start-cron-session
```
