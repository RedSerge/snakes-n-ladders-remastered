# Snakes & Ladders: Remastered (MVP)

This idea came to me when I realized that in the classic Snakes & Ladders, I am not a player but a spectator of a random event. I wanted more action, so I decided to change that, improve the rules, and make “the Shadow Tournament” for my own joy.

The main rules are the same: you roll the dice and move your piece to the corresponding cell. If there’s a blue arrow (stair), you move up. If there’s an orange arrow (snake), you move down. If you get the dice number 6, you roll the dice again. If you go beyond 100, you must “bounce” from the last cell (101 -> 99, 102 -> 98, etc.). Then you pass the turn to another player. The winner is the one who’s reached the 100 first.

Now, about some improvements. First, players have two pieces each, and they can decide which one is moving after looking at the dice. Second, you get a double-roll for the dice number 5, too, not just 6. Third, going down the snake has a bonus: it increases your reserving capacity, so you can preserve (or “cache”) the dice to use later.

You can use your cache in two ways. First, use it fully or ‘simultaneously’. Second, use it ‘dice-by-dice’. In both cases, the piece first makes its turn according to the rolled combination. Then, the cache is applied. ‘Simultaneously’ means that the whole accumulated sum is used to move the piece in one big move. ‘Dice-by-dice’ means that the piece is moved by each dice number one dice after another, taking into consideration all ladders and snakes along the way.

Let’s look at the map to understand it better.

![A version of a map](/static/snakeboard.png "A version of a map used in this MVP")

Say, a piece position is at 60, a current throw is 1, and the cache is [1, 6, 2, 5, 5].

The simultaneous cache is applied like that: 1+6+2+5+5 = 19.

60 + 1 (current throw) -> 61, 61 + 19 -> 80, 80 is a stair to 100 -> Victory!

The dice-by-dice cache usage in this situation will result in a series of movements:

60 -> 61 (current throw) -> 62 (a snake to 19) -> 25 -> 27 -> 32 -> 37. A downfall. But thanks (?) to the snake, you can cache one more dice now (your reserving capacity is one).

This concept of an app :) is using Python & Flask, so if you got both installed, you can just run “app.py” from a console and open “localhost:5000” in your browser.

To make a move, you must press two keys – first, 1 or 2 for the violet or the green piece, respectively – or ‘\`’, that symbol under tilde ‘~’ on the same key if you don’t want to move your pieces but want to cache the current dice chain instead if it’s possible (in the text “CACHED DICE: (N to add)” N must be greater than 0).
The second key represents the way you want to use your cache: ‘dice-by-dice’ (press ‘[‘), ‘simultaneously’ (press ‘]’), or don’t want to use it yet (any other key).
In fact, the second key is useless if you press the ‘\`’ key but saved for the sake of an input uniformity, so you have to spend roughly equal time for each movement, which is important for the Shadow Tournament; more about that later. Usually, it’s good to double-press the first key if you don’t plan to use your cache, like ‘1’-‘1’, ‘2’-‘2’, ‘\`’-‘\`’ sequentially.

Pieces move until someone has won by placing his piece on the last cell, # 100. To reset the game, you can press the ‘DEL’ key. Or, if you are the winner, you can press the ‘Ctrl+DEL’ combination to enter the Shadow Tournament, a type of hot-seat mode.

In the Shadow Tournament mode, the bots are turned off. You can invite your friend (who hopefully was not looking at how you played) and encourage him to repeat your last journey: he will get the same dice as you (or random ones after he’s exceeded the number of steps you’ve taken to the finish). If he manages to spend less/equal quantity of steps and time (counted from the first performed move to the finish) to get his victory, he is considered a winner, and if not – then it’s you. 

To check the status, see the server-side console window. But don’t investigate it during the tournament – some debug messages can help you cheat, and no one wants to spoil the fun, now do they?

The result may look like this:

“=== TOURNAMENT OF THE SHADOWS RESULT: ===

15 VS 15

0:00:39.149962 VS 0:00:52.452576

RESULT: VICTORY!

=== *** ===”

The result is printed with the 2nd player in mind. If he is defeated, then it’s your victory.

Now the 2nd player presses the ‘DEL’ key and starts anew, trying to defeat bots and restart the Shadow Tournament for you. And so on.

Tip: one more thing, if you want to turn the bots off completely, just make a file called “.nobots” in the directory with the game (app.py). I provided some cmd scripts to make it easier for Windows users (“bots on/bots off” commands, as some versions of Windows prevent you from making empty-named files; Linux users can just create them, though, with no problem).

Enjoy (if you can :’D ) this raw prototype version of my idea. You can always play it in real life; it’s just computer usually counts faster. :))) 
