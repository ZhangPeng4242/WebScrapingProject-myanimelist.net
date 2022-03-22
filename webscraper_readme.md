# MyAnimeList web Scraper
The program scrapes information from the website MyAnimeList and stores it in several csv files.

## How We Did It

We first Notice there are 6 types of pages in MyAnimeList from which we wanted to get information:
- anime list page (e.g. [link](https://myanimelist.net/topanime.php))
- people list page (e.g. [link](https://myanimelist.net/people.php))
- anime main page (e.g. [link](https://myanimelist.net/anime/43608/Kaguya-sama_wa_Kokurasetai__Ultra_Romantic))
- anime stat page (e.g. [link](https://myanimelist.net/anime/43608/Kaguya-sama_wa_Kokurasetai__Ultra_Romantic/stats))
- people main page (e.g. [link](https://myanimelist.net/people/118/Hiroshi_Kamiya))


We first used the Requests module along with the fake-useragent module and the free proxy list provided [here](https://www.sslproxies.org/) to create  random proxy and header generators so that we will be able to scrap the website without being blocked.

We then used BeautifulSoup to write a scraper for each type of page which extracts the information we are interested in. For the first two types of pages, the information is a list of other links, while for the last three, it is a fixed length tuple of dictionaries. Each dictionary represents information which will later be stored in its own csv file. 

We then created functions to create and store our extracted information in several csv files and use pandas to reformat and prepare them to be uploaded to a mysql database.All files are stored in a new directory called init_datas and come with the main download of the program, but could be recreated using other modules in the main file. We then use SQLAlchemy to store the data into the following EDR:

![EDR](/pictures/EDR.png)


Four additional text files containig a list of all proxies, a list of all anime page links, a list of all people page links, and a list of all errors that occured during running the program will also be created.

The program was wraped for user interface using argparse, using the arguments decribes in the usage section, the user can set up the database in mysql and then update it fully or partially based on several options. 



## Requirements.
to use the progrm the user needs the following python packages installed:
- requierments
- bs4
- fake-useragent
- pathlib2
- pandas 
- SQLAlchemy
- sqlparse

## Usage
To use the program, first download the dircetory provided above, then run main with the appropriate sequence of arguments, according to your desired goals. We now provide a map of all possible arguments, as well as an explenation on their respective functions:



### First Positional Argument:
there are two posible choises for the first positional arguments:
- init - This argument is used to set up the  database either loaclly or remotely.
note: **When running main for the first time this argument must be used** also note that while running init for the first time a config.json file will be created inside of the directory main is stored in. changing the values of this file allows the user to configure the web scraper as he likes.
- scrap - this argument is used to update the existing database or some parts of it.

### Second Positional Argument:
The possible values of this argument depend on the value of the first argument.
#### After Using init
there are two possible values for the second argument:
- loacl- This will setup the anime database locally on the users computer. after using loacl the user must provide a username and password, and optionally a host name (which by default is "host") 
-remote -  This will setup the anime database remotely. Much like the previous case, after using remote the user must provide a username and password, and optionally a host name (which by default is "host")

here are usage examples of bth cases:
 ```python
# store database locally 
webscaper/main.py init local yam 111

# store database remotely
webscaper/main.py init remote yam 111
```

#### After Using scrap
there are four possible values for the second argument (if no value is specified, the program will run as if all was selected):
 
- anime- This will update only information available in the anime info and anime stats pages. if the user would like to update a more specifc category of anime the following flags are availabe: --name, --rank ,--year, --genre, --studio. if non of this is specified the tables above will be completely updated.
- people- This will update only information available in the people pages. if the user would like to update a more specifc category of people the following flags are availabe: --name, --rank (updates all people this rank or higher) ,--anime (only updates people who were staff in a certain anime provided by anime name) if non of this is specified the tables above will be completely updated. 

- all-updates the whole database

here are some usage exapmles:
 ```python
# update anime by name  
webscaper/main.py scrap anime --name Shingeki no Kyojin 

# updae people with rank higher than 250
webscaper/main.py scrap people rank 250
 

```
finally, here is a map of all arguments:
![Argument Map](/pictures/arg_map.png)
