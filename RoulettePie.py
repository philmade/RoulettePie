import random
from random import randint
import keyboard

test_c_wins = []
test_d_wins = []

def reset_strategy():
    strategy = {
    "bank" : 1000,
    "stake" : 2,
    "target" : 1.5, # defines when to stop playing should the bank * this amount is reached
    "stoploss" : 0.5, # defines the size of the bet (* bank) which should make the machine step away from the table.
    "bet_increase_lose" : 2, #defines how much to increase the stake should it lose - for ex bet_increase = 2 wil
    "bet_increase_win" : 2, # NEW - defines how much to increase the bet should it win - idea via reddit
    "reset_stake" : 17, # NEW - defines how often the strategy should reset itself back to it's original strategy. If 
    }
    return strategy

def roulette(strategy):
    
    """
    ARGUMENTS : Strategy
    RETURNS: Bank
    Takes Dict as argument, which must have bank, stake, target, stoploss, 
    bet_increase_lose, bet_increase_win, reset_stake all defined as below. 
    Function then plays Roulette with the strategy passed through.
    """

    bank = strategy['bank']
    stake = strategy['stake']
    target = strategy['target']
    stoploss = strategy['stoploss']
    bet_increase_lose = strategy['bet_increase_lose']
    bet_increase_win = strategy['bet_increase_win']
    reset_stake = strategy['reset_stake']

    # plays the game until one of the conditions below are met.
    while bank >= stake and \
                    bank > 0 and \
                    bank <= target * bank and \
                    stake <= stoploss * bank:

        # Place the stake on the table
        bank -= stake

        # Produce a result
        result = randint(0,36)

        # Potential boolean conditions based on result
        win = result%2 == 0 # If the result is an even number, you win
        lose = result%2 != 0 or result == 0 # If it's an odd number, or 0, you lost.
        reset_strategy_trigger = 0 <= result <= reset_stake # if the result is between 0 and 'reset_stake', ie 0 and 9, then reset_strategy has been triggered.

        if lose:

            # you must increase your bet for next round
            stake *= bet_increase_lose
            strategy['bank'] = round(bank,0)

        elif win:

            # add my winnings and return the stake - returns double as we always bet on even.
            bank += (stake * 2)

            # NEW! Increase the bet even if you won! This means we must randomly return stake some other way
            stake *= bet_increase_win
            strategy['bank'] = round(bank,0)

        elif reset_strategy_trigger:
            # The stake is set back to what was originally passed in via roulette(strategy)
            stake = strategy['stake']
            
            # print('The result was {} resetting stake back to {}'.format(result,strategy['stake']))

    return round(bank,2)

def roulette_player():

    """
    Roulette player manages the roulette function.    
    If the strategy isn't producing money, it generates a random strategy. 
    If it works after 10 iterations, it is tested via test_further_a, then test_further_b, then test_further_c. 
    """
    
    iterations = 0
    strategy = reset_strategy()
    first_test = [] # where we'll keep a list of results from our first test of the strategy

    # Code looks for 10 strategies in test_c_wins before it stops the while loop
    while len(test_c_wins) <= 10:
        
        iterations += 1
        
        # Add the result of roulette() to first_test list      
        first_test.append(roulette(strategy))

        # Boolean conditions based on results it's getting
        winning = len(first_test) == 10 and first_test[9] <= first_test[0]
        losing = len(first_test) == 10 and first_test[9] >= first_test[0]

        if losing:
                first_test = []
                strategy = randomise_strategy()
                # DEBUG print(f'The new strategy is {strategy}')
                # DEBUG print('Strategy is losing. Randomising')

        if winning:
                # reset_bank()
                first_test=[]
                test_further_a(strategy)

    final_test()

def randomise_strategy():
            strategy = {
            'stake' : round(random.uniform(2,10),2),
            'target' : round(random.uniform(1.1,10),2),
            'stoploss' : round(random.uniform(0.2, 0.8),2),
            'bet_increase_lose' : round(random.uniform(2, 100),2),
            'bet_increase_win' : round(random.uniform(2,100),2),
            'reset_stake' : round(random.uniform(0,36),0),
            'bank' : 1000,
            }
            return strategy

def test_further_a(strategy):
    iterations = 0
    test_a = [1000]
    strategy['bank'] = 1000 # reset the bank to 1000 inside the strategy which was passed through
    # DEBUG print("Testing in test_further_a")

    while iterations <= 100 and strategy['bank'] >= 0:
        
        iterations += 1

        # Produce a result using the current strategy and add the result to test_b.
        test_a.append(roulette(strategy))

        # Boolean conditions based on results in test_a
        winning = len(test_a) == 100 and test_a[99] >= test_a[0]
        losing = len(test_a) == 100 and test_a[99] <= test_a[0]

        if winning:
            # DEBUG print("Strategy worked for 100 iterations.{}" .format(strategy))
            # DEBUG print("The results were {}" .format(test_a))
            # DEBUG print("Worked for 100 iterations. Test_a failed {} times before this" .format(fail_count))
            test_further_b(strategy)


        elif losing:
            break 

def test_further_b(strategy):
    iterations = 0
    test_b = [1000]
    strategy['bank'] = 1000  # reset the bank to 1000 inside the strategy which was pased through.
    # DEBUG print ("Testing in test_further_b")


    while iterations <= 1000:
        
        iterations += 1

        # Produce a result using the current strategy and add the result to test_b
        test_b.append(roulette(strategy))

        # boolen conditions based on results in test_b
        winning = len(test_b) == 1000 and test_b[999] >= test_b[0]
        losing = len(test_b) == 1000 and test_b[999] <= test_b[0]

        if winning:
             # print("IT WORKED for 1000 iterations! The bank started with {} and ended with {}" .format(test_b[0],test_b[999]))
             # print("The strategy was {}" .format(strategy))
             # print("Worked for 1000 iterations - test_B failed {} times before this" .format(fail_count))
            test_further_c(strategy)

        elif losing:
            break

def test_further_c(strategy):
    iterations = 0
    test_c=[1000]
    strategy['bank'] = 1000 
    print("Testing with test_further_c")


    while iterations <= 5000:
        
        iterations += 1

        # Add 1000 to test_c for starting amount then Produce a result using the current strategy and add the result to test_c
        # test_c.append(1000)
        test_c.append(roulette(strategy))

        # Boolean conditions based on results its getting
        winning = (len(test_c) == 5000) and (test_c[4999] >= test_c[0])
        losing = (len(test_c) == 5000) and (test_c[4999] <= test_c[0])
 
        if winning:
            print(f'FIVE THOUSAND ITERATIONS! The bank started with {test_c[0]} and ended with {test_c[-1]}')
            test_c_wins.append(strategy.copy())
            # test_further_d(strategy)
        elif losing:
            break

def test_further_d(strategy):
    iterations = 0
    test_d=[1000]
    strategy['bank'] = 1000 
    print("Testing with test_further_d")


    while iterations <= 10000:
        
        iterations += 1

        # Produce a result using the current strategy and add the result to test_c
        test_d.append(roulette(strategy))

        # Boolean conditions based on results its getting
        winning = (len(test_d) == 10000) and (test_d[9999] >= test_d[0])
        losing = (len(test_d) == 10000) and (test_d[9999] <= test_d[0])
 
        if winning:
            print(f'TEN THOUSAND ITERATIONS! The bank started with {test_d[0]} and ended with {test_d[-1]}')
            test_d_wins.append(strategy.copy())
        elif losing:
            break

def final_test():
    final_test_results = [1000]
    winning_strategy_list = []
    # DEBUG FOR DUMMY WINLIST list_of_ten = list(range(0,10))
    winning_strategy_results = [1000]

    # DEBUG TO CREATE DUMMY WINNING_STRATEGY_LIST
    # for i in list_of_ten:
    #     winning_strategy_list.append(randomise_strategy())

    for strategy in test_c_wins:

        while len(final_test_results) <= 10000000 or bank <= 400:
            final_test_results.append(roulette(strategy))

        else:
            print(f"Here's the strategy{strategy}")
            print("The strategy started with {} and ended with {}" .format(final_test_results[0],final_test_results[-1]))
            print("At one time, there was {} in the bank" .format(max(final_test_results)))
            if final_test_results[-1] >= final_test_results[0]:
                print('Crikey, that was working')
                winning_strategy_list.append(strategy) 
            final_test_results = [1000] 

    print(f'There are {len(winning_strategy_list)} strategies which seemed to be working. Testing indefinitely.')

    for win_strategies in winning_strategy_list:
        
        print(f'The strategy is {win_strategies}')
        print(f'The winning_strategy_results are {winning_strategy_results}')

        while winning_strategy_results[-1] >= 100:
            winning_strategy_results.append(roulette(win_strategies))

            if len(winning_strategy_results)%100000 == 0:
                print(f'{len(winning_strategy_results)} iterations passed. Bank is at {winning_strategy_results[-1]}')

            elif len(winning_strategy_results) >5000000 and len(set(winning_strategy_results)) <= 10:
                print('moving on - kept getting duplicate results')
                winning_strategy_results = [1000]
                continue

        else:
            print(f'The strategy was tested {len(winning_strategy_results)} times, it started with {winning_strategy_results[0]} and ended with {winning_strategy_results[-1]}')
            winning_strategy_results = [1000]

roulette_player()
print("All done!")

