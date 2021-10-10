# Aim : To generate data frames similar to data warehouse for analysis

### Data : Netflix data related to movies and series. It has 11697 rows and 31 columns. 

### Columns: 

['movie_id', 'index', 'title', 'genre', 'tags', 'languages',
       'Movie_Series', 'hidden_gem_score', 'country_available', 'runtime',
       'director', 'writer', 'actors', 'view_rating', 'imdb_score',
       'rotten_tomatoes_score', 'metacritic_score', 'awards_received',
       'awards_nominated_for', 'box_office', 'release_date',
       'netflix_relase_date', 'production_house', 'netflix_link', 'imdb_link',
       'summary', 'imdb_votes', 'image', 'poster', 'tmdb_trailer',
       'trailer_site']
      
  ### Create movie related data:
  
  ![image](https://user-images.githubusercontent.com/67071872/136695938-322ec59c-c6f8-4299-9ace-ee57d4ec4685.png)

## Data frames created:
## movies_df : Contains quantitative information about a given movie. 

'movie_id', 'title', 'Movie_Series', 'runtime', 'view_rating',
       'imdb_score', 'rotten_tomatoes_score', 'metacritic_score', 'box_office',
       'awards_received', 'release_date', 'release_year', 'release_qtr',
       'netflix_relase_date', 'netflix_release_yr', 'netflix_release_qtr'
       
 **movie_id - Is a unique value to indetify each title**
 
 ## genre_df: Contains a genre_flag for each title. 
 
 ['movie_id', 'title', 'genre', 'filmnoir', 'thriller', 'sport', 'news',
       'western', 'horror', 'adventure', 'history', 'fantasy', 'realitytv',
       'musical', 'war', 'biography', 'comedy', 'action', 'short', 'talkshow',
       'crime', 'music', 'adult', 'animation', 'family', 'romance',
       'documentary', 'drama', 'scifi', 'mystery', 'na', 'gameshow']
       
Flag Values are : ['Y','N']

### Sample data:

![image](https://user-images.githubusercontent.com/67071872/136696251-c278c118-9edd-4dcf-a8e5-ae833c461d61.png)

