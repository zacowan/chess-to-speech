
dict={
    "a22": "A2 to",
    "a42": "A4 to",
    "b22": "B2 to" ,
    "c22": "C2 to",
    "d22": "D2 to",
    "e22": "E2 to",
    "f22": "F2 to",
    "g22": "G2 to",
    "h22": "H2 to",
    "tutu": "2 to",
    "2282": "A2 to A2",
    "2288": "A2 to A2",
    "822": "A2 to",
    "8284": "A2 to A4",
    "2284": "to A4",
    "8384": "A3 to A4",
    "8484": "A4 to A4",
    "8584": "A5 to A4",
    "8684": "A6 to A4",
    "8784": "A7 to A4",
    "8884": "A8 to A4",
    "82284": "A2 to A4",
    "F-22": "F2",
    "F-2": "F2",
    "1/4":"A4 to",
    "D12":"D1 to",
    
    }
def adjust_with_bias(text):
    word_list=text.split()
    res_string=""
    for word in word_list:
        if word.lower() in dict.keys():
            print(word.lower()[len(word)-1:len(word)])
            if dict[word.lower()]=="2 to" and len(res_string)>0:
                res_string= res_string[0:len(res_string) -1]
            print("Bias adjustested")
            res_string+=dict[word.lower()]+" "
        elif(len(word)>2 and word.lower()[len(word)-1:len(word)]=="2"):
                res_string+=word[0:len(word)-1]
                res_string+=" to "
                print("Bias adjustested")
                continue
        elif(len(word)>2 and word.lower()[len(word)-1:len(word)]=="2"):
                res_string+=word[0:len(word)-1]
                res_string+=" to "
                print("Bias adjustested")
                continue
        else:
            res_string+=word+" "
    return res_string[0:len(res_string) -1]
            










