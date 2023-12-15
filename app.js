const express = require('express');
const passport = require('passport');
const session = require('express-session');
const passportSteam = require('passport-steam');
const SteamAPI = require('steamapi');
const ejs = require('ejs');
const fs = require('fs');

const SteamStrategy = passportSteam.Strategy;
const steam = new SteamAPI('F1492F11AA362CBCAF9116D92C7EBE06');

const app = express();
const port = 3000;

// Passport setup
passport.serializeUser((user, done) => done(null, user));
passport.deserializeUser((user, done) => done(null, user));

passport.use(new SteamStrategy({
    returnURL: `http://localhost:${port}/api/auth/steam/return`,
    realm: `http://localhost:${port}/`,
    apiKey: 'F1492F11AA362CBCAF9116D92C7EBE06'
}, (identifier, profile, done) => {
    process.nextTick(() => {
        profile.identifier = identifier;
        return done(null, profile);
    });
}));

// Express setup
app.use(session({
    secret: 'Whatever_You_Want',
    saveUninitialized: true,
    resave: false,
    cookie: {
        maxAge: 3600000
    }
}));

app.use(passport.initialize());
app.use(passport.session());

app.set('view engine', 'ejs');

// Store user information, including recent and owned games
const userData = {};

// Routes
app.get('/api/auth/steam', passport.authenticate('steam', { failureRedirect: '/' }), (req, res) => {
    res.redirect('/');
});

app.get('/api/auth/steam/return', passport.authenticate('steam', { failureRedirect: '/' }), (req, res) => {
    // Retrieve user information
    const user = req.user;
    const steamId = user._json.steamid;

    // Store user data locally
    userData[steamId] = {
        user,
        recentGames: [],
        ownedGames: []
    };

    // Redirect to the home page
    res.redirect('/');
});

// Start the server
app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});

// Function to fetch game details by ID
async function fetchGameDetails(gameId) {
    try {
        const gameDetails = await steam.getGameDetails(gameId);
        return gameDetails;
    } catch (error) {
        console.error(`Error fetching game details for ID ${gameId}:`, error);
        return null;
    }
}



app.get('/', async (req, res) => {
    try {
        const user = req.user;
        const steamId = user._json.steamid;

        // Retrieve recent games and owned games
        const recentGames = await steam.getUserRecentGames(steamId);
        const ownedGames = await steam.getUserOwnedGames(steamId);

        // Update user data with recent and owned games
        userData[steamId].recentGames = recentGames;
        userData[steamId].ownedGames = ownedGames;

        // Fetch game details for recent games
        const recentGameDetailsPromises = recentGames.map(game => fetchGameDetails(game.appID));
        const recentGameDetails = await Promise.all(recentGameDetailsPromises);

        // Fetch game details for owned games
        const ownedGameDetailsPromises = ownedGames.map(game => fetchGameDetails(game.appID));
        const ownedGameDetails = await Promise.all(ownedGameDetailsPromises);

        // Create an object to store game descriptions
        const gameDescriptions = {};
        const gameData = []
        temp = {}

        // Populate game descriptions for recent games
        recentGames.forEach((game, index) => {
            gameDescriptions[game.appID] = recentGameDetails[index];
        });

        ownedGames.forEach((game, index) => {
            gameDescriptions[game.appID] = ownedGameDetails[index];
        });

        Object.values(gameDescriptions).forEach((gameDetails, index) => {
            // const gameDetails = recentGameDetails[index];
            const description = prepare_game_description(gameDetails);
            gameData.push(description);
        });

        const movieWordsPath = './movieWords.json'; // total count of each words of each movie scripts
        const titleListPath = './titleList.json'; // total amount of words of each movie's scripts
        const metaListPath = './metaList.json'; // just meta data
        const dfDictPath = './dfDict.json'; // total count of words of all movie scripts

        // Load JSON files
        const movieList = loadJsonFile(movieWordsPath);
        const titleList = loadJsonFile(titleListPath);
        const metaList = loadJsonFile(metaListPath);
        const dfDict = loadJsonFile(dfDictPath);

        const movieScores = calculateMovieScore(gameData, movieList, titleList, metaList, dfDict);
        // console.log(movieScores);
        // console.log(recentGames)

        // Render a template or send the data as JSON
        // console.log('Game Descriptions:', gameDescriptions);
        // console.log("descriptions::", gameData)
        res.render('index', { user, recentGames, ownedGames, gameDescriptions, movieScores });
    } catch (error) {
        res.render('login');
        // console.error('Error retrieving game data:', error);
        // res.status(500).send('Internal Server Error');
    }
});

function prepare_game_description(gameDetails) {
    if (!gameDetails) {
        return null; // or handle the case where game details are not available
    }

    const gameDescription = {};
    const words = gameDetails.short_description.toLowerCase().split(/\s+/);
    // gameDetails.nam

    words.forEach(word => {
        // Remove punctuation from each word
        word = word.replace(/[.,'!]/g, '');

        if (!(word in gameDescription)) {
            gameDescription[word] = 0;
        }
        gameDescription[word]++;
    });

    return { wordFrequency: gameDescription, totalWords: words.length };
}

// Computes a similarity score based on tf-idf between a game and a movie
function tfidfSimilarity(game, movie, dfDict, totalGameWords, totalMovieWords, totalMovies) {
    let similarityScore = 0;

    for (const key in game) {
        if (key in movie) {
            const gameDesc = game[key] / totalGameWords;
            const movieSummary = movie[key] / totalMovieWords;
            const logVal = (totalMovies + 1) / dfDict[key];
            similarityScore += gameDesc * movieSummary * Math.log(logVal);
        }
    }

    return similarityScore;
}

// Function to load JSON file
function loadJsonFile(filePath) {
    try {
        const fileContent = fs.readFileSync(filePath, 'utf8');
        return JSON.parse(fileContent);
    } catch (error) {
        console.error(`Error reading file ${filePath}:`, error);
        throw new Error('An error occurred while reading the file.');
    }
}

// Computes the top 10 movie matches for a given game list
function calculateMovieScore(gameList, movieList, titleList, metaList, dfDict) {
    const movieScores = [];
    const totalMovies = movieList.length;

    for (let idx = 0; idx < movieList.length; idx++) {
        let acc = 0;
        const movieDict = movieList[idx];

        for (const gameDictEntry of gameList) {
            if (gameDictEntry) {
                const totalGameWords = gameDictEntry.totalWords;
                const gameDict = gameDictEntry.wordFrequency;
                acc += tfidfSimilarity(gameDict, movieDict, dfDict, titleList[idx][1], totalGameWords, totalMovies);
            }

        }

        const meta = metaList[idx];
        movieScores.push([acc, meta[2], titleList[idx][0], meta[3], meta[1], meta[0]]);
    }

    movieScores.sort();

    return movieScores.slice(-25).reverse().map(x => x.slice(1));
}

