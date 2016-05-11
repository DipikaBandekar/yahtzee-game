# Automatic Zacate game player
# B551 Fall 2015
# Dipika Bandekar, dipiband
#
# Based on skeleton code by D. Crandall
#
# REPORT:
#1)Tried dividing the 13 turns into open_list, middle list and final_list
#2)Open list: used for 1st 4 turns where 13-9 categories are available
#--> tries to fill the first six categories in order to get bonus
#--> uses smart approach to retain the elements if count >= 2 in first roll and rerolls the other dices
#For instance if [6,6,1,2,3] retain 6 and rolls [1,2,3]
# --> open list also focusses on frijol and quesa and tries to get that configuration
#--> it assigns to category tamal only if sum>22
#--> if no category is obtained it calls best_choice function which assigns the category with maximum score
#3) Middle list
#--> it checks the sum of first six categories > 63 if yes it focusses on lower values else it focusses on upper values
#--> if sum of first six categories > 63 if smartly tries to get triples and caudraples
#4) final_list : focuses on assigning values to remaining 4 turns

# problems faced:
# --> not able to get bonus even after focussing on first six values

# References:
#http://dicestrategy.net/

# This is the file you should modify to create your new smart Zacate player.
# The main program calls this program three times for each turn. 
#   1. First it calls first_roll, passing in a Dice object which records the
#      result of the first roll (state of 5 dice) and current Scorecard.
#      You should implement this method so that it returns a (0-based) list 
#      of dice indices that should be re-rolled.
#   
#   2. It then re-rolls the specified dice, and calls second_roll, with
#      the new state of the dice and scorecard. This method should also return
#      a list of dice indices that should be re-rolled.
#
#   3. Finally it calls third_roll, with the final state of the dice.
#      This function should return the name of a scorecard category that 
#      this roll should be recorded under. The names of the scorecard entries
#      are given in Scorecard.Categories.
#

from ZacateState import Dice
from ZacateState import Scorecard
import random
from collections import defaultdict

class ZacateAutoPlayer:

      def __init__(self):
            pass
      def frijol_four(self,dice,category_list,roll,set_list):
            counts = [dice.dice.count(i) for i in range(1,7)]
            sub_list = list(set(dice.dice).difference(set_list))
            selected = []
            if sub_list != [ ]:
                  for j in range(0,5):
                        if dice.dice[j] in sub_list:
                              selected.append(j)
            else:
                  if max(counts) >= 2:
                        for i in range(0,6):
                              if counts[i] >= 2:
                                    sub_list.append(i+1)
                        for i in range(0,5):
                              if dice.dice[i] in sub_list:
                                    selected.append(i)
                                    break
            return selected

      def frijol_three(self,dice,category_list,roll,set_list1):
            counts = [dice.dice.count(i) for i in range(1,7)]
            sub_list = list(set(dice.dice).difference(set_list1))
            selected = []
            if sub_list != [ ]:
                  for j in range(0,5):
                        if dice.dice[j] in sub_list:
                              selected.append(j)
            else:
                  if max(counts) >= 2:
                        for i in range(0,6):
                              if counts[i] >= 2:
                                    sub_list.append(i+1)
                  t = 0
                  for i in range(0,5):
                        if dice.dice[i] in sub_list and t<2:
                              selected.append(i)
                              t+=1
            return selected

      def best_choice(self,dice,category):
            best_cat = defaultdict(int)
            for x in Scorecard.Categories:
                  best_cat[x] = 0
            count_num = [dice.dice.count(i) for i in range(1,7)]
            if count_num[0] >= 1 and "unos" in category:
                  best_cat["unos"] = count_num[0] * 1
            if count_num[1] >= 1 and "doses" in category:
                  best_cat["doses"] = count_num[1] * 2
            if count_num[2] >= 1 and "treses" in category:
                  best_cat["treses"] = count_num[2] * 3
            if count_num[3] >= 1 and "cuatros" in category:
                  best_cat["cuatros"] = count_num[3] * 4
            if count_num[4] >= 1 and "cincos" in category :
                  best_cat["cincos"]= count_num[4] * 5
            if count_num[5] >= 1 and "seises" in category:
                  best_cat["seises"] = count_num[5] * 6
            if (sorted(dice.dice) == [1,2,3,4,5] or sorted(dice.dice) == [2,3,4,5,6]) and "pupusa de queso" in category:
                  best_cat["pupusa de queso"] = 40
            if (len(set([1,2,3,4]) - set(dice.dice)) == 0 or len(set([2,3,4,5]) - set(dice.dice)) == 0 or len(set([3,4,5,6]) - set(dice.dice)) == 0) and "pupusa de frijol" in category:
                  best_cat["pupusa de frijol"] = 30
            if ((2 in count_num) and (3 in count_num)) and "elote" in category:
                  best_cat["elote"] = 25
            if max(count_num) >= 3 and "triple" in category:
                  best_cat["triple"] = sum(dice.dice)
            if max(count_num) >= 4 and "cuadruple" in category:
                  best_cat["cuadruple"] = sum(dice.dice)
            if max(count_num) == 5 and "quintupulo" in category:
                  best_cat["quintupulo"] = 50
            if sum(dice.dice) > 19 and "tamal" in category:
                  best_cat["tamal"] = sum(dice.dice)
            cat = max(best_cat, key = best_cat.get)
            if cat in category:
                  return cat
            else:
                  if "unos" in category:
                        return "unos"
                  elif "doses" in category:
                        return "doses"
                  else:
                        return random.choice(category)

      def opening_list(self,dice,category_list,roll):
            counts = [dice.dice.count(i) for i in range(1,7)]
            #print "Count of all 6 numbers",counts
            #checking if quintupulo
            if max(counts) == 5 and "quintupulo" in category_list:
                      selected = []
                      if roll == 1 or roll == 2:
                        return  selected
                      elif roll == 3:
                        return  "quintupulo"
            #checking if queso
            if sorted(dice.dice) == [1,2,3,4,5] and "pupusa de queso" in category_list or sorted(dice.dice) == [2,3,4,5,6] and "pupusa de queso" in category_list:
                      selected = []
                      if roll == 1 or roll == 2:
                        return  selected
                      elif roll == 3:
                        return  "pupusa de queso"
            # pupusa de frijol
            # checking for (1,2,3,4,5) and roll = 1 , roll = 2 , roll = 3
            if ((sorted(dice.dice) == [1, 2, 3, 4, 5] and "pupusa de frijol" in category_list and roll == 1) or (sorted(dice.dice) == [2, 3, 4, 5, 6] and "pupusa de frijol" in category_list and roll == 1)) | ((sorted(dice.dice) == [1,2,3,4,5] and "pupusa de frijol" in category_list and roll == 2) or (sorted(dice.dice) == [2, 3, 4, 5, 6] and "pupusa de frijol" in category_list and roll == 2)):
                  return []
            elif (sorted(dice.dice) == [1,2,3,4,5] and "pupusa de frijol" in category_list and roll == 3) or (sorted(dice.dice) == [2,3,4,5,6] and "pupusa de frijol" in category_list and roll == 3):
                  return "pupusa de frijol"
            # checking for (1,2,3,4,x) etc. and roll = 1, roll = 2, roll = 3
            elif ((len(set([1,2,3,4]) - set(dice.dice)) == 0 or len(set([2,3,4,5]) - set(dice.dice)) == 0 or len(set([3,4,5,6]) - set(dice.dice)) == 0) and "pupusa de frijol" in category_list and roll == 1) \
                    | ((len(set([1,2,3,4]) - set(dice.dice)) == 0 or len(set([2,3,4,5]) - set(dice.dice)) == 0 or len(set([3,4,5,6]) - set(dice.dice)) == 0) and "pupusa de frijol" in category_list and roll == 2):
            # for [1,2,3,4]
                  if len(set([1, 2, 3, 4]) - set(dice.dice)) == 0:
                        set_l = set([1, 2, 3, 4])
                        selected = self.frijol_four(dice,category_list,roll,set_l)
                        return selected
                  elif len(set([2,3,4,5]) - set(dice.dice)) == 0:
                        set_l = set([2,3,4,5])
                        selected = self.frijol_four(dice,category_list,roll,set_l)
                        return selected
                  elif len(set([3,4,5,6]) - set(dice.dice)) == 0:
                        set_l = set([3,4,5,6])
                        selected = self.frijol_four(dice,category_list,roll,set_l)
                        return selected
                  else:
                        return [0,1,2,3,4]
            elif (len(set([1,2,3,4]) - set(dice.dice)) == 0 or len(set([2,3,4,5]) - set(dice.dice)) == 0 or len(set([3,4,5,6]) - set(dice.dice)) == 0) and "pupusa de frijol" in category_list and roll == 3:
                  return "pupusa de frijol"
            #checking "pupusa de frijol" (1,2,3,x,y)
            elif (len(set([1,2,3]) - set(dice.dice)) == 0 or len(set([2,3,4]) - set(dice.dice)) == 0 or len(set([3,4,5]) - set(dice.dice)) == 0 or len(set([4,5,6]) - set(dice.dice)) == 0) and "pupusa de frijol" in category_list and roll == 1:
                  if len(set([2,3,4]) - set(dice.dice)) == 0:
                        set_l = set([1,2,3])
                        selected = self.frijol_three(dice,category_list,roll,set_l)
                        return selected
                  elif len(set([2,3,4]) - set(dice.dice)) == 0:
                        set_l = set([2,3,4])
                        selected = self.frijol_three(dice,category_list,roll,set_l)
                        return selected
                  elif len(set([3,4,5]) - set(dice.dice)) == 0:
                        set_l = set([3,4,5])
                        selected = self.frijol_three(dice,category_list,roll,set_l)
                        return selected
                  elif len(set([4,5,6]) - set(dice.dice)) == 0:
                        set_l = set([4,5,6])
                        selected = self.frijol_three(dice,category_list,roll,set_l)
                        return selected
                  else:
                        return [0,1,2,3,4]
            #checking elote
            elif ((2 in counts) and (3 in counts)) and ("elote" in category_list) and (roll == 1 or roll == 2 or roll == 3):
                  # if roll = 1 retaining the three and shuffling the 2 same no.
                  selected = []
                  num = 0
                  if roll == 1:
                        if "triple" in category_list:
                              for i in range(0,6):
                                    if counts[i] == 3:
                                          num = i+1
                                          break
                              for j in range(0,5):
                                    if dice.dice[j] != num:
                                          selected.append(j)
                              return selected
                        else:
                              return selected
                  # if roll = 2 break the elote only if [4,5,6] 3's are present
                  elif roll == 2:
                        for i in range(0,6):
                              if counts[i] == 3:
                                    num = i+1
                              break
                        for j in range(0,5):
                              if dice.dice[j] != num and num in [4,5,6]:
                                    selected.append(j)
                        return selected
                  elif roll == 3:
                        return "elote"
                  else:
                        return [0,1,2,3,4]
            # Tamal to be filled only if sum is >= 22
            elif sum(dice.dice) >= 22 and "tamal" in category_list:
                  if roll == 1 or roll == 2:
                        return []
                  elif roll == 3:
                        return "tamal"
            # filling (1 to 6)
            # check if count of no is >=2 and roll = 1 then reroll / check if count of no.>=3 and roll = 2 and reroll/ check if count
            # of no. >=3 and assign to available category
            elif (max(counts) >= 2 and roll == 1) or (max(counts) >=3 and roll == 2) or (max(counts) >= 3 and roll == 3):
                  max1 = 0
                  for i in range(0,6):
                        if counts[i] == max(counts):
                              #print "count",i+1,counts[i]
                              if i+1 > max1:
                                    max1 = i+1
                             # print max1
                  selected = []
                  cat = " "
                  # the max1 obtained is already taken then, shuffle max1 and keep others intact eg. (4,4,4,2,2)
                  # where 4 i.e cautros already in list then shuffle dice in position (0,1,2) instead of (3,4)
                  for i in Scorecard.Numbers.keys():
                        if Scorecard.Numbers[i] == max1:
                              cat = i
                  #print "max count of dice category",cat
                  if roll == 1 or roll == 2:
                        for j in range(0,5):
                              if cat in category_list:
                                    if dice.dice[j] != max1:
                                          selected.append(j)
                              elif cat not in category_list:
                                    if dice.dice[j] == max1:
                                          selected.append(j)
                        #print "selected to role in 1-6",selected
                        return  selected
                  elif roll == 3:
                        if cat in category_list:
                              return cat
                        else:
                              cate88 = self.best_choice(dice,category_list)
                              return cate88
            else:
                  if roll == 1 or roll == 2:
                        return []
                  if roll == 3:
                        if counts[0] >= 1 and "unos" in category_list:
                              return "unos"
                        elif counts[1] >= 1 and "doses" in category_list:
                              return "doses"
                        else:
                              cate1 = self.best_choice(dice,category_list)
                              return cate1
      def middle_list(self,dice,category_list,roll,scorecard):
            total = 0
            counts = [dice.dice.count(i) for i in range(1,7)]
            for i in scorecard.scorecard.keys():
                  if i in Scorecard.Numbers.keys():
                        total += scorecard.scorecard[i]
            if total < 63:
                        selected = []
                        cate33 = ""
                        if roll == 1:
                              selected = self.opening_list(dice,category_list,roll)
                              return selected
                        if roll == 2:
                              selected = self.opening_list(dice,category_list,roll)
                              return selected
                        if roll == 3:
                              cate33 = self.opening_list(dice,category_list,roll)
                              if len(cate33) == 0:
                                    cate33 = self.best_choice(dice,category_list)
                                    return cate33
                              else:
                                    return cate33
            elif total >= 63:
                  #checking quintupulo
                  if max(counts) == 5 and "quintupulo" in category_list:
                      selected = []
                      if roll == 1 or roll == 2:
                        return  selected
                      elif roll == 3:
                        return  "quintupulo"
                  #checking if queso
                  if sorted(dice.dice) == [1,2,3,4,5] and "pupusa de queso" in category_list or sorted(dice.dice) == [2,3,4,5,6] and "pupusa de queso" in category_list:
                      selected = []
                      if roll == 1 or roll == 2:
                        return  selected
                      elif roll == 3:
                        return  "pupusa de queso"
                  #checking elote
                  if ((2 in counts) and (3 in counts)) and ("elote" in category_list) and (roll == 1 or roll == 2 or roll == 3):
                        # if roll = 1 retaining the three and shuffling the 2 same no.
                        selected = []
                        num = 0
                        if roll == 1:
                              if "triple" in category_list or "cuadruple" in category_list:
                                    for i in range(0,6):
                                          if counts[i] == 3:
                                                num = i+1
                                                break
                                    for j in range(0,5):
                                          if dice.dice[j] != num:
                                                selected.append(j)
                                    return selected
                              else:
                                    return selected
                        # if roll = 2 break the elote only if [4,5,6] 3's are present
                        elif roll == 2:
                              for i in range(0,6):
                                    if counts[i] == 3:
                                          num = i+1
                                    break
                              for j in range(0,5):
                                    if dice.dice[j] != num and num in [4,5,6]:
                                          selected.append(j)
                              return selected
                        elif roll == 3:
                              return "elote"
                  # Tamal to be filled only if sum is >= 22
                  elif sum(dice.dice) >= 22 and "tamal" in category_list:
                        if roll == 1 or roll == 2:
                              return []
                        elif roll == 3:
                              return "tamal"
                  # checking caudrapule
                  elif max(counts) >= 4 and "cuadruple" in category_list:
                        if roll == 1 or roll == 2:
                              value = 0
                              selected = []
                              for i in range(0,6):
                                    if counts[i] == max(counts):
                                          value = i+1
                                          break
                              for j in range(0,5):
                                    if dice.dice[j] != value:
                                          selected.append(j)
                              return selected
                        if roll == 3:
                              return "cuadruple"
                  #checking triple
                  elif max(counts) >= 3 and "triple" in category_list:
                        if roll == 1 or roll == 2:
                              value = 0
                              selected = []
                              for i in range(0,6):
                                    if counts[i] == max(counts):
                                          value = i+1
                                    break
                              for j in range(0,5):
                                    if dice.dice[j] != value:
                                          selected.append(j)
                              return selected
                        if roll == 3:
                              return "triple"
                  else:
                        if roll == 1 or roll == 2:
                              return []
                        elif roll == 3:
                              if counts[0] >= 1 and "unos" in category_list:
                                    return "unos"
                              elif counts[1] >= 1 and "doses" in category_list:
                                    return "doses"
                              else:
                                    cate44 = self.best_choice(dice,category_list)
                                    return cate44
      def final_list(self,dice,category_list,roll):
            counts = [dice.dice.count(i) for i in range(1,7)]
            #checking quintupulo
            if max(counts) == 5 and "quintupulo" in category_list:
                  selected = []
                  if roll == 1 or roll == 2:
                        return  selected
                  elif roll == 3:
                        return  "quintupulo"
            #checking if queso
            if sorted(dice.dice) == [1,2,3,4,5] and "pupusa de queso" in category_list or sorted(dice.dice) == [2,3,4,5,6] and "pupusa de queso" in category_list:
                  selected = []
                  if roll == 1 or roll == 2:
                        return  selected
                  elif roll == 3:
                        return  "pupusa de queso"
            #checking elote
            if ((2 in counts) and (3 in counts)) and ("elote" in category_list) and (roll == 1 or roll == 2 or roll == 3):
                  # if roll = 1 retaining the three and shuffling the 2 same no.
                  selected = []
                  num = 0
                  if roll == 1:
                        if "triple" in category_list or "cuadruple" in category_list:
                              for i in range(0,6):
                                    if counts[i] == 3:
                                          num = i+1
                                          break
                              for j in range(0,5):
                                    if dice.dice[j] != num:
                                          selected.append(j)
                              return selected
                        else:
                              return selected
                  # if roll = 2 break the elote only if [4,5,6] 3's are present
                  elif roll == 2:
                        for i in range(0,6):
                              if counts[i] == 3:
                                    num = i+1
                              break
                        for j in range(0,5):
                              if dice.dice[j] != num and num in [4,5,6]:
                                    selected.append(j)
                        return selected
                  elif roll == 3:
                        return "elote"
            # Tamal to be filled only if sum is >= 22
            elif sum(dice.dice) >= 22 and "tamal" in category_list:
                  if roll == 1 or roll == 2:
                        return []
                  elif roll == 3:
                        return "tamal"
            # checking caudrapule
            elif max(counts) >= 4 and "cuadruple" in category_list:
                  if roll == 1 or roll == 2:
                        value = 0
                        selected = []
                        for i in range(0,6):
                              if counts[i] == max(counts):
                                    value = i+1
                                    break
                        for j in range(0,5):
                              if dice.dice[j] != value:
                                    selected.append(j)
                        return selected
                  if roll == 3:
                        return "cuadruple"
            #checking triple
            elif max(counts) >= 3 and "triple" in category_list:
                  if roll == 1 or roll == 2:
                        value = 0
                        selected = []
                        for i in range(0,6):
                              if counts[i] == max(counts):
                                    value = i+1
                              break
                        for j in range(0,5):
                              if dice.dice[j] != value:
                                    selected.append(j)
                        return selected
                  if roll == 3:
                        return "triple"
            else:
                  if roll == 1 or roll == 2:
                        return [0,1,2,3,4]
                  if roll == 3:
                        if counts[0] >= 1 and "unos" in category_list:
                              return "unos"
                        elif counts[1] >= 1 and "doses" in category_list:
                              return "doses"
                        else:
                              cate44 = self.best_choice(dice,category_list)
                              return cate44

      def turn(self,category_list,dice,roll,scorecard):
            if (len(category_list) > 9) and (len(category_list) <= 13):
                  selected_category = self.opening_list(dice,category_list,roll)
            elif (len(category_list) <= 9) and (len(category_list) >= 5):
                  selected_category = self.middle_list(dice,category_list,roll,scorecard)
            elif (len(category_list) <= 4) and (len(category_list) >= 1):
                  selected_category = self.final_list(dice,category_list,roll)
            return selected_category

      def first_roll(self, dice, scorecard):
            category_list = list(set(Scorecard.Categories) - set(scorecard.scorecard.keys()))
            selected_first = self.turn(category_list,dice,1,scorecard)
            return selected_first

      def second_roll(self, dice, scorecard):
            category_list = list(set(Scorecard.Categories) - set(scorecard.scorecard.keys()))
            selected_second = self.turn(category_list,dice,2,scorecard)
            return selected_second
      
      def third_roll(self, dice, scorecard):
            category_list = list(set(Scorecard.Categories) - set(scorecard.scorecard.keys()))
            selected_third = self.turn(category_list,dice,3,scorecard)
            return selected_third

