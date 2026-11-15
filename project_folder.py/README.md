# MY FIRST REAL PROJECT IN PYTHON

# First of all my name is Audran i'm 17 and i started programming 10 months ago and absolutely love it, that's why i took CS50P and it was a blasr even if it was hard i enjoyed what it made me become more determined and able to solve problems

# Let's talk about the code:

# First of all my project is a small (very beginner level) trading bot it doesn't properly trade but it gets the orderbook from 3 different crypto-currencies, extract the needed information from these orderbooks such as the bids and asks for those currencies and then with those in hand we can start the funny part which is "buying" and "selling" to do so we parse the asks and bids for the best (top) bids ans asks for the best offers. When we got those we start looping over the sorted orderbooks and start buying and selling with a budget of our choice, such as 100, 1000 or even 10000 virtul "dollars". Then we buy until we've reached the target and sell back trying to make a profit, of course my small bot even tho im proud of it doesnt make me mones it only looses but that wasn't the main goal of that project, it was pure discovery.

# Now in details:
# FIRST FUNCTION(pair_buy):

# this fucntion was easily the hardest thing i've had to code during my journey it might look easy at first but i had to properly set up the orderbook which took a super while and set up limit and all (tedious).
# So we start by looping over the orderboon unpacking price and quantity (an orderbook looks like [price, quantitty], example [80000$, 5 bitcoins (it's not 80k for 1 bitcoins its the price per unit of the currency)])
# Then with these prices and quantity unpack we add them to a set to make surr we don't get duplicated values (because i used not so high frequency requests to get tbhose price it was not very much the case of duplicated prices but it prevent it either way)
# When this is done we set our target (how much ofthe currency we can REALISTICALLY buy with our starting budget, it is target = initial budget / price, example 100000/80000 = 5/4 or 1,2 of a bitcoin we can buy and it updates for every cycle otherwise it would be fixed and that's a CRIME) we then can start doing the operations...
# if the target (what we CAN buy) is smaller than the quantity that the orderbook offers us so in realm life it's just someone offering to sell this much currency, so for example if he offers 1 bitcoin and our target is 5,4 or 1,2 we can go ahead and buy that whole 1 bictoin.
# We update then our variables:
# -The accumulated currency is 0 at the start (we bought nothing) we add the quantity bought so here it goes from 0 to ... 1 because we bought one whole bitcoin (i went back and forth at least a week on that fucntion everytime i made a change the code would behave another way) -We update our spending, we spent quantity * price so here 1 * 80000 -> 80k$ spent! and finally -original balance which was just the original budget (100k$) we subtract the quantity * price, here 100k - 80k * 1 = 20k$ left. Once again i know i'm annoying i'f would so much encourage you to try to even recreate this it is so annoying (i'm smilling just thinking about it i SWEAR control flow...)
# Else if the seller who sells his bitcoin (or any other currency) sells more than we need, we just buy the remaining (our updated target, i got a headache the first time i did this like HOW CN WE JUST TAKE A PART OF A CURRENCY) so we buy that remaining target and add it to our accumulated currency it from our orignal balance, update the spending: target * price and subtract it from our original balance (budget) and we can safely set it to 0 to prevent any problems, then if sadly the original balance still isnt equal to 0 we check it and see if it's bigger than the liit if yes we print a message to the user and return None in main
# Otherwise if eevrything is good we return the currency accumulated with the added fees which are 1%

# 2ND FUCTION (pair_sell):
# This function is basically the same structurally as the buy one, the only changes is that we dont need any target since we just want to sell all of our accumulated currency, we do that by selling a bit if the quantity a buyer is asking for is smaller than our total currency amount else we give him eveyrthing and update our earnings leaving us with a final total (always around 30$ lost because of the fees)

# 3RD FUNCTION (deque_spread)
# One thing i learned is that we don't need the prices after we did the previous operations, what we actually need is spreads, the final amount - initial budget. It is mandatory because it tells us how the market behaves and we can easily do calculations on them.
# The function does the following: it takes the final amount and subtract the inital budget and we add it to a DEQUE, this is very important because it is very fast (O(1)) and allows us to effortlessly get values in and out. We add those to the deque and return it and this is the window that we'll do calculations on.

# 4th function (deque mean)
# Nothing special here, we just take the window and use the numpy library to calculate it's mean (which is just: total of all added values divided by the number of values) and we return it, the mean is capital for further calculations.

# 5th function (deque std dev)
# Here again, we use numpy to calculate the standard deviation which is just each value minus the window mean squared divided by the number of values if we have the whole population and minus one if we work with a sample we can clearly see why the mean is important...

# 6th function (deque z score)
# here everything assembles, the z score is basically what tells us if we have a situation where we would make money or not, the function just takes what weve calculated before and puts it to use, the formula is sample - mean divided by the standard deviation. in the function we loop over our window and calculate it raising a zero division error when the standard deviation is 0. And we return the zscore.

# Last function (signal):
# This function has for role to make the decision wheter we are buying or doing you can kinda see this whole thing before the final signal decision as dipping your feet into water and deciding if youre going in or not except here its not about you its about the market, first of all we check if the window length is adequate else we return, we also recheck for a standard deviation who would equal 0 in this case we return. Then we calculate the z score of the last elememt because its the one were making a decision on if his z score is beyond the threshold set and his profit is higher than the budget + margin set then th'ats a buy otherwise we wait until it's the case.

# THANK YOU 
