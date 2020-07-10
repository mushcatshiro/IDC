# Datalabel

motive: to build a datalabel application that allows to introduce more information to data we have accumulated ie production data that requires SME to catagorize before model training

# get things up

- to get redis up, not fully supporting windows

```bash
	# to download 
	$ wget http://download.redis.io/releases/redis-6.0.3.tar.gz
	$ tar xzf redis-6.0.3.tar.gz
	$ cd redis-6.0.3
	$ make

	# to start
	$ src/redis-server
```

- to get celery up

celery django and celery flask should have some minor setup difference, please refer to full documentation

```bash
	# to start
	$ celery -A projectFolderName worker -l info
```

# backlog

- adding celery and redis -> done
- ensure no two user is editing same entry/ collision -> pending test
	- add new column is editing
	- if upon query change to True
	- upon update change to False
- ~~complete getNextItem~~
- generate full table of project
	- categorize button call api to check if its locked
- ~~add flash messages~~ dont find it particularly useful
- sort task -> pending test
	- lock until all entries has a category
- error handling
- tasks status tracking and handling
- build internal API for better organization
