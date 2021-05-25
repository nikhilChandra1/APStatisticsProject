import selenium
from selenium import webdriver
import time
import csv
from random import sample
#parses through the csv file and creates a list of tuples for all billboard songs.
#the tuple order is (year, song name, song artist)
allSongs = []
with open('/Users/nikhil.c/Downloads/charts.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            songTuple = ((row[0][:4]), row[2], row[3])
            allSongs.append(songTuple)
      
#find all songs that are out of the 1960 to 2020 range
valuesToRemove = []
counter = 0
for song in allSongs:
    if (int(song[0]) < 1970 or int(song[0])>2020):
        print(song)
        valuesToRemove.append(counter)
    counter = counter + 1
    
#remove all songs that are out of the 1960 to 2020 range
counter = 0
for value in valuesToRemove:
    index = value - counter
    
    allSongs.pop(index)
    counter = counter + 1

print(len(allSongs))
decade1Songs = []
decade2Songs = []
decade3Songs = []
decade4Songs = []
decade5Songs = []
decade6Songs = []

for song in allSongs:
    if ((int(song[0]) >=1960) and (int(song[0]) < 1970)):
        decade1Songs.append(song)
    if ((int(song[0]) >=1970) and (int(song[0]) < 1980)):
        decade2Songs.append(song)
    if ((int(song[0]) >=1980) and (int(song[0]) < 1990)):
        decade3Songs.append(song)
    if ((int(song[0]) >=1990) and (int(song[0]) < 2000)):
        decade4Songs.append(song)
    if ((int(song[0]) >=2000) and (int(song[0]) < 2010)):
        decade5Songs.append(song)
    if ((int(song[0]) >=2010) and (int(song[0]) < 2020)):
        decade6Songs.append(song)

#randomly sample 1.7k from each decade, for a 10.2k total sample size

def createRandomlySampledArray(array):
    randomlySampledArray = sample(array, 200)
    return randomlySampledArray
    

decade2RandomSample = createRandomlySampledArray(decade2Songs)
decade3RandomSample = createRandomlySampledArray(decade3Songs)
decade4RandomSample = createRandomlySampledArray(decade4Songs)
decade5RandomSample = createRandomlySampledArray(decade5Songs)
decade6RandomSample = createRandomlySampledArray(decade6Songs)
print(len(decade6RandomSample))


#this function loops through a website and finds the genre associated with a song. All the genres are then recorded in a file

def getAllGenres(decadeSongs, nameOfTextFile):
    waitingForSuggestion = True
    # Using Firefox to access web
    driver = webdriver.Firefox()
    # Open the website
    driver.get('https://www.chosic.com/music-genre-finder/')
    time.sleep(2)
    File = open(nameOfTextFile, "a+")
    songBox = driver.find_element_by_id('search-word')
    for song in decadeSongs:
        waitingForSuggestion = True
        print(song)
        
            
        
        #input the song into the search box
        searchElement = song[1] + " " + song[2]
        a_string = "!?.!@#$%^&+=~<>?***()_{:<<>?"
        editedSearchElement = ""
        for character in searchElement:
            if (character not in a_string) and (character.isdigit() is False):
                editedSearchElement += character
        songBox = driver.find_element_by_id('search-word')
        songBox.send_keys(editedSearchElement)
            
        time.sleep(1)
        counter = 0
        while waitingForSuggestion:
            try:
                songBox.click()
                #click on the first suggestion for the song
                firstSuggestion = driver.find_element_by_id('hh1')
                firstSuggestion.click()
                time.sleep(0.1)
                waitingForSuggestion = True
                #using the page source, find the genre for the song
                pageSource = driver.page_source
                list = pageSource.split('https://www.chosic.com/genre-chart/explore/?genre=')
                genreStringRaw = list[1]
                genre = genreStringRaw.replace('</a><a href=', '')
                genre = genre.replace('">', '')
                genre = genre[:int(len(genre)/2)]
                #record the genre to a file
                print(len(genre))
                if len(genre) < 1000:
                    File.write('\n')
                    File.write(genre)
                    print(genre)
            
                waitingForSuggestion = False
                break
            except:
                #the idea here is that if a suggestion could not be found, just let the website load for a second more then look again
                waitingForSuggestion = True
                if counter != 3 and counter != 5:
                    time.sleep(1)
                counter = counter + 1
                
                #if the website has failed to find a suggestion three times, try doing a search without the artist name
                if counter ==3:
                    driver.get('https://www.chosic.com/music-genre-finder/')
                    searchElement = song[1]
                    editedSearchElement = ""
                    a_string = "!?.!@#$%^&+=~<>?***()_{:<<>?"
                    for character in searchElement:
                        if (character not in a_string) and (character.isdigit() is False):
                            editedSearchElement += character
                    songBox = driver.find_element_by_id('search-word')
                    songBox.send_keys(editedSearchElement)
                    time.sleep(1)
                #if the website has failed to find a suggestion 10 times, then just move onto the next song
                if counter ==10:
                    driver.get('https://www.chosic.com/music-genre-finder/')
                    waitingForSuggestion = False
                    break
      
    File.close()
            
            
            
        
        
    


getAllGenres(decade2RandomSample, "decade2Genres.txt")
getAllGenres(decade3RandomSample, "decade3Genres.txt")
getAllGenres(decade4RandomSample, "decade4Genres.txt")
getAllGenres(decade5RandomSample, "decade5Genres.txt")
getAllGenres(decade6RandomSample, "decade6Genres.txt")
        
    
    
        
    



