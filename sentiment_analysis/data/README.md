# Data Set
> 由於csv檔太大，且Github的LFS支援有大小限制，免費用戶最多只能上傳1GB，因此所有data我都放在Google Drive上。
## Raw Data
#### 描述
蝦皮給的train.csv跟test.csv都會放在這。  

## Cleaned Data
#### 描述
經處理過的資料都會放在 `cleaned_data/` 目錄底下。  
#### 檔案格式
`data_emoji.csv` 原生資料以空白分隔emoji的資料。  
`data_emoji2word.csv` 原生資料以空白分隔emoji，並將emoji轉為單詞的資料。  
`data_sol{number}.csv` 已處理某些解決方向的資料。`{number}`為特徵工程解決方向的代號，詳見 [Document](https://docs.google.com/document/d/1Hrj9KQOqlmSbk-LthMqS4LfY8PdOsLwg5jnsTby3xaM/edit?usp=sharing)。  

## Library
#### 描述
程式碼中會用到的第三方資料都會放在 `lib/` 目錄底下。  