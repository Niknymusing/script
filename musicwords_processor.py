genres_text_file = "music_genres.txt"
audio_events_text_file = "audio_events.txt"

f = open(genres_text_file , "r")
string1 = f.read()
g = open(audio_events_text_file , "r")
string2 = g.read()
list_of_audio_events = string1.split(',')
list_of_music_genres = string2.split(',')

print(list_of_audio_events)
print(list_of_music_genres)