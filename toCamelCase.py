#!/usr/bin/env python
#
# Task: Given a string such as 'i'm feeling lucky', convert to camelcase (all
# but first letter of word capitalized. Ex: 'i'm Feeling Lucky'. 


def toCamelCase(string_input):
  # Split the string so that we can operate on each word individually.
  string_input = string_input.split()
  
  # A counter is needed because duplicated phrases such as 'I'm i'm' will not
  # camel case properly.
  index = 0
  
  # Loop through the list of words and lowercase the first one, but capitalize
  # the others.
  for word in string_input:
    if index > 0:
      string_input[index] = word.capitalize()
      index += 1
    else:
      string_input[index] = string_input[index].lower()
      index += 1
  
  # Finally, join it back into a string to be printed/returned.
  string_input = ' '.join(string_input)

  print 'string_input: %s' % string_input


if __name__ == '__main__':
  print 'Enter string to camel case:\n'
  toCamelCase(raw_input())

