#----------------------------------------------------
#               COMP9021 
#               Assignment 3
#           Written by Chunnan Sheng
#           Student Code z5100764
#----------------------------------------------------
import sys
import re

#-----------------------------------------------------------------
#    A Claim records a statement of a Sir
#    In this statement, other Sirs (including himself) may be mentioned.
#    Names of Sirs mentioned are recorded in self.sir_names
#    The claimed Job is also recorded.
#    For example:
#        Sir D said: "Sir A, Sir B, Sir C and I are Knights."
#    Then A, B, C and D are recorded in self.sir_names.
#    And self.job = 1 (1 represents Knight and 0 represents Knave) because
#    'Knight' is mentioned in Sir D's statement
#-----------------------------------------------------------------
class Claim:
    def __init__(self, text):
        self.text = text
        self.claim_type = None
        self.sir_names = None
        self.job = None

#----------------------------------------------------------------
#    A Sir who is a Knight or a Knave
#    One Sir may include one claim, multiple claims or no claim
#----------------------------------------------------------------
class Sir:        
    
    def __init__(self, name):  
        self.name = name
        self.claims = []
    
    def new_claim(self, claim):
        self.claims.append(claim)

#---------------------------------------------------------                  
#    This class reads puzzle file, extract useful information.
#    Data extracted will be recorded as a collection of Sirs.
#    Each Sir may have no claims, one claim or multiple claims.
#---------------------------------------------------------                  
class PuzzleFile:
    #----------------------------------------------------- 
    #     Regular expression of sirs' claims:
    #-----------------------------------------------------
    # At/at least one of Conjunction_of_Sirs/us is a Knight/Knave
    at_least_one_of_them = '^[\s]*[aA]t[\s]+least[\s]+one[\s]+of[\s]+(.*[^\s])[\s]+is[\s]+a[\s]+([^,.!?\s]*)'
    
    # At/at most one of Conjunction_of_Sirs/us is a Knight/Knave
    at_most_one_of_them = '^[\s]*[aA]t[\s]+most[\s]+one[\s]+of[\s]+(.*[^\s])[\s]+is[\s]+a[\s]+([^,.!?\s]*)'
        
    # Exactly/exactly one of Conjunction_of_Sirs/us is a Knight/Knave
    one_of_them = '^[\s]*[eE]xactly[\s]+one[\s]+of[\s]+(.*[^\s])[\s]+is[\s]+a[\s]+([^,.!?\s]*)'
    
    # All/all of us are Knights/Knaves
    all_of_them = '^[\s]*[aA]ll[\s]+of[\s]+(.*[^\s])[\s]+are[\s]+([^,.!?\s]*)'
    
    # I am a Knight/Knave
    i_am = '^[\s]*(.*[^\s])[\s]+am[\s]+a[\s]+([^,.!?\s]*)'
    
    # Sir Sir_Name is a Knight/Knave
    he_is = '^[\s]*Sir[\s]+([^,.!?\s]*)[\s]+is[\s]+a[\s]+([^,.!?\s]*)'
    
    # Disjunction_of_Sirs is a Knight/Knave
    a_or_b_is = '^[\s]*(.*[\s]+or[\s]+.*[^\s])[\s]+is[\s]+a[\s]+([^,.!?\s]*)'
    
    # Conjunction_of_Sirs are Knights/Knaves
    a_and_b_are = '^[\s]*(.*[\s]+and[\s]+.*[^\s])[\s]+are[\s]+([^,.!?\s]*)'
        
    #----------------------------------------------------------
    #    Initialization of this class
    #    And extract data of Sirs from puzzle file
    #----------------------------------------------------------
    def __init__(self, file_name):
        text = self._read_file(file_name)
        self.all_claim_types = self._initialize_claim_types()
        self.all_sirs = self._decode(text)
        
    #----------------------------------------------------------
    #    Read puzzle text from puzzle file
    #----------------------------------------------------------
    def _read_file(self, file_name):
        text = None
        try:
            with open(file_name, 'r') as my_file:
                str_text = my_file.read()
                text = list(str_text)
                    
        except IOError:
            print('Can not open puzzle file.')
            sys.exit()
            
        return text
        
    #----------------------------------------------------------------------
    #   Initialize enumerations of regular expressions of claim types
    #----------------------------------------------------------------------
    def _initialize_claim_types(self):
              
        all_claim_types = []
        all_claim_types.append(PuzzleFile.at_least_one_of_them)
        all_claim_types.append(PuzzleFile.at_most_one_of_them)
        all_claim_types.append(PuzzleFile.one_of_them)
        all_claim_types.append(PuzzleFile.all_of_them)
        all_claim_types.append(PuzzleFile.i_am)
        all_claim_types.append(PuzzleFile.he_is)
        all_claim_types.append(PuzzleFile.a_or_b_is)
        all_claim_types.append(PuzzleFile.a_and_b_are)
        
        return all_claim_types
        
    
    #----------------------------------------------------------------------
    #   Print all information of sirs (For debug)
    #----------------------------------------------------------------------
    def print_all_sirs(self):
        for (sir_name, sir) in sorted(self.all_sirs.items()):
            print('Sir: {}'.format(sir_name))
            for claim in sir.claims:
                print('    {}'.format(claim.text))
                #print('    {}'.format(claim.claim_type))
                #print('    {}'.format(claim.sir_names))
                #print('    {}'.format(claim.job))
        
    
    #----------------------------------------------------------------------
    #   Decode puzzle text into data that is suitable for calculation
    #----------------------------------------------------------------------
    def _decode(self, text):
    
        # First step: Decode puzzle file into sentences and quotes
        sentences = self._text_into_sentences(text)
        
        '''
        for (sent, quote) in sentences:
            print('Sentence: {}'.format(''.join(sent)))
            if not (quote is None):
                print('Quote: {}'.format(''.join(quote)))
            print('')
        '''
        
        # Second step: Decode sentences and quotes into Sirs and Claims
        return self._sentences_into_sirs(sentences)



    #-----------------------------------------------------
    #     Map puzzle text into multiple sentences
    #     If there is quote, get it out of this sentence
    #-----------------------------------------------------
    def _text_into_sentences(self, text):
        sentences = []
        sent = []
        quote = []
        in_sentence = False
        in_quote = False
        for ele in text:
            if ele in {'\n', '\r', '\t'}:
                ele = ' '
            
            if (not in_sentence) and (not in_quote):
                if ele == '\"':
                    in_sentence = True
                    in_quote = True
                    sent.append(ele)
                    
                elif (ord(ele) >= 48 and ord(ele) <= 57) or \
                    (ord(ele) >= 65 and ord(ele) <= 90) or \
                    (ord(ele) >= 97 and ord(ele) <= 122):
                    in_sentence = True
                    sent.append(ele)
                    
                else:
                    pass
                    
            elif in_sentence and (not in_quote):
                if ele in {'.', '!', '?'}:
                    sent.append(ele)
                    sentences.append((sent, quote))
                    sent = []
                    quote = []
                    in_sentence = False
                    
                elif ele == '\"':
                    in_quote = True
                    sent.append(ele)
                    
                else:
                    sent.append(ele)
                    
            elif in_sentence and in_quote:
                if ele in {'.', '!', '?'}:
                    quote.append(ele)
                    in_sentence = False
                    
                elif ele == '\"':
                    sent.append(ele)
                    in_quote = False
                else:
                    quote.append(ele)
            else:
                if ele == '"':
                    sent.append(ele)
                    sentences.append((sent, quote))
                    sent = []
                    quote = []
                    in_quote = False
                    
                else:
                    print('Invalid syntax in puzzle file, program will exit')
                    sys.exit()
                    
        return sentences

    
    #-----------------------------------------------------
    #     Map multiple sentences into collection of Sirs
    #     Each Sir includes: 
    #     1. Sir name
    #     2. Claims(speaking) of this Sir
    #     3. Other Sirs mentioned in his speaking
    #-----------------------------------------------------
    def _sentences_into_sirs(self, sentences):
        all_sirs = {}
        for (sent, quote) in sentences:
            #There is no quote in this sentence
            if len(quote) == 0:
                sir_names = self._decode_sentence_without_quote(sent)
                for sir_name in sir_names:
                    if not (sir_name in all_sirs):
                        all_sirs[sir_name] = Sir(sir_name)
            else:
                (sir_name, quote) = self._decode_sentence_with_quote(sent, quote)
                    
                if not (sir_name in all_sirs):
                    all_sirs[sir_name] = Sir(sir_name)
                
                the_sir = all_sirs[sir_name]
                
                new_claim = self._decode_quote_and_generate_claim(quote, the_sir, all_sirs)                
                the_sir.new_claim(new_claim)

        for (s_name, sir) in all_sirs.items():
            for claim in sir.claims:
                if claim.sir_names == 'us':
                    claim.sir_names = list(all_sirs.keys())
                
        return all_sirs


    #--------------------------------------------------------------
    #     Extract Sir information from a sentence without quote
    #--------------------------------------------------------------
    def _decode_sentence_without_quote(self, sent):
        sir_names = []
        
        words = []
        receiver = []
        for ele in sent:
            if ele in {' ', '\t', ',', '.', '\"', '!', '?', ':'}:
                if len(receiver) > 0:
                    words.append(''.join(receiver))
                    receiver = []
            else:
                receiver.append(ele)
                
        in_sir_statement = False
        one_sir = False
        after_and = False
        
        for word in words:
            if not in_sir_statement:
                if word == 'Sir':
                    in_sir_statement = True
                    one_sir = True
                    after_and = False
                elif word == 'Sirs':
                    in_sir_statement = True
                    one_sir = False
                    after_and = False
                else:
                    pass
            elif one_sir:
                sir_names.append(word)
                in_sir_statement = False
                one_sir = False
                after_and = False
                
            elif not after_and:
                if word == 'and':
                    after_and = True
                else:
                    sir_names.append(word)
            else:
                sir_names.append(word)
                in_sir_statement = False
                one_sir = False
                after_and = False
        
        #print('--------------')
        #for sir_name in sir_names:
        #    print(sir_name)
        #print('--------------')
            
        return sir_names    

    #----------------------------------------------------------------------   
    #    Extract a sir and his claim from a sentence with quote
    #----------------------------------------------------------------------
    def _decode_sentence_with_quote(self, sent, quote):
        sir_names = self._decode_sentence_without_quote(sent)
        
        if len(sir_names) != 1:
            print(sir_names)
            print('Sentence with quote should include ONE Sir name outside quote, program will exit')
            sys.exit()
        
        sir_name = sir_names[0]
        
        return (sir_name, quote)
        
        
    #--------------------------------------------------------------------------------
    #       Analyse quote and generate suitable claim data for calculation
    #       This process may add new Sir if there is new Sir mentioned in quote
    #--------------------------------------------------------------------------------
    def _decode_quote_and_generate_claim(self, quote, me, all_sirs):
        
        claim_text = ''.join(quote)
        
        match = 0
        the_claim_type = None
        
        # self.all_claim_types includes all regular expressions that a sir may speak
        # go through all regular expressions to find out suitable one
        for claim_type in self.all_claim_types:
            match = re.search(claim_type, claim_text)
            if match:
                the_claim_type = claim_type
                break
        
        # If there is no match of regular expression
        # Something is probably wrong
        if not match:
            print('Invalid human speaking in puzzle file, program will exit')
            sys.exit();
        
        sir_names_text = match.group(1)
        str_job = match.group(2)
            
        sir_names = self._decode_to_sir_names(sir_names_text, me, all_sirs)
        job = self._decode_to_boolean(str_job)
        
        claim = Claim(claim_text)
        claim.claim_type = the_claim_type
        claim.sir_names = sir_names
        claim.job = job
        
        return claim

    
    #-----------------------------------------------------------------
    #    Extract Sir names from Sir name expression extracted from quote
    #    This expression maybe like:
    #    1. Sir name1, Sir name2 and Sir name3
    #    2. Sir name1 or Sir name2
    #    3. Sir name1, Sir name2, Sir name3 and I
    #    4. Sir name1, Sir name2 or I
    #    5. I
    #    6. us
    #-----------------------------------------------------------------
    def _decode_to_sir_names(self, sir_names_text, me, all_sirs):
        sir_names = []
        words = []
        receiver = []
        
        if sir_names_text == 'us':
            sir_names = 'us'
            return sir_names
            
        char_list = list(sir_names_text)
        
        for ele in char_list:
            if ele in {' ', '\t', ','}:
                if len(receiver) > 0:
                    words.append(''.join(receiver))
                    receiver = []
            else:
                receiver.append(ele)
                
        if len(receiver) > 0:
            words.append(''.join(receiver))
        
        for word in words:
            if not (word in {'I', 'and', 'or', 'Sir', 'Sirs'}):
                sir_names.append(word)
            elif word == 'I':
                sir_names.append(me.name)
         
        for sir_name in sir_names:
            if not sir_name in all_sirs:
                all_sirs[sir_name] = Sir(sir_name)
                
        return sir_names
        
    
    #--------------------------------------------------------------------
    #     Decode jobs into digits
    #     'Knight' or 'Knights' into 1
    #     'Knave' or 'Kaves' into 0   
    #--------------------------------------------------------------------
    def _decode_to_boolean(self, job):
        if job in {'Knight', 'Knights'}:
            return 1
        elif job in {'Knave', 'Knaves'}:
            return 0
        else:
            print('Neither Knight nor Knave is found, program will exit')
            print(job)
            sys.exit();
            
#--------------------------------------------------------------
#    This class is used to represent a solution of a Sir
#--------------------------------------------------------------
class SolutionSir:
    def __init__(self, name):
        self.name = name
        self.job = None
        
#----------------------------------------------------------
#    This class represent a candidate solution
#    Each candidate solution includes all Sirs with possible job values
#    For example:
#    SirA SirB SirC SirD SirE
#     0    1    0    0    1
#----------------------------------------------------------        
class Solution:
    def __init__(self, all_sir_names):
        self.correct = True
        self.answers = {}
        for sir_name in all_sir_names:
            self.answers[sir_name] = SolutionSir(sir_name)

            
#----------------------------------------------------------
#    This class figures out answers of Knight Knave puzzle
#    With Sir data as input
#----------------------------------------------------------
class PuzzleCalulator:
    def __init__(self, all_sirs):
        self.all_sirs = all_sirs
        self.all_sir_names = []
        for (sir_name, sir) in self.all_sirs.items():
            self.all_sir_names.append(sir.name)
        
        self.candidate_solutions = self._generate_all_solutions()

    
    #-------------------------------------------------------------------
    #    Generate all candidate solutions
    #    If there are 3 Sirs, then all candidate solutions would be:
    #    SirA SirB SirC
    #     0    0    0
    #     0    0    1
    #     0    1    0
    #     0    1    1
    #     1    0    0
    #     1    0    1
    #     1    1    0
    #     1    1    1
    #-------------------------------------------------------------------
    def _generate_all_solutions(self):
        solutions = {}
        length = len(self.all_sir_names)
        amount = pow(2, length)
        for i in range(1, amount + 1):
            solutions[i] = Solution(self.all_sir_names)
            j = i
            for sir_name in self.all_sir_names:
                digit = j % 2
                j = j // 2
                solutions[i].answers[sir_name].job = digit
                solutions[i].answers[sir_name].job = digit
        
        return solutions
        
    
    #-------------------------------------------------------------------
    #     Deal with logic of 'At least one of them'
    #     Delete the candidate solution if there is paradox
    #-------------------------------------------------------------------
    def _deal_with_at_least_one_of_them(self, teller, claim):
        claimed_sir_names = claim.sir_names
        claimed_job = claim.job
        
        solutions_to_delete = []
        for (i, solution) in self.candidate_solutions.items():
            
            found = False
            for sir_name in claimed_sir_names:
                if solution.answers[sir_name].job == claimed_job:
                    found = True
                    break
            # In this assumed solution, the teller is a Knight
            # He tells the truth
            # So, at least one of claimed Sirs has this job
            if solution.answers[teller].job == 1:
                if not found:
                # If there is no one having this job, paradox happens
                    solutions_to_delete.append(i)
            # In this assumed solution, the teller is a Knave
            # He lies
            # So, none of claimed Sirs have this job
            else:
                if found:
                # If there is anyone holding this job, paradox happens
                    solutions_to_delete.append(i)
        
        for i in solutions_to_delete:
            del self.candidate_solutions[i]


    #-------------------------------------------------------------------
    #     Deal with logic of 'At most one of them'
    #     Delete the candidate solution if there is paradox
    #------------------------------------------------------------------- 
    def _deal_with_at_most_one_of_them(self, teller, claim):
        claimed_sir_names = claim.sir_names
        claimed_job = claim.job
        
        solutions_to_delete = []
        # Iterate all candidate solutions
        for (i, solution) in self.candidate_solutions.items():
            
            sum = 0
            # Iterate all Sirs on behalf of one solution
            for sir_name in claimed_sir_names:
                if solution.answers[sir_name].job == claimed_job:
                    sum += 1
                    if sum > 1:
                        break
            # In this assumed solution, the teller is a Knight
            # He tells the truth
            # So, at most one of claimed Sirs has this job
            if solution.answers[teller].job == 1:
                if sum > 1:
                # If there more than one having this job, paradox happens
                    solutions_to_delete.append(i)
            # In this assumed solution, the teller is a Knave
            # He lies
            # So, more than one Sirs have this job
            else:
                if sum <= 1:
                # If there is at most one Sir this job, paradox happens
                    solutions_to_delete.append(i)
        
        for i in solutions_to_delete:
            del self.candidate_solutions[i]
   
   
    #-------------------------------------------------------------------
    #     Deal with logic of 'One of them'
    #     Delete the candidate solution if there is paradox
    #------------------------------------------------------------------- 
    def _deal_with_one_of_them(self, teller, claim):
        claimed_sir_names = claim.sir_names
        claimed_job = claim.job
        
        solutions_to_delete = []
        for (i, solution) in self.candidate_solutions.items():
            
            sum = 0
            for sir_name in claimed_sir_names:
                if solution.answers[sir_name].job == claimed_job:
                    sum += 1
                    if sum > 1:
                        break
            # In this assumed solution, the teller is a Knight
            # He tells the truth
            # So, exactly one of claimed Sirs has this job
            if solution.answers[teller].job == 1:
                if sum != 1:
                # If number of Sirs having this job is not 1, paradox happens
                    solutions_to_delete.append(i)
            # In this assumed solution, the teller is a Knave
            # He lies
            # So, number of Sirs having this job should not be 1
            else:
                if sum == 1:
                # If there is anyone having this job, paradox happens
                    solutions_to_delete.append(i)
        
        for i in solutions_to_delete:
            del self.candidate_solutions[i]
            
 
    #-------------------------------------------------------------------
    #     Deal with logic of 'All of them'
    #     Delete the candidate solution if there is paradox
    #------------------------------------------------------------------- 
    def _deal_with_all_of_them(self, teller, claim):
        claimed_sir_names = claim.sir_names
        claimed_job = claim.job
        
        solutions_to_delete = []
        for (i, solution) in self.candidate_solutions.items():
            
            exception_found = False
            for sir_name in claimed_sir_names:
                if solution.answers[sir_name].job != claimed_job:
                    exception_found = True
                    break
            # In this assumed solution, the teller is a Knight
            # He tells the truth
            # So, all of claimed Sirs have this job
            if solution.answers[teller].job == 1:
                if exception_found:
                # If there is anybody who does not have this job, paradox happens
                    solutions_to_delete.append(i)
            # In this assumed solution, the teller is a Knave
            # He lies
            # So, there should be somebody who does not have this job
            else:
                if not exception_found:
                # If all of those Sir have this job, paradox happens
                    solutions_to_delete.append(i)
        
        for i in solutions_to_delete:
            del self.candidate_solutions[i]
    
    
    #-------------------------------------------------------------------
    #    Go through Claims of a Sir
    #    Each claim may decrease amount of candidate solutions
    #------------------------------------------------------------------- 
    def _deal_with_sir(self, sir):
        #print(sir.name)
        for claim in sir.claims:
                    
            if claim.claim_type == PuzzleFile.at_least_one_of_them:
                self._deal_with_at_least_one_of_them(sir.name, claim)
                
            elif claim.claim_type == PuzzleFile.at_most_one_of_them:
                self._deal_with_at_most_one_of_them(sir.name, claim)
                
            elif claim.claim_type == PuzzleFile.one_of_them:
                self._deal_with_one_of_them(sir.name, claim)
                
            elif claim.claim_type == PuzzleFile.all_of_them:
                self._deal_with_all_of_them(sir.name, claim)
                
            elif claim.claim_type == PuzzleFile.i_am:
                self._deal_with_all_of_them(sir.name, claim)
                
            elif claim.claim_type == PuzzleFile.he_is:
                self._deal_with_all_of_them(sir.name, claim)
                
            elif claim.claim_type == PuzzleFile.a_or_b_is:
                self._deal_with_at_least_one_of_them(sir.name, claim)
                
            elif claim.claim_type == PuzzleFile.a_and_b_are:
                self._deal_with_all_of_them(sir.name, claim)
            
            #print(claim.text)
            #print(len(self.candidate_solutions))

                
    #-------------------------------------------------------------------
    #    The calculation goes through all Sirs
    #    Each Sir may decrease amount of candidate solutions
    #------------------------------------------------------------------- 
    def calculate(self):
        for (sir_name, sir) in self.all_sirs.items():
            self._deal_with_sir(sir)


    #-------------------------------------------------------------------
    #    Print all solutions
    #    This method is for debug
    #------------------------------------------------------------------- 
    def print_all_solutions(self):
        for (i, solution) in self.candidate_solutions.items():
            for (sir_name, sir) in sorted(solution.answers.items()):
                print('{}: {}'.format(sir_name, sir.job), end = ' ')
            print('')


    #-------------------------------------------------------------------
    #    Print all Sir names for Assignment 3
    #------------------------------------------------------------------- 
    def print_sirs_ass3_format(self):
        print('The Sirs are: ', end = '')
        for sir_name in sorted(self.all_sirs.keys()):
            print(sir_name, end = ' ')
        print('')


    #-------------------------------------------------------------------
    #    Print solutions of Assignment 3 format
    #------------------------------------------------------------------- 
    def print_solutions_ass3_format(self):
        if 0 == len(self.candidate_solutions):
            print('There is no solution.')
            
        elif 1 == len(self.candidate_solutions):
            print('There is a unique solution:')
            for (i, solution) in self.candidate_solutions.items():
                for (sir_name, sir) in sorted(solution.answers.items()):
                    job = 'Knight'
                    if 0 == sir.job:
                        job = 'Knave'
                    print('Sir {} is a {}.'.format(sir_name, job))
        else:
            print('There are {} solutions.'.format(len(self.candidate_solutions)))
                    
    
            
if __name__ == '__main__':
    
    file_name = input('Which text file do you want to use for the puzzle? ')
    
    puzzle_file = PuzzleFile(file_name)
    #puzzle_file.print_all_sirs()
    
    calculator = PuzzleCalulator(puzzle_file.all_sirs)
    calculator.calculate()
    #calculator.print_all_solutions()
    
    #print('')
    #print('')
    calculator.print_sirs_ass3_format()
    calculator.print_solutions_ass3_format()
    
    
            
            
            
            
            
            
            