# CNN Models Performation
*紀錄一下在調整模型時每一步觀察結果、遇到的問題、思考方向以及更改過程，以便往後試圖改良模型時能梳理模型歷史的更改脈絡。*
## 目錄
[toc]

## 過程

### 最初的模型
:::spoiler
#### 描述
*這個模型是參考一個由作者 [Akshat Maheshwari](https://github.com/akki3d76) 所寫的CNN模型，這個模型適用在Text-Classification領域上，因此為了適用於我們的資料集，稍微改了資料前處理部分的code，並增加該模型的kernelsize到8，降低MaxPooling的size到3，為的是希望模型能吸取到更全面的資料，也順便為模型增加複雜度。*
#### 程式
```python=
embedding_layer = Embedding(input_dim=WORD_ID_DICT_LEN+1, 
                           output_dim=EMBEDDING_DIM, 
#                            weights=[embedding_matrix], 
                           input_length=MAX_VOCABULARY_NUM, 
                           trainable=True)

seq_input = Input(shape=(WORD_SEQUENCE_LENGTH,), dtype='int32')
embedding_seq = embedding_layer(seq_input)
conv_layer1 = Conv1D(128, 8, activation='relu')(embedding_seq)
pool_layer1 = MaxPooling1D(3)(conv_layer1)
conv_layer2 = Conv1D(128, 8, activation='relu')(pool_layer1)
pool_layer2 = MaxPooling1D(3)(conv_layer2)
conv_layer3 = Conv1D(128, 8, activation='relu')(pool_layer2)
pool_layer3 = MaxPooling1D(3)(conv_layer3)
conv_layer4 = Conv1D(128, 8, activation='relu')(pool_layer3)
pool_layer4 = MaxPooling1D(26)(conv_layer4)
flatten_layer = Flatten()(pool_layer4)
dense_layer = Dense(128, activation='relu')(flatten_layer)
predict_layer = Dense(LABEL_NUM, activation='softmax')(dense_layer)
```

#### 結構
![model_1](https://i.imgur.com/6GXq42K.png =350x)

#### 表現
...超差，直接給我一個重擊 :punch: 
```
epochs= 9
acc= 0.29x -> 0.28x -> ... -> 0.28x
```
> 由於最一開始沒有任何想法，直接拿著範本下去跑，只是感覺應該可以表現得不錯，所以沒有記錄下完整的訓練過程
:::

### 範本模型
:::spoiler
#### 描述
*在發現最初的模型表現不佳後，決定先不動任何參數，看一下參考模型的表現*
#### 程式
```python=
embedding_layer = Embedding(input_dim=WORD_ID_DICT_LEN+1, 
                           output_dim=EMBEDDING_DIM, 
#                            weights=[embedding_matrix], 
                           input_length=MAX_VOCABULARY_NUM, 
                           trainable=True)

seq_input = Input(shape=(WORD_SEQUENCE_LENGTH,), dtype='int32')
embedding_seq = embedding_layer(seq_input)
conv_layer1 = Conv1D(128, 5, activation='relu')(embedding_seq)
pool_layer1 = MaxPooling1D(5)(conv_layer1)
conv_layer2 = Conv1D(128, 5, activation='relu')(pool_layer1)
pool_layer2 = MaxPooling1D(5)(conv_layer2)
conv_layer3 = Conv1D(128, 5, activation='relu')(pool_layer2)
pool_layer3 = MaxPooling1D(35)(conv_layer3)
flatten_layer = Flatten()(pool_layer3)
dense_layer = Dense(128, activation='relu')(flatten_layer)
predict_layer = Dense(LABEL_NUM, activation='softmax')(dense_layer)
```

#### 結構
![model_2](https://i.imgur.com/HyYbTI1.png =350x)


#### 表現
相比於最初的模型，第一個epoch的準確度就提升到了0.36x，但準確度卻隨著epochs的增加逐漸遞減...
```
epochs= 5
acc= 0.36x -> 0.30x -> ... -> 0.29x
```
> 只是看一下這參考模型有沒有騙我，所以也沒記錄完整過程

#### 結論
就這次的觀察發現<span style='color:dodgerblue'>模型複雜度不是影響表現的主要原因</span>，後來小組討論了一下後，覺得可能是由於訓練資料的單詞種類過於多樣，導致模型學習時<span style='color:coral'>依賴太多無意義或意思重複但型式不同的單詞</span>，因此決定<span style='color:limegreen'>在分類時關掉一些神經元</span>
:::

### 加入Dropout Layer
:::spoiler
#### 描述
經過討論後，希望模型學習時不要過度依賴多餘的詞彙，因此在進行分類前加入了Dropout layer，關閉一些神經元。
#### 程式
```python=
embedding_layer = Embedding(input_dim=WORD_ID_DICT_LEN+1, 
                           output_dim=EMBEDDING_DIM, 
#                            weights=[embedding_matrix], 
                           input_length=MAX_VOCABULARY_NUM, 
                           trainable=True)

seq_input = Input(shape=(WORD_SEQUENCE_LENGTH,), dtype='int32')
embedding_seq = embedding_layer(seq_input)
conv_layer1 = Conv1D(128, 5, activation='relu')(embedding_seq)
pool_layer1 = MaxPooling1D(5)(conv_layer1)
conv_layer2 = Conv1D(128, 5, activation='relu')(pool_layer1)
pool_layer2 = MaxPooling1D(5)(conv_layer2)
conv_layer3 = Conv1D(128, 5, activation='relu')(pool_layer2)
pool_layer3 = MaxPooling1D(35)(conv_layer3)
flatten_layer = Flatten()(pool_layer3)
dense_layer = Dense(128, activation='relu')(flatten_layer)
tf.random.set_seed(0)
drop_layer1 = Dropout(.2)(dense_layer)
predict_layer = Dense(LABEL_NUM, activation='softmax')(drop_layer1)
```

#### 結構
![model_3](https://i.imgur.com/1mKNuCa.png =350x)

#### 表現
#### 結論
<span style='color:dodgerblue'>觀察</span>
實驗結果顯示加入dropout layer後模型表現明顯較範本模型好，這意味著資料集裡的確有太多冗言贅詞。
而進行淺層學習的另一組發現資料集裡有許多種類相同但長相不同的詞(例如bags跟bagsssss)，英文中還參雜著許多國以英文字母形式出現的語言

<span style='color:coral'>改進方向</span>
1. 過濾長相不同但種類相同的單詞
2. 多國語言的單詞意思
3. 找出準確度隨epochs增加而下降的主因
4. 提升準確度
5. 防止Overfitting的情況發生

<span style='color:limegreen'>改進方法</span>
針對第2個方向，深度學習模型可透過練習來找出他國語言的單詞的表示向量。
針對第3, 4, 5，減少訓練資料，一方面可以較快觀察結果，一方面減少詞彙量，增加重複較多次的單詞數量
:::

### 新版模型
:::spoiler
#### 描述
#### 程式
#### 結構
#### 表現
#### 結論
:::
