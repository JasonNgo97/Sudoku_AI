from __future__ import print_function
from game import sd_domain,sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random, copy

import pdb
class AI:
    def __init__(self):
        pass


    def solve(self, problem):
        domains = init_domains()
        restrict_domain(domains, problem) 
        back_track_stack = []
        # TODO: implement backtracking search.
        while True:
            result = self.propagate(problem,domains)
            if result:
                # You have found your solution
                if self.all_values_assigned(domains):
                    #print("Problem is completed")
                    clean_domain = self.clean_domain(domains)
                    return clean_domain
                # Make a decision and then propagate everything
                else:
                    domain_copy = copy.deepcopy(domains)
                    var,val = self.make_decision(problem,domains)
                    back_track_stack.append((domain_copy,var,val))
                    domains[var] = [val] # Here, we apply the decision
            # This corresponds to an error
            else:
                # There is no solution
                if len(back_track_stack) == 0:
                    return None
                # Restore the old domain with this decision removed aka backtracking
                else:
                    old_domain,var,val = back_track_stack.pop()
                    old_domain[var].remove(val)
                    domains = old_domain
        return None
        # TODO: delete this block ->
        # Note that the display and test functions in the main file take domains as inputs. 
        #   So when returning the final solution, make sure to take your assignment function
        #   and turn the value into a single element list and return them as a domain map. 
        #for spot in sd_spots:
        #    domains[spot] = [1]
        #return domains
        # <- TODO: delete this block

    def propagate(self,problem,domain):
        domain_change = True

        # This keeps iterating until there is no element with only singleton
        while domain_change:
            domain_change = False # Reset the domain change
            for item in domain.items():
                spot = item[0]
                spot_list = item[1]
                if type(spot_list) == list: # Singleton
                    if len(spot_list) == 1:
                        value = spot_list[0]
                        conflict = self.remove_value_from_peer(value,spot,domain)
                        if conflict:
                            return False
                        else:
                            domain[spot] = value
                            domain_change = True
        return True

    def remove_value_from_peer(self,value,var,domain):
        conflict_col = self.remove_value_from_column(value,var,domain)
        if conflict_col:
            return True
        conflict_row = self.remove_value_from_row(value,var,domain)
        if conflict_row:
            return True
        conflict_square = self.remove_value_from_square(value,var,domain)
        if conflict_square:
            return True
        # There is no conflict
        return False

    def remove_value_from_row(self,value,var,domain):
        # Here, we fix the column
        row_comp = var[0]
        # Iterate through the row
        for j in range(SD_SIZE):
            elem_comp = (row_comp,j)
            if j != var[1]: # Make sure you don't hit the same element
                elem_list = domain[elem_comp]
                if type(elem_list) == list:
                    # Value matches
                    if value in elem_list:
                        domain[elem_comp].remove(value)
                        if len(domain[elem_comp]) == 0:
                            return True
        return False

    def remove_value_from_column(self,value,var,domain):
        # Here, we fix the column
        col_comp = var[1]
        # Iterate through the column
        for i in range(SD_SIZE):
            elem_comp = (i,col_comp)
            if i != var[0]: #Make sure you don't hit the same element
                elem_list = domain[elem_comp]
                if type(elem_list) == list: # This is not assigned value
                    # Value matches
                    if value in elem_list:
                        domain[elem_comp].remove(value)
                        if len(domain[elem_comp]) == 0:
                            return True
        return False

    def remove_value_from_square(self,value,var,domain):
        # Note that you can't remove the same row and column
        row_start = int(var[0]/SD_DIM)*SD_DIM
        col_start = int(var[1]/SD_DIM)*SD_DIM
        # Here, your indices are off
        for i in range(row_start,row_start+SD_DIM):  # Iterate through row
            for j in range(col_start,col_start+SD_DIM):  # Iterate through column
                if i != var[0] and j != var[1]:
                    elem_list = domain[(i,j)]
                    if type(elem_list) == list: # This is not singleton
                        if value in elem_list:
                            domain[(i,j)].remove(value)
                            if len(domain[(i,j)]) == 0:
                                return True

        return False



    def not_arc_consistent(self,var1,var2,domain):
        # Check that they are peers
        if self.peer(var1,var2,domain):
            domain_1 = domain[var1]
            domain_2 = domain[var2]
            # Case if domain 1 is singleton
            if len(domain_1) == 1:
                if domain_1[0] in domain_2:
                    return True
                else:
                    return False
            # Case if domain 2 is singleton
            elif len(domain_2) == 1:
                if domain_2[0] in domain_1:
                    return True
                else:
                    return False
            else:
                return False
        # Not peers, so not applicable
        else:
            return False

    def peer(self,var1,var2,domain):
        if var1 == var2:  # Missing the first condition
            return False
        elif var1[0] == var2[0]:  # Check row
            return True
        elif var1[1] == var2[1]:  # Check column
            return True
        elif self.in_same_square(var1,var2,domain):   # Check if in same square
            return True
        else:
            return False


    def in_same_square(self,var1,var2,domain,square_size=3):
        if int(var1[0]/square_size) != int(var2[0]/square_size): # Check with division on row
            return False

        elif int(var1[1]/square_size) != int(var2[1]/square_size): # Check with division on column
            return False
        else:
            return True

    def all_values_assigned(self,domain):
        #Iterate through value of dictionary
        for item in domain.items():
            value = item[1]
            if type(value) == list:
            #if len(value) > 1 or len(value) == 0:  # Here, a decision hasn't been made
                return False
        # All decisions has been made
        return True


    def make_decision(self,problem,domain):
        # First check that there are no other element with singleton
        # Then pick the element with the least number of options
        min_length = 50  # This is the sentinel value to be reset
        min_var = None
        # Iterate through domain
        for item in domain.items():
            var = item[0]
            if type(item[1]) == list:
                decision_length = len(item[1])
                # We try to find the element in domain where least amount of decision
                if decision_length < min_length and decision_length > 1:
                    min_var = var
                    min_length = decision_length
        # Determine the decision
        decision = (domain[min_var])[0]
        return min_var,decision

    def clean_domain(self,domain):
        for item in domain.items():
            var = item[0]
            decision = item[1]
            domain[var] = [decision]
        return domain

    def print_domain_dict(self,domain):
        for item in domain.items():
           print("Item: ",item)
        return domain

    # TODO: add any supporting function you need





    #### The following templates are only useful for the EC part #####

    # EC: parses "problem" into a SAT problem
    # of input form to the program 'picoSAT';
    # returns a string usable as input to picoSAT
    # (do not write to file)
    def sat_encode(self, problem):
        text = ""

        # TODO: write CNF specifications to 'text'

        return text

    # EC: takes as input the dictionary mapping 
    # from variables to T/F assignments solved for by picoSAT;
    # returns a domain dictionary of the same form 
    # as returned by solve()
    def sat_decode(self, assignments):
        # TODO: decode 'assignments' into domains
        
        # TODO: delete this ->
        domains = {}
        for spot in sd_spots:
            domains[spot] = [1]
        return domains
        # <- TODO: delete this
