


Authenticate via steam

Once the user authenticates, we retrieve the user's recently and owned games via steam api

Along with the game information, we want to retrieve information all about the games

Using the recommendation algorithm, we could comparatively rank the similarity of the game information against a database of movies


When scraping, load the tf dictionaries and a df dictionary across the whole collection. we write the dictionaries along with correlated movie titles and metadata to s3.

Lambda function to that is hit with a list of game info per game that we treat as a list of queries that we rank against the movies in s3 and return the top ranked movies

REST API wrapped around the lambda function that can receive the list of songs and trigger the lambda function when it is hit and also return results when the lambda function returns.

