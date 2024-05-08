
# jinmei-variants.txtとjoyo-variants.txt、non-cjk.txtは以下のソフトウェアから使用した

# 異体字データベース
# https://kanji-database.sourceforge.net/

#　Mit licence 
# © 2009 CJKV (Chinese Japanese Korean Vietnamese) Ideograph Database

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


#＜辞書を読み込む関数＞
def load_text(filePath: str):


    #＜テキストの読み込み＞
    with open(filePath, encoding='utf8') as f:
        data = f.read().split("\n")
       

    #＜二重配列へ変換する処理＞
    i = 0
    while True:
        
        content = data[i]
        
        if i == len(data)-1:
            #終端を削除
            data.pop(i)
            break

        #コメント行の場合削除
        if content == "" or content[0] == "#" or content == "\x1a":
            data.pop(i)

        #hydzd-variants.txtの簡体字の部分を削除
        #elif "hydzd/simplified" in content or content[0:4] == "hydzd":
            #data.pop(i)

        #inmei-variants.txtの凡例を削除
        elif content[:5] in "jinmei":
            data.pop(i)

        #joyo-variants.txtの凡例を削除
        elif str(content)[:3] in "joyo":
            data.pop(i)

        #non-cjk.txtのカタカナの部分と凡例を削除
        elif "non-cjk/katakana" in content or content[0:6] in "non-cjk":
            data.pop(i)
            
        

        #削除、終了しない場合
        else:
            #分割
            data[i] = content.split(",")
            i += 1
        
        
        


    #print(content)
    return data





#辞書を使用して異体字を置き換える処理
def normalize(input:str  ,debug_print:bool = False):

    itaiji_list = []


    #法務省・人名漢字表（2010年現在）の、別表２の１で同一の字種とされる漢字および人名漢字表 別表２の２で規定される異体字
    itaiji_list += load_text("./dict/cjkvi-variants/jinmei-variants.txt")

    #文科省・常用漢字表に記載された異体字（2010年現在）
    itaiji_list += load_text("./dict/cjkvi-variants/joyo-variants.txt")

    #UCSにおける非漢字・擬似漢字と漢字の対応表
    itaiji_list += load_text("./dict/cjkvi-variants/non-cjk.txt")

    #漢語大字典に記載されている異体字一覧
    #itaiji_list += load_text("./dict/cjkvi-variants/hydzd-variants.txt")

    



    #＜変換前の文字のリスト作成＞
    after_conv_word_list = []

    for l in itaiji_list:
        after_conv_word_list.append(l[2])




    #＜再変換してしまう項目（ある項目の変換後の文字がその後の項目の変換前のもじと同じ場合もう一度変換してしまう）の削除リストを作成＞
    dell_list = []
 
        
    for l in itaiji_list:

        #異体字リストの現在の項目の変換前の字を代入
        before_conv_word = l[0] 

        
        while True:
            #現在の項目の変換後の字が、変換前の字のリストにない場合
            if not before_conv_word in after_conv_word_list:
                break

            num = after_conv_word_list.index(before_conv_word)

                

            #チェックを付ける
            after_conv_word_list[num] = "Checked"

            #[!]デバッグ出力
            if debug_print == True:
                dellword = itaiji_list[num]
                print("文字:" + str(dellword) + ",番号:" + str(num))

            
            #変換後文字リストの現在の項目が異体字リストの現在の項目より前の場合
            #（変換後の文字Xが後で変換前の文字として出てくる場合）
            if num < itaiji_list.index(l):

                #変換後の文字Xを消去リストに追加
                dell_list.append(num)



    #消去リストを使用し削除
    dellnum = 0
    for i in dell_list:
        #インデックス番号-消去した数
        itaiji_list.pop(i-dellnum)
        dellnum += 1



    #＜異体字の置換処理＞

    i = 0

    while True:

        #異体字が含まれているか判定
        if itaiji_list[i][2] in input:
           #異体字を置換
           input = input.replace(itaiji_list[i][2], itaiji_list[i][0]) 

        
        i += 1


        #辞書のすべての項目を検証したら終了
        if i == len(itaiji_list):
            break

    
    #変換後の文字を返す
    return input 

#print(normalize(text, True))