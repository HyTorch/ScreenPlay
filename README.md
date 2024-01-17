# ScreenPlay

ScreenPlay: Matching Movies to Your Gaming Preferences. 
<br> The application will match TV shows and movies to the users’ game playing preferences such as games and board games. Implement an Okapi BM25 TF/IDF weighting for the output of a list of games in comparative ranking.
<br> It’s an important and interesting application because this gives people the opportunity to live through the experience of their favorite scenes and characters in the screens of movies and TV shows.
<br>Planned approach - Build a correlation between the user’s screen preferences and game preferences by comparing the games’ review, genres, and description to the movie’s review, genres, and description respectively.
<br>Tools, systems or datasets involved - It will require using Steam Web API to get access to the largest game library provided by the engine. For Steam Web API calls and usage, I will use the NodeJS Client wrapper for Steam API. It will also require using IMDB API to get access to the largest movie and tv show library. I 
<br>Expected outcome - When users login to their Steam account, the ScreenPlay application has their gaming information to output a list of movies in comparative ranking 
<br>Evaluation - If the list of games are aligned with the suggested movies, it's doing the job correctly. For example, if I play Spider-man games, I would see Spider-man movies as my top results.

A web application implemented with calling both the Steam Web API and IMDB API for data to execute Okapi BM25 TF/IDF weighting on the AWS (or locally) architecture would suffice more than 20 hours of work.

<br> - Identifying the tools, systems and datasets involved. The tools to use are pypi's steam api, the systems require a large dataset to be stored by mining the imdb site, the datasets involved are both using those two tools.
<br> - I've acquired Steam's Web API to access to the largest game library provided by the engine. When the user enters his or her Steam user ID, I am able to retrieve the games they own.
<br> - Created comparative ranking using the BM25 TF/IDF weighing

<br>
<br> - All the source code and main results are available in this github page.
<br> - Source code was documented with the comments.
<br> - I tested using two different Steam accounts, and the expected outcomes were ideal.
<br> A demo that shows your code can actually run and generate the desired results.
<br> - Uploaded video on how the application works - Note: you must be logged in to the mediaspace site
<br> https://mediaspace.illinois.edu/media/t/1_nxpaq4av
