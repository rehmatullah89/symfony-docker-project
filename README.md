# Unifonic PHP Assignment

Original Repo: https://github.com/dunglas/symfony-docker

A [Docker](https://www.docker.com/)-based installer and runtime for the [Symfony](https://symfony.com) web framework,
with [FrankenPHP](https://frankenphp.dev) and [Caddy](https://caddyserver.com/) inside!

## Getting Started

1. If not already done, [install Docker Compose](https://docs.docker.com/compose/install/) (v2.10+)
2. Run `make build` or `docker compose build --no-cache && docker compose -f docker-compose.smsapi.yml build --no-cache` to build fresh images
3. Run `make start` or `docker compose up --pull -d --wait && docker compose -f docker-compose.smsapi.yml up --pull -d --wait` to start the project
4. Open `https://localhost` in your favorite web browser and [accept the auto-generated TLS certificate](https://stackoverflow.com/a/15076602/1352334)
5. Run `make stop` or `docker compose down --remove-orphans && docker compose -f docker-compose.smsapi.yml down --remove-orphans` to stop the Docker containers.


## Objective
Imagine you are building a system that will allow a user to send SMS campaigns to a list of contacts. The user should be able to create a campaign, upload a list of contacts, and send the campaign to the list of contacts.


## Instructions & Requirements
1. Please don't spend more than 2 hours on this exercise.
1. Upon completion of the exercise, please send us a link to a repository or a ZIP file of this project.
1. A sample file of contacts can be found in the root of this project (`./data/contacts.csv`).
1. There should be a way to retrieve historical campaigns with their contacts.
1. Ensure that there are no pending PHPStan issues (run `vendor/bin/phpstan`).
1. And most importantly, we don't want you to actually send any SMS 😅.
    - Instead, this project ships with a mock SMS API service, which runs on localhost, port "8585". It provides two endpoints: "/send" and "/bulk" (both accept only JSON).
    - "/send": Takes a `message` and a `phone_number` field.
    - "/bulk": Takes a `campaign_id`, a `message` and a collection of `recipients` (max. 1000 per request), where each entry has a `phone_number` field.
    - [See more details below](#mock-service-details)

#### HINT: Also think about how to handle potential duplicate values - within the same list of contacts for a campaign, but also across different campaigns.


#### Mock Service Details:
POST to `/send`
```
POST http://localhost:8585/send
{
    "message": "Test Single Message",
    "phone_number": "+971123456789"
}
```
\
POST to `/bulk`
```
POST http://localhost:8585/bulk
{
    "campaign_id": "50a179a2-1b97-40ad-861c-1b7f05834150",
    "message": "Test Bulk Message",
    "recipients": [
        {
            "phone_number": "+971123456789"
        },
        {
            "phone_number": "+971123456789"
        },
        {
            "phone_number": "+971123456789"
        } 
    ]
}
```



## Questions?
Feel free to reach out to [Sven Schneemann](mailto:sschneemann@unifonic.com)

