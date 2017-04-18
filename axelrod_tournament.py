from axelrod import Player, Actions, init_args, Game, DeterministicCache
from flask_ask import Ask, statement, question
import axelrod.interaction_utils as iu
from flask import Flask
import axelrod as axl

app = Flask(__name__)
ask = Ask(app, '/')

C, D = Actions.C, Actions.D
PLAYERS = []
ROUNDS = 0


def update_history(player, move):
    """
    Updates histories and cooperation / defections counts following play.
    """
    # Update histories
    player.history.append(move)
    # Update player counts of cooperation and defection
    if move == C:
        player.cooperations += 1
    elif move == D:
        player.defections += 1

def update_state_distribution(player, action, reply):
    """
    Updates state_distribution following play.
    """
    last_turn = (action, reply)
    player.state_distribution[last_turn] += 1

class Alexa(Player):
    name = 'Alexa'

    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(['length', 'game']),
        'long_run_time': True,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @init_args
    def __init__(self, name='Alexa'):
        Player.__init__(self)
        self.name = name

    def strategy(self, opponent, choice):
        """
        This strategy should in theory work similar to human except for the amazon echo,
        so you will have to say whetherr you want to cooperate or defect.
        """
        action = choice
        return action

class Match(object):

    def __init__(self):
        global ROUNDS
        global PLAYERS
        self.result = []
        self.game = Game()
        self.turns = ROUNDS
        self.players = list(PLAYERS)
        self._cache = DeterministicCache()

    def final_score(self):
        """
        Returns the final score for a Match.
        """
        return iu.compute_final_score(self.result, self.game)

    def winner(self):
        """
        Returns the winner of the Match.
        """
        winner_index = iu.compute_winner_index(self.result, self.game)
        if winner_index is False:  # No winner
            return False
        if winner_index is None:  # No plays
            return None
        return self.players[winner_index]

    def _last_round_moves(self):
        move = self.players[1].history[-1]
        opp_move = self.players[0].history[-1]

        return move, opp_move

    def talk(self):
        round = len(self.players[0].history) + 1
        opp = self.players[0].name
        turns = self.turns

        if opp == '$\phi$':
            opp = 'phi'
        elif opp == '$\pi$':
            opp = 'pi'
        elif opp == '$e$':
            opp = 'e'

        if round == 1:
            msg = question("Starting a {} round match between you and {}.  Round 1, would you like to cooperate or defect?".format(turns, opp))
        elif round > 1 and round < turns:
            move, opp_move = self._last_round_moves()
            msg = question("In round {}, you played {}, {} played {}.  Round {}, would you like to cooperate or defect?".format(round - 1, move, opp, opp_move, round))
        elif round == turns:
            move, opp_move = self._last_round_moves()
            msg = question("In round {}, you played {}, {} played {}. Final round, would you like to cooperate or defect?".format(round - 1, move, opp, opp_move))
        elif round > turns:
            self.result = list(zip(self.players[0].history, self.players[1].history))
            score = self.final_score()
            winner = self.winner()

            if winner == False:
                msg = statement("End of match, you scored {}, and {} scored {}, meaning the match is a draw.".format(score[1], opp, score[0]))
            elif str(winner) == '$\phi$':
                msg = statement("End of match, you scored {}, and {} scored {}, meaning phi is the winner.".format(score[1], opp, score[0]))
            elif str(winner) == '$\pi$':
                msg = statement("End of match, you scored {}, and {} scored {}, meaning pi is the winner.".format(score[1], opp, score[0]))
            elif str(winner) == '$e$':
                msg = statement("End of match, you scored {}, and {} scored {}, meaning e is the winner.".format(score[1], opp, score[0]))
            else:
                msg = statement("End of match, you scored {}, and {} scored {}, meaning {} is the winner.".format(score[1], opp, score[0], winner))

        return msg

def which_strategy(opp):
    if opp == "adaptive":
        strategy = "Adaptive"
    elif opp == "adaptive tit for tat":
        strategy = "Adaptive Tit For Tat"
    elif opp == "aggravater":
        strategy = "Aggravater"
    elif opp == "allcoralld":
        strategy = "ALLCorALLD"
    elif opp == "alternator":
        strategy = "Alternator"
    elif opp == "alternator hunter":
        strategy = "Alternator Hunter"
    elif opp == "anticycler":
        strategy = "AntiCycler"
    elif opp == "anti tit for tat":
        strategy = "Anti Tit For Tat"
    elif opp == "adapative pavlov 2006":
        strategy = "Adapative Pavlov 2006"
    elif opp == "adapative pavlov 2011":
        strategy = "Adapative Pavlov 2011"
    elif opp == "appeaser":
        strategy = "Appeaser"
    elif opp == "arrogant qlearner":
        strategy = "Arrogant QLearner"
    elif opp == "average copier":
        strategy = "Average Copier"
    elif opp == "backstabber":
        strategy = "BackStabber"
    elif opp == "bully":
        strategy = "Bully"
    elif opp == "calculator":
        strategy = "Calculator"
    elif opp == "cautious qlearner":
        strategy = "Cautious QLearner"
    elif opp == "champion":
        strategy = "Champion"
    elif opp == "contrite tit for tat":
        strategy = "Contrite Tit For Tat"
    elif opp == "cooperator":
        strategy = "Cooperator"
    elif opp == "cooperator hunter":
        strategy = "Cooperator Hunter"
    elif opp == "cycle hunter":
        strategy = "Cycle Hunter"
    elif opp == "cycler cccccd":
        strategy = "Cycler CCCCCD"
    elif opp == "cycler cccd":
        strategy = "Cycler CCCD"
    elif opp == "cycler ccd":
        strategy = "Cycler CCD"
    elif opp == "cycler dc":
        strategy = "Cycler DC"
    elif opp == "cycler ddc":
        strategy = "Cycler DDC"
    elif opp == "cycler cccdcd":
        strategy = "Cycler CCCDCD"
    elif opp == "davis":
        strategy = "Davis"
    elif opp == "defector":
        strategy = "Defector"
    elif opp == "defector hunter":
        strategy = "Defector Hunter"
    elif opp == "desperate":
        strategy = "Desperate"
    elif opp == "doublecrosser":
        strategy = "DoubleCrosser"
    elif opp == "doubler":
        strategy = "Doubler"
    elif opp == "easygo":
        strategy = "EasyGo"
    elif opp == "eatherley":
        strategy = "Eatherley"
    elif opp == "eventual cycle hunter":
        strategy = "Eventual Cycle Hunter"
    elif opp == "evolvedann":
        strategy = "EvolvedANN"
    elif opp == "evolvedlookerup":
        strategy = "EvolvedLookerUp"
    elif opp == "feld":
        strategy = "Feld"
    elif opp == "firm but fair":
        strategy = "Firm But Fair"
    elif opp == "fool me forever":
        strategy = "Fool Me Forever"
    elif opp == "fool me once":
        strategy = "Fool Me Once"
    elif opp == "forgetful fool me once":
        strategy = "Forgetful Fool Me Once"
    elif opp == "forgetful grudger":
        strategy = "Forgetful Grudger"
    elif opp == "forgiver":
        strategy = "Forgiver"
    elif opp == "forgiving tit for tat":
        strategy = "Forgiving Tit For Tat"
    elif opp == "fortress3":
        strategy = "Fortress3"
    elif opp == "fortress4":
        strategy = "Fortress4"
    elif opp == "pso gambler":
        strategy = "PSO Gambler"
    elif opp == "gtft":
        strategy = "GTFT"
    elif opp == "go by marjority":
        strategy = "Go By Marjority"
    elif opp == "go by majority 10":
        strategy = "Go By Majority 10"
    elif opp == "go by majority 20":
        strategy = "Go By Majority 20"
    elif opp == "go by majority 40":
        strategy = "Go By Majority 40"
    elif opp == "go by majority 5":
        strategy = "Go By Majority 5"
    elif opp == "phi":
        strategy = "$\phi$"
    elif opp == "gradual":
        strategy = "Gradual"
    elif opp == "gradual killer":
        strategy = "Gradual Killer"
    elif opp == "grofman":
        strategy = "Grofman"
    elif opp == "grudger":
        strategy = "Grudger"
    elif opp == "grudgeralternator":
        strategy = "GrudgerAlternator"
    elif opp == "grumpy":
        strategy = "Grumpy"
    elif opp == "handshake":
        strategy = "Handshake"
    elif opp == "hard go by majority":
        strategy = "Hard Go By Majority"
    elif opp == "hard go by majority 10":
        strategy = "Hard Go By Majority 10"
    elif opp == "hard go by majority 20":
        strategy = "Hard Go By Majority 20"
    elif opp == "hard go by majority 40":
        strategy = "Hard Go By Majority 40"
    elif opp == "hard go by majority 5":
        strategy = "Hard Go By Majority 5"
    elif opp == "hard prober":
        strategy = "Hard Prober"
    elif opp == "hard tit for 2 tats":
        strategy = "Hard Tit For 2 Tats"
    elif opp == "hard tit for tat":
        strategy = "Hard Tit For Tat"
    elif opp == "hesitant qlearner":
        strategy = "Hesitant QLearner"
    elif opp == "hopeless":
        strategy = "Hopeless"
    elif opp == "inverse":
        strategy = "Inverse"
    elif opp == "inverse punisher":
        strategy = "Inverse Punisher"
    elif opp == "joss":
        strategy = "Joss"
    elif opp == "knowledgeable worse and worse":
        strategy = "Knowledgeable Worse and Worse"
    elif opp == "limited retaliate":
        strategy = "Limited Retaliate"
    elif opp == "limited retaliate 2":
        strategy = "Limited Retaliate 2"
    elif opp == "limited retaliate 3":
        strategy = "Limited Retaliate 3"
    elif opp == "math constant hunter":
        strategy = "Math Constant Hunter"
    elif opp == "naive prober":
        strategy = "Naive Prober"
    elif opp == "negation":
        strategy = "Negation"
    elif opp == "nice average copier":
        strategy = "Nice Average Copier"
    elif opp == "nydegger":
        strategy = "Nydegger"
    elif opp == "omega tft":
        strategy = "Omega TFT"
    elif opp == "once bitten":
        strategy = "Once Bitten"
    elif opp == "opposite grudger":
        strategy = "Opposite Grudger"
    elif opp == "pi":
        strategy = "$\pi$"
    elif opp == "predator":
        strategy = "Predator"
    elif opp == "prober":
        strategy = "Prober"
    elif opp == "prober 2":
        strategy = "Prober 2"
    elif opp == "prober 3":
        strategy = "Prober 3"
    elif opp == "prober 4":
        strategy = "Prober 4"
    elif opp == "punisher":
        strategy = "Punisher"
    elif opp == "raider":
        strategy = "Raider"
    elif opp == "random":
        strategy = "Random"
    elif opp == "random hunter":
        strategy = "Random Hunter"
    elif opp == "remorseful prober":
        strategy = "Remorseful Prober"
    elif opp == "retaliate":
        strategy = "Retaliate"
    elif opp == "retaliate 2":
        strategy = "Retaliate 2"
    elif opp == "retaliate 3":
        strategy = "Retaliate 3"
    elif opp == "ripoff":
        strategy = "Ripoff"
    elif opp == "risky qlearner":
        strategy = "Risky QLearner"
    elif opp == "shubik":
        strategy = "Shubik"
    elif opp == "slow tit for two tats":
        strategy = "Slow Tit For Two Tats"
    elif opp == "sneaky tit for tat":
        strategy = "Sneaky Tit For Tat"
    elif opp == "soft grudger":
        strategy = "Soft Grudger"
    elif opp == "soft joss":
        strategy = "Soft Joss"
    elif opp == "solutionb1":
        strategy = "SolutionB1"
    elif opp == "solutionb5":
        strategy = "SolutionB5"
    elif opp == "spiteful tit for tat":
        strategy = "Spiteful Tit For Tat"
    elif opp == "stochastic cooperator":
        strategy = "Stochastic Cooperator"
    elif opp == "stochastic wsls":
        strategy = "Stochastic WSLS"
    elif opp == "suspicious tit for tat":
        strategy = "Suspicious Tit For Tat"
    elif opp == "thuemorse":
        strategy = "ThueMorse"
    elif opp == "thuemorseinverse":
        strategy = "ThueMorseInverse"
    elif opp == "thumper":
        strategy = "Thumper"
    elif opp == "tit for tat":
        strategy = "Tit For Tat"
    elif opp == "tit for 2 tats":
        strategy = "Tit For 2 Tats"
    elif opp == "tricky cooperator":
        strategy = "Tricky Cooperator"
    elif opp == "tricky defector":
        strategy = "Tricky Defector"
    elif opp == "tullock":
        strategy = "Tullock"
    elif opp == "two tits for tat":
        strategy = "Two Tits For Tat"
    elif opp == "willing":
        strategy = "Willing"
    elif opp == "win-shift lose-stay":
        strategy = "Win-Shift Lose-Stay"
    elif opp == "win-stay lose-shift":
        strategy = "Win-Stay Lose-Shift"
    elif opp == "worse and worse":
        strategy = "Worse and Worse"
    elif opp == "zd-extort-2":
        strategy = "ZD-Extort-2"
    elif opp == "zd-extort-2 v2":
        strategy = "ZD-Extort-2 v2"
    elif opp == "zd-extort-4":
        strategy = "ZD-Extort-4"
    elif opp == "zd-gtft-2":
        strategy = "ZD-GTFT-2"
    elif opp == "zd-gen-2":
        strategy = "ZD-GEN-2"
    elif opp == "zd-set-2":
        strategy = "ZD-SET-2"
    elif opp == "e":
        strategy = "$e$"
    elif opp == "meta hunter":
        strategy = "Meta Hunter"
    elif opp == "meta majority":
        strategy = "Meta Majority"
    elif opp == "meta minority":
        strategy = "Meta Minority"
    elif opp == "meta winner":
        strategy = "Meta Winner"
    elif opp == "meta majority memory one":
        strategy = "Meta Majority Memory One"
    elif opp == "meta winner memory one":
        strategy = "Meta Winner Memory One"
    elif opp == "meta majority finite memory":
        strategy = "Meta Majority Finite Memory"
    elif opp == "meta winner finite memory":
        strategy = "Meta Winner Finite Memory"
    elif opp == "meta majority long memory":
        strategy = "Meta Majority Long Memory"
    elif opp == "meta winner long memory":
        strategy = "Meta Winner Long Memory"
    elif opp == "meta mixer":
        strategy = "Meta Mixer"
    elif opp == "meta winner ensemble":
        strategy = "Meta Winner Ensemble"

    return strategy

@ask.launch
def welcome():
    welcome_msg = 'Welcome to the Axelrod tournament, what would you like to do?'
    return question(welcome_msg)

@ask.intent("PlayIntent")
def play_intent(Rounds, Strategy):
    you = Alexa(name='you')
    strategy = which_strategy(Strategy)
    opp = axl.strategies[[s.name for s in axl.strategies].index(strategy)]()

    global PLAYERS
    PLAYERS = []
    PLAYERS.append(opp)
    PLAYERS.append(you)

    global ROUNDS
    ROUNDS += int(Rounds)

    for player in PLAYERS:
        player.set_match_attributes(length=ROUNDS, game=Game(), noise=0)

    return Match().talk()

@ask.intent("ChoiceIntent")
def choice_intent(self, Choice):
    if Choice == 'defect':
        choice = D
    elif Choice == 'cooperate':
        choice = C

    global PLAYERS
    global ROUNDS
    if len(PLAYERS[0].history) == 0 or len(PLAYERS[0].history) > ROUNDS:
        for p in PLAYERS:
            p.reset()

    s1, s2 = PLAYERS[0].strategy(PLAYERS[1]), PLAYERS[1].strategy(PLAYERS[0], choice)

    update_history(PLAYERS[0], s1)
    update_history(PLAYERS[1], s2)
    update_state_distribution(PLAYERS[0], s1, s2)
    update_state_distribution(PLAYERS[1], s2, s1)

    return Match().talk()

@ask.intent("AMAZON.HelpIntent")
def help_intent():
    help_msg = "Using this skill you are able to start a 2 player match against one of 149 different strategies in the Axelrod library. You define how many rounds you want to go for, who you want to challenge, then tell me to cooperate or defect when it is your turn. Why not give a 3 round game against tit for tat a go, or if your feeling adventurous try a 23 round game against EvolvedANN."
    return statement(help_msg)

@ask.intent("AMAZON.StopIntent")
def stop_intent():
    stop_msg = "This is not the skill you are after... Carry on."
    return statement(stop_msg)

@ask.intent("AMAZON.CancelIntent")
def cancel_intent():
    cancel_msg = "This is not the skill you are after... Carry on"
    return statement(cancel_msg)

if __name__ == '__main__':
    app.run()
