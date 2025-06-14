import MeCab
import pandas as pd


class Word_data:
    def mecab_list(self,text):
        tagger = MeCab.Tagger("-Ochasen")   #ChaSenという形態素解析器と互換の出力をする設定にしている
        tagger.parse('')
        node = tagger.parseToNode(text) #nodeにsurface(単語)feature(品詞情報)を持つ解析結果を代入
        word_class = []
        while node:
            word = node.surface #wordにnodeの単語を入力
            #print(word)
            wclass = node.feature.split(',')
            ##node.featureは品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音の順になっているのでsplitで配列化
            if wclass[0] != u'BOS/EOS': #BOS は beginning of sentenceで文頭、EOS は end of sentence で文末、ということ。
                if wclass[6] == "*":
                    word_class.append(word)
                else:
                    word_class.append(wclass[6])
            node = node.next

        word_class = ','.join(word_class)+","
        return word_class

    def word_datacheck(self,me_text):
        pos = 0
        neg = 0
        for i, row in self.Emotion.iterrows():
            posneg = self.Emotion.loc[i, 'seikika'] in me_text
            if posneg == True and self.Emotion.loc[i, 'pos_neg'] == 'pos':
                    pos += 1
            elif posneg == True and self.Emotion.loc[i, 'pos_neg'] == 'neg':
                    neg += 1

        if pos != 0 and neg != 0:
            pos = 0
            neg = 0

        if pos >= 1:
            result = "Pos"
        elif neg >= 1:
            result = "Neg"
        else:
            result = "None"
        #print(result)

        return result


    def csv_read(self):
        emotion_dic=pd.read_csv("D18-2018_2.csv")
        list=[]
        for i, row in emotion_dic.iterrows():
            emotion_dic.loc[i,'seikika']=self.mecab_list(emotion_dic.at[i,'Word'])
        print("list="+str(list))

        return emotion_dic



