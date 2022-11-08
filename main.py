from random import choices
import re

class MarkovChain:


  def __init__(self, evaluator='single'): # Enter the evaluator type to decide whether it will use the single or double evaluation pattern.

    self.markov = dict() # Initialize Markov Chain Dictionary

    evaluators = ['single', 'double'] # Valid Evaluator types

    if evaluator not in evaluators: # If the evaluator type isn't valid raise a ValueError.
      raise ValueError(f"""Invalid evaluator type. Expected one of these types: "{'", "'.join(evaluators)}".""")
    else: self.evaluator = evaluator # Else set the evaluator to the parameters.



  def evaluate_sentence(self, input_text): # Enter input text to add to the evaluation model of the markov chain.

    input_text = "".join([char for char in input_text if char.isalpha() or char == " "]).lower() # Remove non alpha characters from input text.
    input_arr = input_text.split(" ") # Convert input text into an array.

    if self.evaluator == 'single': # If evaluator type is single.

      for key in (key for key in input_arr if key not in self.markov): # For every unique word in the input text that is not already in the chain.
        self.markov[key] = dict() # Set every new key to a blank dict.

      for i in range(len(input_arr)): # Evaluation.
        try:
          if input_arr[i+1] in list(self.markov[input_arr[i]].keys()):
            self.markov[input_arr[i]][input_arr[i+1]] += 1
          else:
            self.markov[input_arr[i]][input_arr[i+1]] = 1
        except IndexError: break

    elif self.evaluator == 'double': # If evaluator type is double.
      try:
        for key in (f'{input_arr[i]} {input_arr[i+1]}' for i in range(len(input_arr)) if f'{input_arr[i]} {input_arr[i+1]}' not in self.markov): # For every unique word in the input text that is not already in the chain.
          self.markov[key] = dict() # Set every new key to a blank dict.
      except IndexError: pass

      for i in range(len(input_arr)): # Evaluation.
        try:
          if input_arr[i+2] in list(self.markov[f'{input_arr[i]} {input_arr[i+1]}'].keys()):
            self.markov[f'{input_arr[i]} {input_arr[i+1]}'][input_arr[i+2]] += 1
          else:
            self.markov[f'{input_arr[i]} {input_arr[i+1]}'][input_arr[i+2]] = 1
        except IndexError: break
    
    self.keys = list(self.markov.keys()) # Set self.keys equal to a list of all learned chain keys.



  def evaluate_paragraph(self, input_text):
    for sentence in re.split(".?;.!", input_text): # For every sentence in the input parameters split by any punctuation mark, evaluate.
      self.evaluate_sentence(sentence)



  def generate_sentence(self, start=None, max_length=10, forced_restart=False):
    if type(max_length) is not int: # If max_length isn't integer, raise ValueError
      raise ValueError(f"""Invalid value {max_length} for max_length. Only integers are accepted.""")

    if type(forced_restart) is not bool: # If forced_restart isn't boolean, raise ValueError
      raise ValueError(f"""Invalid value {forced_restart} for forced_restart. Valid values are True and False.""")

    if start is None: # If start was not specified, choose a random start from chain keys. If start is not in the chain keys, raise ValueError
      start = choices(list(self.markov.keys()), [sum(self.markov[key].values()) for key in self.markov.keys()], k=1)[0]
    elif start not in list(self.markov.keys()): 
      raise ValueError(f"""Invalid value {start} for start key. Valid start key are stored in self.keys.""")
    
    output_text = start # Begin output_text with the start key.

    for i in range(max_length): # Repeat for max_length words.

      if self.evaluator == 'single': current_word = output_text.split(" ")[-1] # If evaluator is type 'single' set current_word equal to the last word.
      elif self.evaluator == 'double': current_word = " ".join(output_text.split(" ")[-2:]) # If evaluator is type 'double' set current_word equal to the last two words.
      else: raise ValueError(f"""Invalid value {self.evaluator} for self.evaluator. Valid evaluators include: 'single' and 'double'.""") # Raise ValueError
      
      if self.markov[current_word] == dict() and forced_restart is False: break
      elif self.markov[current_word] == dict() and forced_restart is True:
        output_text += " " + choices(list(self.markov.keys()), [sum(self.markov[key].values()) for key in self.markov.keys()], k=1)[0] # Output random next word based on usage (keys).
      else:
        output_text += " " + choices(list(self.markov[current_word].keys()), list(self.markov[current_word].values()), k=1)[0] # Output random next word based on usage.
  
    return output_text.capitalize() + "."


      
# Example usage of the Markov Chain class.
if __name__ == "__main__":
  mc = MarkovChain(evaluator='double')
  mc.evaluate_sentence("Hello there how are you my friends?")
  mc.evaluate_paragraph("Hello, i am having a nice day with my friends. What do you like to do with your friends. I like to go to the park with my friends sometimes and talk about life.")
  print(mc.generate_sentence(forced_restart=True, max_length=25))
