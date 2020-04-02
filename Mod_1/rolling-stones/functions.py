
import collections
import matplotlib.pyplot as plt

    
# Pass album name and data set, returns dict of album info.
def find_by_album(album, data_set):
    for entry in data_set:
        print(entry)
        if entry['album'].lower() == album.lower():
            return entry
        else:
            return None

        
# Pass album name, returns dict of album info.
def find_by_name(name, data_set):
    for album in data_set:
        if album['album'].lower() == name.lower():
            return album
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
    for entry in songs_data:
        track_list = []
        for song in album['tracks']:
            track_list.append(song)
            for track in track_list:
                if track in top_500:
                    result.append(entry['album'])
    return list(set(result))


# Returns list of songs in the Top Albums list.
def songs_in_top_albums():
    result = []
    for entry in songs_data:
        if entry['album'] in all_albums(albums):
            for song in entry['tracks']:
                result.append(song)
    return result


# Returns histogram of (top 10 albums by number of songs in Top 500 Songs list, corresponding number).
def top_albums_hist():
    sample = []
    for entry in songs_data:
        track_list = []
        for song in entry['tracks']:
            track_list.append(song)
            for track in track_list:
                if track in top_500:
                    sample.append(entry['album'])
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
    for entry in all_artists(albums):
        sample[entry] = i
    for entry in songs_data:
        if entry['album'] in all_albums(albums):
            sample[entry['artist']] += 1
    for entry in songs:
        if entry['artist'] not in sample.keys():
            sample[entry['artist']] = i + 1
        sample[entry['artist']] += 1
    top = max(sample.values())
    for entry in sample:
        if sample[entry] == top:
            return entry, top
top_overall_artist()

