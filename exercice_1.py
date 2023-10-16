
SPLIT = ' '
def my_fuction(p_size, dict_possibilities, sentence):
    split_sentence = sentence.split(SPLIT)
    for possibilities in range(p_size):
        if not int(possibilities+1) in dict_possibilities or \
            not split_sentence[possibilities] in dict_possibilities[int(possibilities+1)]:
            return False
    return True


def test_my_fuction(p_size, dict_possibilities, sentence, correct ):
    try:
        assert my_fuction(p_size, dict_possibilities, sentence) == correct
        print (f"Test with: {sentence} is {my_fuction(p_size, dict_possibilities, sentence)} as expected")
    except AssertionError:
        print ("Test error")

p_size = 3
dict_possibilities = {1 : ["Je" , "Tu" , "Demain je" ],
       2 : ["mange" , "bois" , "vole" , "voles" ], 
       3 : ["." , "!" , "?" , "…" ]}
sentence_1 = "Je mange !" 
sentence_2 = "Tu dors ?"
#test correct

test_my_fuction(p_size, dict_possibilities, sentence_1, True)
test_my_fuction(p_size, dict_possibilities, sentence_2, False)

#test other wrong dict
dict_possibilities_wrong = {
       2 : ["mange" , "bois" , "vole" , "voles" ], 
       3 : ["." , "!" , "?" , "…" ]}

test_my_fuction(p_size, dict_possibilities_wrong, sentence_1, False)

dict_possibilities_wrong_2 = { 1: [],
       2 : [], 
       3 : []}
test_my_fuction(p_size, dict_possibilities_wrong_2, sentence_1, False)

#test empty
test_my_fuction(p_size, dict_possibilities, "", False)
test_my_fuction(0, {}, "", True)
