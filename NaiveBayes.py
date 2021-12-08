from sklearn.naive_bayes import CategoricalNB

class NB:

    ''' Constructor
        inputs: (optional) training_data - 
        output: None
    '''
    def __init__(self, training_data:list=[]) -> None:
        self.training_data = training_data
        # variables used for probability calculations
        self.price_decrease_counter = {}
        self.price_stagnant_counter = {}
        self.price_increase_counter = {}
        self.decrease_sum = 0
        self.stagnant_sum = 0
        self.increase_sum = 0

        self.decrease_prob = {}
        self.stagnant_prob = {}
        self.increase_prob = {}
        
        if (training_data != []):   # automatically train if given training data    
            self.train([])
        
        return


    ''' reset - resets NB training
        inputs: None
        outputs: None
        side effects: clears old training data in NB
    '''
    def reset(self) -> None:
        self.training_data = []
        self.price_decrease_counter = {}
        self.price_stagnant_counter = {}
        self.price_increase_counter = {}
        self.decrease_sum = 0
        self.stagnant_sum = 0
        self.increase_sum = 0
        self.decrease_prob = {}
        self.stagnant_prob = {}
        self.increase_prob = {}
        return


    ''' train - 
        inputs: training_data - [ (float<social data>, float<price change>), ... ]
        output: None
    '''
    def train(self, new_training_data:list) -> None:
        print("Training Naive Bayes")
        laplace = 0.01  # laplace smoothing variable
        self.training_data += new_training_data

        # add social data to counters for price deltas
        for data in new_training_data:
            social = data[0]
            price = data[1]
            if price < 0:    # price decrease
                if social in self.price_decrease_counter:
                    self.price_decrease_counter[social] += 1
                else:
                    self.price_decrease_counter[social] = 1
                self.decrease_sum += 1
            elif price == 0:   # stagnant price
                if social in self.price_stagnant_counter:
                    self.price_stagnant_counter[social] += 1
                else:
                    self.price_stagnant_counter[social] = 1
                self.stagnant_sum += 1
            else:   # price increase
                if social in self.price_increase_counter:
                    self.price_increase_counter[social] += 1
                else:
                    self.price_increase_counter[social] = 1
                self.increase_sum += 1

        # calculate probability of price delta given social data
        for soc in self.price_decrease_counter:
            self.decrease_prob[soc] = (self.price_decrease_counter[soc]+laplace)/(self.decrease_sum+laplace*3)
        for soc in self.price_stagnant_counter:
            self.stagnant_prob[soc] = (self.price_stagnant_counter[soc]+laplace)/(self.stagnant_sum+laplace*3)
        for soc in self.price_increase_counter:
            self.increase_prob[soc] = (self.price_increase_counter[soc]+laplace)/(self.increase_sum+laplace*3)

        return


    ''' predict - 
        inputs: test_data - 
        output: +1 for predicted increase in price
                0 for perdicted stagnant price
                -1 for predicted decrease in price
        side effects: adds test_data to training_data for future predictions
    '''
    def predict(self, test_data:list) -> int:
        self.training_data += test_data

        return self.test_predict(test_data)

    
    ''' test_predict - predict without adding test_data to training_data
        inputs: test_data - 
        output: +1 for predicted increase in price
                0 for perdicted stagnant price
                -1 for predicted decrease in price
    '''
    def test_predict(self, test_data:list) -> int:

        return 0
