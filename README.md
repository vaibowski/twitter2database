# HackerCamp2018Submission-API
Twitter streaming API to fetch tweets in realtime, store them in mongoDB and export to csv

1. Call function fetch_data() with 2 parameters. The keywords queries and the max tweet to store in database.
2. Search function helps to filter tweets saved in mongoDB with filters: name, retweet count, favourites count.
3. The filtered tweets are stored in a csv file with fields: Name, Retweet Count, Favourites count, Time Created at.
