# linkedin_scraper
extracts linkedin profiles


this project extracts data from linkedin profiles, please read carefully to use it properly.

first download all librares that used on project.

changes in connect.py scripts
1) First you will need to download last version of chromedriver  https://chromedriver.chromium.org/downloads   (if you don't use chomre browser then there are other alternative drivers for other browsers).
Save installed chromedriver to linkedin_scraper folder. 
Then add path of chromedriver "Service('path')"  in connect.py

2) next,  enter your linkedin email and password of your linkedin account to the linkedin_connect() function.
Please, be carefull that you use your second/dummy linkedin account, because linkedin may ban the accaunt beacuse of too many requests.



changes in run_scrape.py scripts
1)  Add path to df_url=pd.read_csv(path), csv file should include linkedin urls... example: https://www.linkedin.com/in/tom_and_jerry/
It will extract and save linkedin profiles' data to /data folder.


After you have done with all changes , you can start scraping data by running run_scrape.py script.
