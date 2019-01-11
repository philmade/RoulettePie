import random

global test_c_wins
test_c_wins = []

def reset_strategy():
    global strategy
    strategy = {
    "bank" : 1000,
    "stake" : 2,
    "target" : 1.5, # defines when to stop playing should the bank * this amount is reached
    "stoploss" : 0.5, # defines the size of the bet (* bank) which should make the machine step away from the table.
    "bet_increase_lose" : 2, #defines how much to increase the stake should it lose - for ex bet_increase = 2 wil
    "bet_increase_win" : 2, # NEW - defines how much to increase the bet should it win - idea via reddit
    "reset_stake" : 17, # NEW - defines how often the strategy should reset itself back to it's original strategy. If

}
    return
    strategy

def reset_bank():
    strategy['bank'] = 1000

def roulette():
    # plays the game of Roulette with a globally defined strategy 
    # Returns bank

    from random import randint

    bank = strategy['bank']
    stake = strategy['stake']
    target = strategy['target']
    stoploss = strategy['stoploss']
    bet_increase_lose = strategy['bet_increase_lose']
    bet_increase_win = strategy['bet_increase_win']
    reset_stake = strategy['reset_stake']

    while bank >= stake and \
                    bank > 0 and \
                    bank <= target * bank and \
                    stake <= stoploss * bank:

        #place the stake on the table
        bank -= stake

        #produce a result
        result = randint(0,36)

        if result == 0 :

            #the house wins, so you must double your stake
            stake *= bet_increase_lose
            strategy['bank'] = round(bank,0)

        elif result%2  == 0:

            #it's an EVEN number, so you won!

            # add my winnings and return the stake
            bank += (stake * 2)

            # NEW! Increase the bet even if you won! This means we must randomly return stake some other way
            stake *= bet_increase_win
            strategy['bank'] = round(bank,0)

        # if the result is between the two numbers in the reset_strategy range, ie 0 and 9, then reset the stake.
        # elif result == enumerate(strategy['reset_stake'],1):
        elif 0 <= result <= reset_stake :
            stake = strategy['stake']
            # print("The result was {} resetting stake back to {}" .format(result,strategy['stake']))
            

        else:
            #it must be an odd number, you LOST, therefore double your stake
            stake *= bet_increase_lose
            strategy['bank'] = round(bank,0)

def roulette_player():

    """Roulette player manages the roulette function.    
    If the strategy isn't producing money, it generates a random strategy. 
    If it works after 10 iterations, it is tested over 100, then finally 1000. 
    ."""
    
    def randomise_strategy():
                strategy['stake'] = round(random.uniform(2,10),2)
                strategy['target'] = round(random.uniform(1.1,10),2)
                strategy['stoploss'] = round(random.uniform(0.2, 0.8),2)
                strategy['bet_increase_lose'] = round(random.uniform(2, 100),2)
                strategy['bet_increase_win'] = round(random.uniform(2,100),2)
                strategy['reset_stake'] = round(random.uniform(0,36),0)
                reset_bank()

    def test_further_a():
        iterations = 0
        test_a = []
        # print("Testing to 100")
        reset_bank()

        while iterations <= 100 and strategy['bank'] >= 0:
            
            iterations += 1

            # Produce a result using the current strategy
            roulette()

            # add the result to test_b
            test_a.append(strategy['bank'])

            if len(test_a) == 100 and test_a[99] >= test_a[0]:
                # print("Strategy worked for 100 iterations.{}" .format(strategy))
                # print("The results were {}" .format(test_a))
                # print("Worked for 100 iterations. Test_a failed {} times before this" .format(fail_count))
                test_further_b()


            elif len(test_a) == 100 and test_a[99] <= test_a[0]:
                break
    
    def test_further_b():
        iterations = 0
        test_b = []
        # print ("Testing to 1000")
        reset_bank()


        while iterations <= 1000:
            
            iterations += 1

            # Produce a result using the current strategy
            roulette()

            # add the result to test_b
            test_b.append(strategy['bank'])

            if len(test_b) == 1000 and test_b[999] >= test_b[0]:
                 # print("IT WORKED for 1000 iterations! The bank started with {} and ended with {}" .format(test_b[0],test_b[999]))
                 # print("The strategy was {}" .format(strategy))
                 # print("Worked for 1000 iterations - test_B failed {} times before this" .format(fail_count))
                test_further_c()

            elif len(test_b) == 1000 and test_b[999] <= test_b[0]:
                 # fail_count += 1
                break
    
    def test_further_c():
        iterations = 0
        test_c=[]
        #print("Testing to 5,000")
        reset_bank()


        while iterations <= 5000:
            
            iterations += 1

            # Produce a result using the current strategy
            roulette()

            # add the result to test_b
            test_c.append(strategy['bank'])

           # if len(test_b)%10 == 10: 
            if len(test_c) == 5000 and test_c[4999] >= test_c[0]:
                print("FIVE THOUSAND ITERATIONS! The bank started with {} and ended with {}" .format(test_c[0],test_c[4999]))
                print(strategy)
                test_c_wins.append(strategy.copy())
            elif len(test_c) == 5000 and test_c[4999] <= test_c[0]:
                break
    
    def final_test():
        iterator = 0
        final_test = []
        final_test_results = []

        # print("The winning strategies were{}".format(test_c_wins))
        for each_strategy in test_c_wins:
            
            strategy.update(test_c_wins[iterator])
            print("The new strategy is {}" .format(strategy))
            reset_bank()

            while len(final_test_results) <= 10000: #strategy['bank'] <= strategy['bank'] * strategy['target']:
                roulette()
                # print(strategy['bank'])
                final_test_results.append(strategy['bank'])

            else:
                print("The strategy starting with {} and ended with {}" .format(final_test_results[0],final_test_results[-1]))
                print("At one time, there was {} in the bank" .format(max(final_test_results)))
                final_test_results = []    
                iterator += 1

    import random
    iterations = 0
    first_test = []

    # Code looks for 10 strategies in test_c_wins before it stops the while loop
    while len(test_c_wins) <= 10:
        # produce a result using roulette() function # add the result to first_test
        iterations += 1
        roulette()      
        first_test.append(strategy['bank'])

        #    compares results to see if it was winning money, or losing

        if len(first_test) == 10 and first_test[9] <= first_test[0]:
                # print("Strategy fail. Randomising")
                first_test = []
                randomise_strategy()


        if len(first_test) == 10 and first_test[9] >= first_test[0]:
                # print ("The bank started with {} and ended with {}" .format(first_test[0],first_test[9]))
                # print(" Result. Testing strategy further....")
                # print(strategy)
                reset_bank()
                first_test=[]
                test_further_a()

    final_test()


reset_strategy()
reset_bank()
roulette_player()
print(test_c_wins)
print("All done!")

