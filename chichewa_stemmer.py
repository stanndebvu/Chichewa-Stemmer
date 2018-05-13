class stemming:
    '''The class is responsible for removing all the suffixes of a word'''

    def __init__(self):
        self.prefix=['mwa','mwau','mo','ku', 'li','i','zo','ndina',
        'ada','ada','anka','wo','a','pa','mu','ma','mi','chi','ka','ti','u','zi','si','su','sa','woka','woza','po','o','la','wa','na','nko','nkwa']
        self.infix=['dz','nk','mm','na','ku','da','sa','ma']
        self.suffix=['be','nso','ni','eka','di','itsa','era','tsa','ana','chi','li','ti','ko','ja','po','mu','mo','ku','ko','nji','edwa','idwa','tu']

        self.b = ""  # buffer for word to be stemmed
        self.k = 0
        self.k0 = 0
        self.j = 0   # j is a general offset into the string        self.s_len=''

    def ends(self, suffix):
        """ends(s) is TRUE <=> k0,...k ends with the string s."""        
        length =len(suffix)
        self.s_len=length
        
        if length>=len(self.b):# do nothing if the word is not attached to a stem
           return 0

        if suffix[length - 1] != self.b[self.k]: # tiny speed-up
            return 0
        if length >(self.k - self.k0 + 1):
            return 0
        if self.b[self.k-length+1:self.k+1] != suffix:
            return 0
        self.j = self.k - length
        return 1

    def strip_suffix_only(self):
        found=False
        for x in self.suffix:
            length=len(x)
            index=len(self.b)-length-1 #find the position os the latter befor the suffix
            if self.b.endswith(x):
                found=True 
                if self.cons(index): #test if the letter  b4  is a vowel
                    if length>2 :
                        if self.b[index]=='w':
                            pass
                        else:
                            self.k=len(self.b)-length  
                            self.setto("a") 
                    else:
                        pass
                else:
                    self.k= len(self.b)-length-1# remove the  leter before the suffix
                    self.setto("a")
    def is_stem(self,word):
        
        
        with open("stem_dictionary.txt",'r') as openfile:# open a file that contains stem
            stems=openfile.read()
            
            if word not in stems:
                    return 0
            else:
                return 1


    def inside_sterm(self):
        
        
        with open("stem_dictionary.txt",'r') as openfile:
            stem=openfile.read()
            stems=stem.split()
            k0=0
            k=0
            len_1=0
            index_1=-1
            
            for x in stems:
                index=self.b.find(x)
                if index !=-1:
                    length=len(x)
                    if length>len_1:
                        len_1=length
                        index_1=index

                if index>-1:
                    self.k0=index_1
                    self.k=len_1+index_1-1
                else:
                    pass
            

                          

    def strip_infix(self):
        for x in self.infix:
            length=len(x)
            total_len=len(self.b)
            index=self.b.find(x)
            if index >0 and index <5 and not self.b.endswith(x):
                if index+length+1==total_len:
                    break
                if self.cons(length+index): #test if the next letter after infix is a vowel
                    self.k0=length+index# do not remove the next leter after infix
                    break
                else:
                    self.k0=length+index+1# remove the next leter after infix
                    break
                    
            else:
                self.strip_suffix_only()



    def strip_prefix(self,prefix):
        ''' strip all the types of prifixes if the word does not start with one type of prix try the other type'''
        length=0
        test=self.b
        for x in prefix:
            if self.b.startswith(x):
                length=len(x)
                self.k0=length
                

    def setto(self, s):
        """setto(s) sets (j+1),...k to the characters in the string s, readjusting k."""
        length = len(s)
        if len(self.b)>length:
            self.b = self.b[:self.j+1] + s + self.b[self.j+length+1:]
            self.k = self.j + length
            self.start_with()

    def stems_to_word(self):
        """step1ab() gets rid of suffixes that that that makes a word to be an adverb or that make the word to be an object of a sentnce
        """
        if self.ends("idwa") or self.ends("ika") or self.ends("etsa") or self.ends("ira") or self.ends("era") or self.ends("edwa")  or self.ends("itsa")or self.ends("ire") or self.ends("eka"):
            self.setto("a")
        elif self.ends("nso") or  self.ends("be"):
            self.setto('')
        else:
            self.strip_infix()


    def cons(self, i):
        """decide whether a letter is consonat or not."""
        if self.b[i] == 'a' or self.b[i] == 'e' or self.b[i] == 'i' or self.b[i] == 'o' or self.b[i] == 'u':
            return 0
        else:
            return 1

    def start_with(self):
        
        for x in self.prefix:
            length=len(x)
            if self.b.startswith(x):
                self.k0=length

     
    def stem(self, p, i, j,affix):
        """In stem(p,i,j), p is a char pointer, and the string to be stemmed
        is from p[i] to p[j] inclusive. Typically i is zero and j is the
        """
        # copy the parameters into statics
        self.b = p
        self.k = j
        self.k0 = i
        if self.k <= self.k0 + 1:
            return self.b # --DEPARTURE--

    
        if affix==1:
            self.strip_infix()
        elif affix==2:
            self.strip_prefix(self.prefix)
        elif affix==0:
            self.inside_sterm()
        else:
            self.stems_to_word()
            
        
        return self.b[self.k0:self.k+1]


def is_in_stopword(word):
        
        
        with open("stop_words.txt",'r') as openfile:# open a file that contains a list of stop words
            stopwords=openfile.read()
            
            if word not in stopwords:
                    return 0
            else:
                return 1


if __name__ == '__main__':

    mawu=[]
    ina=[]
    unchanged=0
    correctl_stemmed=0
    under_stemmed=0
    over_stemmed=0
    all_words=0
    count=0
    p = stemming()
    word="amapitabe" # this is the word to be stemmed
    stop_word=False
    if is_in_stopword(word):
        stop_word=True
    
    if stop_word==True:
        print(word +" is a stop word no need to be stemmed")
    else:
    
        if p.is_stem(word):
                pass    
        else:
            word=p.stem(word,0,len(word)-1,0)

        if p.is_stem(word):
            pass    
        else:
            word=p.stem(word,0,len(word)-1,1)

        if p.is_stem(word):
            pass    
        else:
            word=p.stem(word,0,len(word)-1,2)

        if p.is_stem(word):
            pass    
        else:
            word=p.stem(word,0,len(word)-1,3)
        print(word)




        

