# Play-Jeopardy

Welcome to the play-jeopardy bot github! 

You may be thinking..trivia bots for discord? Seems like a common idea.

You're right about that, but none of them actually resemble jeopardy at all. It's either a random question where people 'react' to pick an answer or a user inputs a command to pick a random category + value. Play-Jeopardy actually allows you to play a game of jeopardy with your friends - complete with a table of popular categories and standard values.

If you'd like to give the play-jeopardy bot a spin, you can find the invite link here: 
https://discord.com/oauth2/authorize?client_id=772633650751340574&scope=bot&permissions=117760

## How does it work

1. Invite the bot to your server with the above link. Create a dedicated Trivia/Jeopardy Channel if you'd like. 
2. Run the ```!setup``` command. This is to create your server & channel's dedicated jeopardy data.
3. Gather your friends, and have each of them run the ```!join``` command. These players are the only players allowed to use commands when the game is in session.
4. Run the ```!start_game``` command. This will kick off the game, and a random player will get picked to select a question from the category + value table.
5. That player will run the ```!select <category> <value>``` command (e.g. ```!select "movies & tv" 1000). 
6. Play-Jeopardy will send the question to the channel for everyone to read. It will then begin the pre-buzz countdown!
7. Jeopardy will count down until it sends the message "Go!", in which every player should buzz the channel. The buzz can be literally anything, but the fastest is one letter.
8. After, Jeopardy will gather every message sent by each player and the timestamps, and pick the earliest one (the differential can be less than a few milliseconds). This player gets to answer the question with the ```!answer <answer>```. You don't need to answer in the question format of Jeopardy, just put in the keyword answer.
9. If you get the answer correct straight up, Play-Jeopardy will automatically award you the points, and you get to select the next question for the cycle to repeat itself again. If Play-Jeopardy is unsure, it will send you a DM with a table containing your answer, and the correct answer, for you to use your judgement on whether or not you should get the points or not. This is to solve any issues with misspelling. We rely on the honor system here, and figured that no one is going to cheat in a game of jeopardy with your friends.
10. To override, simply type Y or Yes into the channel and it will award you the points and proceed as normal. To continue without overriding, enter N or No into the channel and it'll allow the people who have not attempted the question yet a chance to buzz and steal. This continues until everyone has attempted. 
11. If everyone has attempted the question, and no one got it right, Play Jeopardy will share the answer to the channel and randomly select a player to pick a new question.
12. After all of the questions are selected, Play-Jeopardy will trigger the ```!endgame``` command itself, and a winner will be declared. If there is a tie, Play-Jeopardy picks a random question for the people tied to answer until one gets it right and wins.

Happy Jeopardy-ing!