import csv
import json
import collections
import matplotlib.pyplot as plt

    
# Open Top Albums csv file, create list albums.
with open('data.csv') as f:
    albums = []
    for row in csv.DictReader(f):
        albums.append(row)

        
# # Open Top 500 Songs txt file, create list songs.        
# text_file = open('top-500-songs.txt', 'r')
# lines = text_file.readlines()
# song_list = []
# for line in lines:
#     line_list = line.split('\t')
#     song_list.append(line_list)      
# songs = []
# for s in song_list:
#     song = {'rank': s[0],
#             'name': s[1],
#             'artist': s[2],
#             'year': s[3][:-1],
#                 }
#     songs.append(song)

# Open Top 500 Songs txt file, create list songs.
text_file = open('top-500-songs.txt', 'r')
lines = text_file.readlines()
song_list = []
songs = []
for line in lines:
    song_list.append(line.split('\t'))
for song in song_list:
    songs.append({'rank': song[0], 'name': song[1], 'artist': song[2], 'year': song[3][:-1]})


# Open Top 500 Songs json file, create list songs_data.
file = open('track_data.json', 'r')
songs_data = json.load(file)


# Pass album name and data set, returns dict of album info.
def find_by_album(name, data_set):
    for entry in data_set:
        if entry['album'].lower() == name.lower():
            return entry
        else:
            return None


# Pass album rank and data set, returns album name, rank.
def find_by_rank(rank, data_set):
    for entry in data_set:
        if int(entry['number']) == rank:
            return entry['album'], rank
        else:
            return None

        
# Pass start rank, end rank and data set, returns list of album names in range (inclusive).
def find_by_ranks(start_rk, end_rk, data_set):
    result = []
    for entry in data_set:
        if int(entry['number']) in range(start_rk, end_rk + 1):
            result.append(entry['album'])
    return result


# Pass year and data set, returns list of album names in that year. 
def find_by_year(year, data_set):
    result = []
    for entry in data_set:
        if int(entry['year']) == year:
            result.append(entry['album'])
    return result


# Pass start year, end year and data set, returns list of album names in range (inclusive).
def find_by_years(start_yr, end_yr, data_set):
    result = []
    for entry in data_set:
        if int(entry['year']) in range(start_yr, end_yr + 1):
            result.append(entry['album'])
    return result


# Pass data set, returns list of all album titles.
def all_albums(data_set):
    result = []
    for entry in data_set:
        result.append(entry['album'])
    return result


# Pass data set, returns list of all artist names.
def all_artists(data_set):
    result = []
    for entry in data_set:
        result.append(entry['artist'])
    return result


# Pass data set, returns list of all songs.
def all_songs(data_set):
    result = []
    for entry in data_set:
        result.append(entry['name'])
    return result
# Set variable for easy use.
top_500 = all_songs(songs)


# Pass data set, returns artist with the most albums on Top Albums list.
def artist_w_most_albums(data_set):
    sample = all_artists(data_set)
    c = collections.Counter(sample)
    return c.most_common(1)

    
# Pass data set, returns word used most in all album titles.
def most_pop_word(data_set):
    result = []
    for entry in all_titles(data_set):
        word_list = entry.split()
        for entry in word_list:
            result.append(entry)
    c = collections.Counter(result)
    return c.most_common(1)


# Pass data set, returns histogram of (decade, number of albums in decade).
def year_hist(data_set):
    result = []
    for entry in data_set:
        result.append(int(entry['year']))
    num_bins = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]
    plt.hist(result, num_bins, facecolor='blue', alpha=1)
    plt.title('Album Histogram')
    plt.xlabel('Number of Albums')
    plt.ylabel('Years')
    return plt.show()
                       

# Pass data set, returns histogram of (genre, number of albums in genre).                     
def genre_hist(data_set):
    result = []
    for entry in data_set:
        result.append(entry['genre']) 
    c = collections.Counter(result)
    plt.bar(range(len(c)), c.values(), alpha=1)
    plt.title('Genre')
    plt.xlabel('Genres')
    plt.ylabel('Counter')
    return plt.show()


# Returns album with the most songs in Top 500 list.
def album_w_most_songs():
    sample = {}
    most_songs = 0
    top_album = []
    for entry in songs_data:
        i = 0
        track_list = []
        for song in entry['tracks']:
            track_list.append(song)
            for track in track_list:
                if track in all_songs(songs):
                    i += 1
                    sample[entry['album']] = [entry['artist'], i]
                    if i > most_songs:
                        most_songs = i
                        top_album = [entry['artist'], entry['album']]
    return top_album


# Returns list of albums with at least one song in Top 500 Songs list.
def albums_w_top_songs():
    result = []
    for album in songs_data:
        track_list = []
        for song in album['tracks']:
            track_list.append(song)
            for track in track_list:
                if track in all_songs(songs):
                    result.append(album['album'])
    return list(set(result))
albums_w_top_songs()


# Returns list of songs in the Top Albums list.
def songs_in_top_albums():
    result = []
    for album in songs_data:
        if album['album'] in all_albums(albums):
            for song in album['tracks']:
                result.append(song)
    return result
songs_in_top_albums()


# Returns histogram of (top 10 albums by number of songs in Top 500 Songs list, corresponding number).
def top_albums_hist():
    sample = []
    for album in songs_data:
        track_list = []
        for song in album['tracks']:
            track_list.append(song)
            for track in track_list:
                if track in all_songs(songs):
                    sample.append(album['album'])
    counter = collections.Counter(sample)
    c = counter.most_common(10)
    numbers = []
    titles = []
    for item in counter.most_common(10):
        titles.append(item[0])
        numbers.append(item[1])
    plt.bar(titles, numbers, alpha=1)
    plt.title('Top 10 Album')
    plt.xlabel('Albums')
    plt.ylabel('Apperances')
    return plt.show()


# Returns top overall artist by number of songs in Top 500 Songs list plus number of albums in Top Albums list.
def top_overall_artist():
    sample = {}
    i = 0
    for artist in all_artists(albums):
        sample[artist] = i
    for album in songs_data:
        if album['album'] in all_albums(albums):
            sample[album['artist']] += 1
    for song in songs:
        if song['artist'] not in sample.keys():
            sample[song['artist']] = i + 1
        sample[song['artist']] += 1
    top = max(sample.values())
    for artist in sample:
        if sample[artist] == top:
            return artist, top
top_overall_artist()

