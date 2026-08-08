# project :  steam companion

## goal :
Building a web application that works as a personal achievements timeline analytics tool for steam
## mvp (testing version 0.1.0):
- [x] Steam api call 
- [x] Take user's steam ID as input
- [x] Make a simple login page
- [x] Validate given ID
- [] Ability to present achievement by date like a story-line 
- [] Differenciate achievements by 3 levels of difficulty  
- [] Show basic stats of each chosen achievement

note : the app only works on owned games for now and does not include steam families or shared games

## goals for next version :
- [] Make a users database
- [] automate achievement fetching
- [] Add ability to track friends from the achievements page without needing a steam ID

### milestones :
#### research phase : 
- [x] Get a steam web api key
- [x] Read api documentation and understand basic api calls
- [x] Test api calls 
- [x] Decide tech stack 


### tech stack:
#### backend :
- python (logic)/ python-dotenv (managing environment variables and api keys)
- flask (web framework)
- steam web api (steam data fetching)
- sqlite (data base use for future features)
#### frontend :
- html
- css 
- bootstrap
- js 

## current task :
[] finish the timeline

## future tasks :
- [x] make a page to display achivements and a place holder for stats
- [x] enhance the achievement function to be able to return the date with each achievement 
- [x] make a display for ahievements by date 
- [] finish the timeline
- [] add validation checks on each field