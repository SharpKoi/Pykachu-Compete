# 比賽用的Repository
## 檔案結構
### 結構圖
```
├─<compete 1>
│  ├─data
│  │  └─cleaned_data
│  └─submittion
├─<compete 2>
│  ├─data
│  │ └─cleaned_data
│  └─submission
├─<compete 3>
│  ├─data
│  │  └─cleaned_data
│  └─submission
├─<compete 4>
│  ├─data
│  │ └─cleaned_data
│  └─submission
│ ...
```

### 說明
`/` 根目錄(也就是首頁)放的是各個比賽的資料夾，還有一些git的設定檔。

`/<compete>/` 比賽目錄下放的是程式碼，還有 data 資料夾以及 submission 資料夾。

`/<compete>/data/` data目錄下放的是官方給的原生資料(raw data)，還有一個 cleaned_data 資料夾。

`/<compete>/data/cleaned_data/` cleaned_data目錄下放的是所有處理過的資料。

`/<compete>/submission/` submission目錄下放的是要繳交的資料文件。

*其他沒被歸類到的就看哪裡適合就放哪裡*