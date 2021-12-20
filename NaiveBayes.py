import math
from sklearn.naive_bayes import CategoricalNB
from sklearn.naive_bayes import GaussianNB

class NB:
    ''' Methods:
    reset() - resets NB training
    train(new_training_data) - trains NB with social data & price deltas
    predict(test_data) - predict price direction
    cnb_train(new_training_data) - train a CategoricalNB from sklearn package
    cnb_predict(test_data) - price direction prediction by CategoricalNB
    gnb_train(new_training_data) - train a GaussianNB from sklearn package
    gnb_predict(test_data) - price direction prediction by GaussianNB
    full_suite(new_training_data, test_data) - trains all 3 NB models on new_training_data
                                                and returns predictions for test_data
    '''

    ''' Constructor
        inputs: (optional) training_data - [ (float<social data>, float<price change>), ... ]
                            -> list of tuples
        output: None
    '''
    def __init__(self, training_data:list=[]) -> None:
        self.reset()
        self.training_data = training_data
        
        if (training_data != []):   # automatically train if given training data    
            self.train([])
        
        return


    ''' reset - resets NB training
        inputs: None
        outputs: None
        side effects: clears old training data in NB
    '''
    def reset(self) -> None:
        print("Resetting NB")
        self.training_data = []
        # variables used for probability calculations
        self._price_decrease_counter = {}
        self._price_stagnant_counter = {}
        self._price_increase_counter = {}
        self._decrease_sum = 0
        self._stagnant_sum = 0
        self._increase_sum = 0
        self._dec_UNK = 0
        self._stag_UNK = 0
        self._inc_UNK = 0
        # probabilities used in predictions
        self.decrease_prob = {}
        self.stagnant_prob = {}
        self.increase_prob = {}

        # variables used in sklearn NB functions
        self._cnb = CategoricalNB()
        self._gnb = GaussianNB()

        return


    ''' train - trains NB with social data & price deltas
        inputs: new_training_data - [ (float<social data>, float<price change>), ... ]
                    -> list of tuples
        output: None
        notes: does NOT clear old training data -> adds to existing training
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
                if social in self._price_decrease_counter:
                    self._price_decrease_counter[social] += 1
                else:
                    self._price_decrease_counter[social] = 1
                self._decrease_sum += 1
            elif price == 0:   # stagnant price
                if social in self._price_stagnant_counter:
                    self._price_stagnant_counter[social] += 1
                else:
                    self._price_stagnant_counter[social] = 1
                self._stagnant_sum += 1
            else:   # price increase
                if social in self._price_increase_counter:
                    self._price_increase_counter[social] += 1
                else:
                    self._price_increase_counter[social] = 1
                self._increase_sum += 1

        # calculate probabilities of price delta given social data
        for soc in self._price_decrease_counter:
            self.decrease_prob[soc] = (self._price_decrease_counter[soc]+laplace)/(self._decrease_sum+laplace*4)
        for soc in self._price_stagnant_counter:
            self.stagnant_prob[soc] = (self._price_stagnant_counter[soc]+laplace)/(self._stagnant_sum+laplace*4)
        for soc in self._price_increase_counter:
            self.increase_prob[soc] = (self._price_increase_counter[soc]+laplace)/(self._increase_sum+laplace*4)
        
        # probabilities for unknown social data values
        self._dec_UNK = laplace / (self._decrease_sum + laplace*4)
        self._stag_UNK = laplace / (self._stagnant_sum + laplace*4)
        self._inc_UNK = laplace / (self._increase_sum + laplace*4)

        return


    ''' predict - predict price direction
        inputs: test_data - list of social data: [float<social data>, ...]
        output: list of ints (each int corresponding to test data set):
                +1 for predicted increase in price
                0 for perdicted stagnant price
                -1 for predicted decrease in price
    '''
    def predict(self, test_data:list, log:bool=True) -> list:
        print("Predicting Price Direction")
        # prior probabilities
        prior_prob_dec = self._decrease_sum / (self._decrease_sum+self._stagnant_sum+self._increase_sum)
        prior_prob_stag = self._stagnant_sum / (self._decrease_sum+self._stagnant_sum+self._increase_sum)
        prior_prob_inc = self._increase_sum / (self._decrease_sum+self._stagnant_sum+self._increase_sum)
        prob_dec = (prior_prob_dec)
        prob_stag = (prior_prob_stag)
        prob_inc = (prior_prob_inc)

        price_predictions = []

        # calculate price direction probabilities for social data
        for social in test_data:
            prob_dec = self._log(prior_prob_dec, log)
            prob_stag = self._log(prior_prob_stag, log)
            prob_inc = self._log(prior_prob_inc, log)
            if social in self.decrease_prob:
                prob_dec += self._log(self.decrease_prob[social], log)
            else:
                prob_dec += self._log(self._dec_UNK, log)
            if social in self.stagnant_prob:
                prob_stag += self._log(self.stagnant_prob[social], log)
            else:
                prob_stag += self._log(self._stag_UNK, log)
            if social in self.increase_prob:
                prob_inc += self._log(self.increase_prob[social], log)
            else:
                prob_inc += self._log(self._inc_UNK, log)
            
            # find max probability for price direction
            if prob_dec == prob_inc:    # rare case of equal decrease & increase probabilities
                price_predictions.append(0) # return stagnant
            else:
                probs = [prob_dec, prob_stag, prob_inc]
                price_predictions.append((probs.index(max(probs))) - 1)

        return price_predictions
    

    ''' _log - static method for taking log of input if bool value is set
        inputs: input - value to take or not take log of
                log - boolean value indicating whether or not to take log
        outputs: log of input if log, else input
    '''
    @staticmethod
    def _log(input:float, log:bool) -> float:
        if log:
            return math.log(input)
        else:
            return input


    ''' cnb_train - train a CategoricalNB from sklearn package
        inputs: new_training_data - [ (float<social data>, float<price change>), ... ]
                    -> list of tuples
        output: None
        notes: does NOT clear old training data in CNB -> adds to existing training
    '''
    def cnb_train(self, new_training_data:list) -> None:
        print("Training CategoricalNB")
        social_samples = []
        price_classes = []

        for data in new_training_data:
            social_samples.append([data[0]])
            price = data[1]
            if price < 0:    # price decrease
                price_classes.append(-1)
            elif price == 0:   # stagnant price
                price_classes.append(0)
            else:   # price increase
                price_classes.append(1)
        # fit data in CNB (partial fit for adding new data, fit for first time training)
        try:
            self._cnb.partial_fit(social_samples, price_classes)
        except ValueError:
            self._cnb.fit(social_samples, price_classes)

        return


    ''' cnb_predict - price direction prediction by CategoricalNB
    inputs: test_data - list of social data: [float<social data>, ...]
    output: list of ints (each int corresponding to test data set):
            +1 for predicted increase in price
            0 for perdicted stagnant price
            -1 for predicted decrease in price
    '''
    def cnb_predict(self, test_data:list) -> list:
        print("CategoricalNB Prediction")
        price_predictions = []

        for social in test_data:
            try:
                price_predictions.append(self._cnb.predict([[social]])[0])
            except IndexError:
                price_predictions.append(self._cnb.predict([[len(self._cnb.category_count_)-1]])[0])

        return price_predictions


    ''' gnb_train - train a GaussianNB from sklearn package
    inputs: new_training_data - [ (float<social data>, float<price change>), ... ]
                -> list of tuples
    output: None
    notes: does NOT clear old training data in GNB -> adds to existing training
    '''
    def gnb_train(self, new_training_data:list) -> None:
        print("Training GaussianNB")
        social_samples = []
        price_classes = []

        for data in new_training_data:
            social_samples.append([data[0]])
            price = data[1]
            if price < 0:    # price decrease
                price_classes.append(-1)
            elif price == 0:   # stagnant price
                price_classes.append(0)
            else:   # price increase
                price_classes.append(1)
        # fit data in GNB (partial fit for adding new data, fit for first time training)
        try:
            self._gnb.partial_fit(social_samples, price_classes)
        except ValueError:
            self._gnb.fit(social_samples, price_classes)

        return


    ''' gnb_predict - price direction prediction by GaussianNB
    inputs: test_data - list of social data: [float<social data>, ...]
    output: list of ints (each int corresponding to test data set):
            +1 for predicted increase in price
            0 for perdicted stagnant price
            -1 for predicted decrease in price
    '''
    def gnb_predict(self, test_data:list) -> list:
        print("GaussianNB Prediction")
        price_predictions = []
        social_samples = []

        for social in test_data:
            social_samples.append([social])
        price_predictions = list(self._gnb.predict(social_samples))

        return price_predictions


    ''' full_suite - trains all 3 NB models on new_training_data and returns predictions for test_data
        inputs: new_training_data - [ (float<social data>, float<price change>), ... ]
                -> list of tuples
                test_data - list of social data: [float<social data>, ...]
        outputs: tuple of lists:
                    list of ints (each int corresponding to test data set):
                        +1 for predicted increase in price
                        0 for perdicted stagnant price
                        -1 for predicted decrease in price
        side effects: resets all training data
    '''
    def full_suite(self, new_training_data:list, test_data:list, log:bool=True) -> tuple:
        self.reset()
        self.train(new_training_data)
        self.cnb_train(new_training_data)
        self.gnb_train(new_training_data)
        return self.predict(test_data, log), self.cnb_predict(test_data), self.gnb_predict(test_data)
