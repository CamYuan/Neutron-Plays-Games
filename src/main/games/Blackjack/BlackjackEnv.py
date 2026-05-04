import gymnasium as gym
from gymnasium import spaces
from games.Blackjack import Card, Hand, Player, Table 
import numpy as np


class BlackjackEnv(gym.Env):
  metadata = {'render_modes': ['human'], 'render_fps': 1}
  def __init__(self, render_mode=None):
    self.reset()
    # [stand, hit, double down, split]
    self.action_space = spaces.Discrete(4)
    
    self.observation_space = spaces.Box(0, 1, shape=(2,)) #??? TODO
    
    self.table: Table = Table()
    self.player: Player = Player('Goddard', autobet=True)
  
  def reset(self, seed=None, options=None):
    super().reset(seed=seed)

    self.table.__reset()
    self.player.__reset()
    self.hands = self.table.initializeRound([self.player]) #1
    self.table.deal(self.hands) #2
    self.table.checkBlackjacks(self.hands)
    
    # self.playHands(self.hands)
    # self.removeBustHands(self.hands)
    # #Hands will get cleared when there is a blackjack or bust. 
    # #If it's a dead hand, dealer doesn't take cards for no reason
    # if(len(self.hands) > 0): 
    #   self.dealerHand.dealer = False #expose the dealer hand
    #   self.playDealerHand()
    #   self.calculateScoresAndPayout(hands)
    # self.reset()    

    self.render()
    
    return self._getObservation(), {} #info = {} since I'm not using it
  
  def step(self, action):
    pass
    return observation, reward, terminated, truncated, info
  def render(self):
    if(self.render_mode == None):
      return
    if(self.render_mode == "terminal"):
      ...
      
  def _getObservation(self):
    dealerCard: Card = self.table.getDealerUpCard()
    dealerSoftScore = dealerCard.getSoftValue()
    dealerHardScore = dealerCard.getHardValue()
    playerHand: Hand = self.hands[0]
    playerSoftScore = playerHand.getSoftScore()
    playerHardScore = playerHand.getHardScore()
    return np.array([ dealerSoftScore, dealerHardScore, playerSoftScore, playerHardScore])
    pass
  
  def action_masks(self): 
    pass
      
  
def checkMyEnv():
    from gymnasium.utils.env_checker import check_env
    env = gym.make('Blackjack-v0', render_mode='terminal')
    check_env(env.unwrapped)
  
def doubleCheckMyEnv():
    # from gymnasium.utils.env_checker import check_env
    # env = gym.make('Blackjack-v0', render_mode='terminal')
    # check_env(env.unwrapped)
    #TODO
    ...
    
if __name__ == "__main__":
  ##Uncomment to check env
  checkMyEnv()

  
  