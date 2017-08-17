#liar puzzle generator

from random import seed, randint, choice, sample, randrange
import sys



class PuzzleGenerator:

    def __init__ (self, the_seed, number_of_sirs, number_of_claims):
        if number_of_sirs > 30:
            print('Number of sirs should not be larger than 30, program will exit.')
            sys.exit()
            
        if number_of_claims > number_of_sirs:
            print('Number of claims should not be larger than number of sirs, program will exit.')
            sys.exit()
            
        seed(the_seed)
        
        self.seed = the_seed
        self.all_names = self._read_all_names()
        self.names = sample(self.all_names, number_of_sirs)
        self.names_mentioned = []
        
        self.splitters = [' ', ',']
        self.full_stops = ['.', '?', '!']
        
        self.claims = self._generate_claims(number_of_claims)
        self.number_of_claims = number_of_claims
        
        for (claim, name) in self.claims:
            print(name)
            print(claim)



    def generate_sentences(self):
        all_random_sentence_functions = []
        all_random_sentence_functions.append(self._generate_random_sentence_with_sir_name_and_claim)
        all_random_sentence_functions.append(self._generate_random_sentence)
        all_random_sentence_functions.append(self._generate_random_sentence_with_sir_names)

        sentences = []
        
        while len(self.claims) > 0:
            func = choice(all_random_sentence_functions)
            sentence = func()
            sentences.append(sentence)
        
        #--------------------------------------------------------------------------------------------
        letters = list(''.join(sentences))
        
        new_letters = []
        punc = {'.', ':', ',', '!', '?'}
        
        for i in range(len(letters)):
            new_letters.append(letters[i])
            if letters[i] in punc:
                if ((i + 1) < len(letters)) and letters[i + 1] != ' ' and letters[i + 1] != '\"':
                    new_letters.append(' ')
                    
        for i in range(len(new_letters)):
            if new_letters[i] == ' ' and (randint(0, 1) == 0):
                new_letters[i] = '\n'
                
        
        output = ''.join(new_letters)
        
        file_name = 'puzzle_{}_{}_{}.txt'.format(self.seed, len(self.names), self.number_of_claims)
        try:
            with open(file_name, 'w') as file:
                file.write(output)
                    
        except IOError:
            print('Can not open name resouce.')
            sys.exit()
        
        
        
    def _read_all_names(self):
        sir_names = []
        try:
            with open('names.txt', 'r') as name_file:
                str_lines = name_file.readlines()
                
                for str_line in str_lines:
                    words = str_line.split()
                    sir_names.append(words[0])
                    
        except IOError:
            print('Can not open name resouce.')
            sys.exit()
            
        return sir_names
        

        
    
    def print_sir_names(self):
        print(self.names)
      

    def _generate_random_sentence_with_sir_name_and_claim(self):
        
        sentence = []
        
        if len(self.claims) > 0:
            #print(len(self.claims))
            (claim, name) = choice(self.claims)
            self.claims.remove((claim, name))
            #print(name)
            #print(claim)
            
            name_pos = randint(0, 1)
        
            if name_pos == 0:
                sentence.append(self._generate_random_sentence_part_with_sir_name(name))
            else:
                sentence.append(self._generate_random_sentence_part())
                
            sentence.append(": ")
            
            sentence.append('\"')
            sentence.append(claim)

            if name_pos == 0:
                sentence.append(choice(self.full_stops))
            else:
                sentence.append(',')
            
            sentence.append('\"')
            sentence.append(' ')
               
            if not name_pos == 0:
                sentence.append(self._generate_random_sentence_part_with_sir_name(name))
                sentence.append(choice(self.full_stops))
    
        
        return ''.join(sentence)
                    
        
        
    
    def _generate_random_sentence(self):
        
        sentence = []
        
        capital_letter = chr(randint(65, 90))
        number_of_words = randint(1, 20)
        
        for i in range(number_of_words):
            word_len = randint(1, 20)
            word = []
            for j in range(word_len):
                if i == 0 and j == 0:
                    word.append(capital_letter)
                else:
                    word.append(chr(randint(97, 122)))
                    
            sentence.append(''.join(word))
            
            if i < number_of_words - 1:
                sentence.append(choice(self.splitters))
            else:
                sentence.append(choice(self.full_stops))
               
        
        return ''.join(sentence)
        
    
    
    
    def _generate_random_sentence_with_sir_names(self):
        
        sentence = []
        sentence.append(self._generate_random_sentence_part())
        sentence.append(choice(self.splitters))
        
        number = randint(1, len(self.names))
        
        if number == 1:
            sentence.append('Sir ')
        else:
            sentence.append('Sirs ')
        
        sir_names = []
        for sir_name in self.names:
            sir_names.append(sir_name)

        for i in range(number):
            sir_name = choice(sir_names)
            sir_names.remove(sir_name)
            
            if i == number - 1 and i != 0:
                sentence.append(' and ' )
            elif i > 0:
                sentence.append(', ')
                
            sentence.append(sir_name)
            
        sentence.append(choice(self.splitters))
        sentence.append(self._generate_random_sentence_part())
        sentence.append(choice(self.full_stops))
        
        return ''.join(sentence)


        
  
    def _generate_random_sentence_part(self):
        
        sentence = []
        
        capital_letter = chr(randint(65, 90))
        number_of_words = randint(0, 10)
        
        for i in range(number_of_words):
            word_len = randint(1, 20)
            word = []
            for j in range(word_len):
                if i == 0 and j == 0:
                    word.append(capital_letter)
                else:
                    word.append(chr(randint(97, 122)))
                    
            sentence.append(''.join(word))
            
            if i < number_of_words - 1:
                sentence.append(choice(self.splitters))
        
        return ''.join(sentence)
        
        
    
    def _generate_random_sentence_part_with_sir_name(self, name):
        
        sentence = []
        
        capital_letter = chr(randint(65, 90))
        number_of_words = randint(1, 10) 
        name_pos = randrange(0, number_of_words)
        
        for i in range(number_of_words):
            word_len = randint(1, 20)
            word = []
            
            if i == name_pos:
                sentence.append('Sir ')
                sentence.append(name)
            else:
                for j in range(word_len):
                    if i == 0 and j == 0:
                        word.append(capital_letter)
                    else:
                        word.append(chr(randint(97, 122)))
                        
                sentence.append(''.join(word))

            if i < number_of_words - 1:
                sentence.append(choice(self.splitters))
        
        return ''.join(sentence)
        

    
    
    def _generate_conjunction_of_sirs(self, number, name):
        
        conjunction = []

        sir_names = []
        for sir_name in self.names:
            sir_names.append(sir_name)
            
        for i in range(number):
            sir_name = choice(sir_names)
            sir_names.remove(sir_name)
            
            if i == number - 1 and i != 0:
                conjunction.append(' and ' )
            elif i > 0:
                conjunction.append(', ')
                
            if sir_name == name:
                conjunction.append('I')
            else:
                conjunction.append('Sir ')
                conjunction.append(sir_name)
                
        return ''.join(conjunction)




    def _generate_disjunction_of_sirs(self, number, name):
    
        disjunction = []

        sir_names = []
        for sir_name in self.names:
            sir_names.append(sir_name)
            
        for i in range(number):
            sir_name = choice(sir_names)
            sir_names.remove(sir_name)
            
            if i == number - 1 and i != 0:
                disjunction.append(' or ' )
            elif i > 0:
                disjunction.append(', ')
                
            if sir_name == name:
                disjunction.append('I')
            else:
                disjunction.append('Sir ')
                disjunction.append(sir_name)
                
        return ''.join(disjunction)
   



    def _generate_at_least_one_of_claim(self, name):
        #At/at least one of Conjunction_of_Sirs/us is a Knight/Knave
        claim = []
        
        a_or_A = randint(0, 1)
        
        if a_or_A == 0:
            claim.append('at least one of ')
        else:
            claim.append('At least one of ')
        
        number = randint(2, len(self.names))
        if number == len(self.names):
            claim.append('us ')
        else:
            claim.append(self._generate_conjunction_of_sirs(number, name))
        
        jobs = ['Knight', 'Knave']
        
        claim.append(' is a ')
        claim.append(choice(jobs))
        
        return ''.join(claim)
        
        
        
    
    def _generate_at_most_one_of_claim(self, name):
        #At/at most one of Conjunction_of_Sirs/us is a Knight/Knave
        claim = []
        
        a_or_A = randint(0, 1)
        
        if a_or_A == 0:
            claim.append('at most one of ')
        else:
            claim.append('At most one of ')
        
        number = randint(2, len(self.names))
        if number == len(self.names):
            claim.append('us ')
        else:
            claim.append(self._generate_conjunction_of_sirs(number, name))
        
        jobs = ['Knight', 'Knave']
        
        claim.append(' is a ')
        claim.append(choice(jobs))
        
        return ''.join(claim)

        
    
    def _generate_exactly_one_of_claim(self, name):
        #Exactly/exactly one of Conjunction_of_Sirs/us is a Knight/Knave
        claim = []
        
        e_or_E = randint(0, 1)
        
        if e_or_E == 0:
            claim.append('exactly one of ')
        else:
            claim.append('Exactly one of ')
        
        number = randint(2, len(self.names))
        if number == len(self.names):
            claim.append('us ')
        else:
            claim.append(self._generate_conjunction_of_sirs(number, name))
        
        jobs = ['Knight', 'Knave']
        
        claim.append(' is a ')
        claim.append(choice(jobs))
        
        return ''.join(claim)
        
        
        
        
    def _generate_all_of_us_claim(self, name):
        #All/all of us are Knights/Knaves
        claim = []
        a_or_A = randint(0, 1)
        
        if a_or_A == 0:
            claim.append('all of us are ')
        else:
            claim.append('All of us are ')
        
        jobs = ['Knights', 'Knaves']
        claim.append(choice(jobs))
        
        return ''.join(claim)
        
        
        
    def _generate_one_is_claim(self, name):
        #Sir Sir_Name is a Knight/Knave
        claim = []
        
        sir_name = choice(self.names)
        if name == sir_name:
            claim.append('I am a ')
        else:
            claim.append('Sir ')
            claim.append(sir_name)
            claim.append(' is a ')
        
        jobs = ['Knight', 'Knave']

        claim.append(choice(jobs))

        return ''.join(claim)
        
        
        
    def _generate_one_of_them_claim(self, name):
        #Disjunction_of_Sirs is a Knight/Knave
        claim = []
        claim.append(self._generate_disjunction_of_sirs(randint(2, len(self.names)), name))
        
        jobs = ['Knight', 'Knave']
        
        claim.append(' is a ')
        claim.append(choice(jobs))
        
        return ''.join(claim)
        
        
        
    def _generate_all_of_them_claim(self, name):
        #Conjunction_of_Sirs are Knights/Knaves
        claim = []
        claim.append(self._generate_conjunction_of_sirs(randint(2, len(self.names)), name))
        
        jobs = ['Knights', 'Knaves']
        
        claim.append(' are ')
        claim.append(choice(jobs))
        
        return ''.join(claim)
        
        
        
    def _generate_claims(self, number_of_claims):
        all_claim_func = []
        all_claim_func.append(self._generate_at_least_one_of_claim)
        all_claim_func.append(self._generate_at_most_one_of_claim)
        all_claim_func.append(self._generate_exactly_one_of_claim)
        all_claim_func.append(self._generate_all_of_us_claim)
        all_claim_func.append(self._generate_one_is_claim)
        all_claim_func.append(self._generate_one_of_them_claim)
        all_claim_func.append(self._generate_all_of_them_claim)
        
        names = []
        claims = []
        for name in self.names:
            names.append(name)
            
        for i in range(number_of_claims):
            
            claim_func = choice(all_claim_func)
            
            name = choice(names)
            #names.remove(name)
            
            claims.append((claim_func(name), name))
        
        return claims
        
            
        
if __name__ == '__main__':

    the_seed = int(sys.argv[1])
    number_of_sirs = int(sys.argv[2])
    number_of_claims = int(sys.argv[3])
    
    generator = PuzzleGenerator(the_seed, number_of_sirs, number_of_claims)
    generator.print_sir_names()
    generator.generate_sentences()
    

