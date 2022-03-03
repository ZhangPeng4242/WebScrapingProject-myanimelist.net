# MyAnimeList web Scraper
The program scrapes information from the website MyAnimeList and stores it in several csv files.

## How We Did It

We first Notice there are 5 types of pages in MyAnimeList from which we wanted to get information:
- anime list page (e.g. [link](https://myanimelist.net/topanime.php))
- people list page (e.g. [link](https://myanimelist.net/people.php))
- anime main page (e.g. [link](https://myanimelist.net/anime/43608/Kaguya-sama_wa_Kokurasetai__Ultra_Romantic))
- anime stat page (e.g. [link](https://myanimelist.net/anime/43608/Kaguya-sama_wa_Kokurasetai__Ultra_Romantic/stats))
- people main page (e.g. [link](https://myanimelist.net/people/118/Hiroshi_Kamiya))

We first used the Requests module along with the fake-useragent module and the free proxy list provided [here](https://www.sslproxies.org/) to create  random proxy and header generators so that we will be able to scrap the website without being blocked.

We then used BeautifulSoup to write a scraper for each type of page which extracts the information we are interested in. For the first two types of pages, the information is a list of other links, while for the last three, it is a fixed length tuple of dictionaries. Each dictionary represents information which will later be stored in its own csv file. 

We then created functions to create and store our extracted information in several csv files. all files will be stored in a new directory called Datas, created inside the paretnt directory of the current directory. the files which will be created are the following:

**store anime page**
- anime_info.csv - contains  anime_id, title, type, aired, premiered, studios, source, genres, rating and theme.
-  alternative_titles.csv - contains anime_id, and english_title
- anime_site_stats.csv contains anime_id, score, rating_count, ranked, popularity, members, and favorites

**store people page data**
- people_info.csv - contains people_id, people_full_name, birthday, member_favorites and people_img_url
- anime_characters_info.csv - contains character_id, anime_id, character_fullname, role, character_favorites and character_img_url
- voice_actors_info.csv - contains character_id and people_id
- staff_info.csv - contains anime_id, people_id and staff role

**store stats page**
- anime_watch_stats.csv - contains anime_id, Watching, Completed, On-Hold, Dropped, Plan_to_Watch and Total 
- anime_score_stats.csv - contains anime_id and num of people who rated the anime 1 - 10

four additional text files containig a list of all proxies, a list of all anime page links, a list of all people page links, and a list of all errors that occured during running the program will also be created.


Finally, our main function uses all previous functions to create and store all of these files filled with the information we collected, on the user's computer. 


## Usage and Requirements.
to use the progrm the user needs the following python packages installed:
- requierments
- bs4
- fake-useragent
- pathlib2 

To use the program, download all the different libraries we have created and provided above, and then run main.