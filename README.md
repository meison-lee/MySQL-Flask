
## Implementation
### User
https://youtu.be/KDSdgODHUDw

<!-- 資料庫設計 -->
## 資料庫設計之資料表如下：

1. activity
* 符合題目需求設計活動之id,name,scope,type,value,available,startAt,endAt,productId,sellerId

2. color
* 為各別ID的顏色記入其名稱

3. coupon
* 符合題目需求設計活動之id,name,scope,type,value,amount,startAt,endAt,productId,sellerId

4. inventories
* 考慮資料庫之合理性，特別設計了一個inventories的資料表，當中記錄id,colorId,sizeId,inventory，id為各別顏色尺寸衣服所剩庫存的特定編號

5. order
* 符合題目需求設計訂單之id,items,totalPrice,status,sellerId,buyerId,createAt,updateAt,CouponUsed

6. products
* 符合題目需求設計訂單之product_id,name,description,picture,colors,sizes,price,available,startAt,endAt,sellerId,inventories。當中的inventories為特定顏色尺寸衣服所剩庫存的特定編號

7. size
* 為各別ID的尺寸記入其名稱id,name

8. user
* 符合題目需求設計訂單之user_id,name,email,phone,password,coupon，當中的coupon為user所擁有的折價卷ID

9. items
*  考慮資料庫之合理性，特別設計了一個items的資料表，當中記錄id,productId,amount，id為各別購買項目和購買數量的特定編號


<!-- 待優化項目 -->
1. 沒有檢查期限相關資訊
2. try catch 沒處理好，但不影響實際操作。
3. 回傳資訊有些會包含foreign key，應該統整一下code 統一每個 route 下的回傳資料

## Run in local
1. move in DBFinalProject directory and run "python3 routes.py"
2. if there are module not found,create the environment and install them by "pip3 install flask..."
3. we test the code on postman
