# Datalabel
____

motive: to build a datalabel application that allows to introduce more information to data we have accumulated ie production data that requires SME to catagorize before model training

## get things up

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

## backlog

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
- **clean up all directories**

## challenges

- ensure row locking (not true locking yet)
	- sqlite have no row locking feature, oracle db has but not sure how it works precisely, ie lock id passing / identifying who has the right to edit the locked row
	- current approach relies on user refresh to see which row is locked, the more the users its more likely to have multiple users in same item; also with the list of images increases users need to scroll to reach bottom
	- previous approach is to hide all operation and expose getNextItem to users, was rejected due to there is no way we can update the lock and select the locked item correctly (time -10 sec may work but not robust), actually there maybe a workaround by adding a modify datetime string column, with it we store dt.datetime.now() to a variable, using it to update the table and query that row with modified date filter
	- some tools in github provides a different approach (or at least give me the idea) by having source dir, staging dir and dest dir. the labeling process relies by moving image to staging one by one, thus achieve locking. however might not be as straight forward as moving files take time especially huge images.
- related to challenge 1, how do we prevent all searches from require constantly checking if the table is updated