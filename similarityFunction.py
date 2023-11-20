import math

# Computes a similarity score based on tf-idf between a game and a movie
def tfidf_similarity(game, movie, df_dict, total_game_words, total_movie_words):
    similarity_score = 0
    for key in game:
        if key in movie:
            game_desc = game[key] / total_game_words
            movie_summary = movie[key] / total_movie_words
            log_val = (total_movies + 1) / df_dict[key]
            similarity_score += song_lyric * movie_word * math.log(log_val)
    return similarity_score

# Computes the top 10 movie matches for a given song list
def calculate_movie_score(game_list, movie_list, titles_list, df_dict):
    movie_scores = []
    for idx, movie_dict in enumerate(movie_list):
        acc = 0
        for game_dict in game_list:
            total_song_words = game_dict[1]
            game_dict = song_dict[0]
            acc += tfidf_similarity(game_dict, movie_dict, df_dict, titles_list[idx][1], total_song_words)
        movie_scores.append((acc, title_list[idx][0]))
    movie_scores.sort()
    return [x[1] for x in movie_scores][-10:]

