# Monitoring Instagram
*Jan 2020*

### How it works

The plugin monitors your Instagram feed automatically. Using this information, we will be able to tell if the algorithms that decide what users see give priority to certain type of content and if they censor other types of content.

The results of the investigation will be published by [AlgorithmWatch](https://algorithmwatch.org/) and their media partners.

### Privacy

The plugin only records data about some of the accounts you follow and the date and time at which content from certain accounts appear in your newsfeed. Your user name is pseudonymized using a one-way cryptographic hash function, so that it is impossible to identify you.

The data will only ever be used for the journalistic investigation "Monitoring Instagram" and will never be sold or shared with any third-parties.

## How to install and run

### The backend

**Required**

* pipenv
* docker & docker-compose (in order to run postgres database)

**Instructions**

1. `make installbackend`
1. `make migrate`
1. `make createsuperuser`
1. `make runbackend`

**Schedulers (hourly)**

`$ python manage.py gvision`
`$ python manage.py ig_scraper`

### The web extension

**Required**

* yarn

**Instructions**

1. `make installwebext`
1. `make runwebext`


## How to prepare a web-ext release

1. Bump the version up in [web-ext/extension/manifest.json](web-ext/extension/manifest.json)
1. `make build_webext`
1. Submit a new version on [addons.mozilla.org](https://addons.mozilla.org/en-US/developers/addon/e838268c69974a4295f9/versions/submit/) in order to auto signed it
1. Wait for approval and download the .xpi file
1. Copy the .xpi file to [backend/static/web-ext-releases](backend/static/web-ext-releases)
1. Deploy the backend

The new version is now published and will be upgraded by browsers in the next 24h.
