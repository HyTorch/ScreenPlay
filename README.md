# ScreenPlay
Matching Games to Your Viewing Preferences

1. Name, NetID, Captain - Chris Park(Captain and sole member of Crescent Orange Team) - hpark102

2. Free topic - ScreenPlay: Matching Movies to Your Gaming Preferences. 
<br> Task(s) - The application will match TV shows and movies to the users’ game playing preferences such as games and board games. Implement an Okapi BM25 TF/IDF weighting for the output of a list of games in comparative ranking.
<br>Importance and Interest - It’s an important and interesting application because this gives people the opportunity to live through the experience of their favorite scenes and characters in the screens of movies and TV shows.
<br>Planned approach - Build a correlation between the user’s screen preferences and game preferences by comparing the games’ review, genres, and description to the movie’s review, genres, and description respectively.
<br>Tools, systems or datasets involved - It will require using Steam Web API to get access to the largest game library provided by the engine. For Steam Web API calls and usage, I will use the NodeJS Client wrapper for Steam API. It will also require using IMDB API to get access to the largest movie and tv show library. I 
<br>Expected outcome - When users login to their Steam account, the ScreenPlay application has their gaming information to output a list of movies in comparative ranking 
<br>Evaluation - If the list of games are aligned with the suggested movies, it's doing the job correctly. For example, if I play Spider-man games, I would see Spider-man movies as my top results.

3. Programming language - I'll be primarily using Javascript, CSS, HTML, and Python.

4. At least 20*N hours justification - The time it takes to implement a web application that can call both the Steam Web API and IMDB API for data to execute Okapi BM25 TF/IDF weighting on the AWS (or locally) architecture would suffice more than 20 hours of work.


# Progress Report
Please upload your progress report to the Github repo shared on CMT. The progress report should give us an idea of how you're implementing your proposal. It should answer 3 main questions: 1) Which tasks have been completed? 2) Which tasks are pending? 3) Are you facing any challenges? 

1) Complete tasks include
<br> - Identifying the tools, systems and datasets involved. The tools to use are pypi's steam api, the systems require a large dataset to be stored by mining the imdb site, the datasets involved are both using those two tools.
<br> - I've acquired Steam's Web API to access to the largest game library provided by the engine. When the user enters his or her Steam user ID, I am able to retrieve the games they own.
<br> - Created comparative ranking using the BM25 TF/IDF weighing
2) Which tasks are pending
<br> - I want to be able to have a simple web page where users can interact with it by inputting their ID. Currently it's only running on hard coded Steam ID
<br> - I need to test out some more samples to see if the comparative ranking is sufficient
3) Are you facing any challenges
<br> - I am spending more time on trying to set up the web page
<br> - Which includes, outputting a ranked list of recommended movies
<br> - and improve the site to allow users without the need to download depending libraries.

# Final Report
At the final stage of your project, you need to deliver the following:
1) Your documented source code and main results.
<br> - All the source code and main results are available in this github page.
<br> - Source code was documented with the comments.
3) Self-evaluation. Have you completed what you have planned? Have you got the expected outcome? If not, discuss why.
<br> - I have completed most of what I had planned. Although I haven't completed all the aspects of the webpage's architecture, I have achieved the expected outcome.
<br> - I have wanted to make the site accessible through a domain hosted on AWS once I have successfully made the webpage work. Implementing the required tasks to make a functioning site, a webscraper for movie imsdb site, an Okapi BM25 TF/IDF weighting for the output of a list of movies in comparative ranking, Steam API usage for logins and game information, and the express ejs webpage already took over 20 hours.
<br> - I could not proceed to transfer the architecture onto AWS as I had to document, test, and record the results.
<br> - I believe the concept and idea of suggesting movies based on the games users play is a novelty. Also, game descriptions and game titles are better data to suggest movies than what the previous SpotFlix project has implemented in their applicaions. Frankly, comparing between screen entertainment such as gaming and movies would suggest better rankings over the other project's comparison between song lyrics and movies.
5) A demo that shows your code can actually run and generate the desired results.
<br> - Uploaded video on how the application works - Note: you must be logged in to the mediaspace site
<br> 
