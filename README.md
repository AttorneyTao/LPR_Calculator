<!--
SPDX-FileCopyrightText: 2023 Tao Ye <taoye1992@163e.com>

SPDX-License-Identifier: MIT
-->

# LPR_Calculator

本软件可实现对LPR的批量计算，适用于存在多笔本金的情形，如每月均产生货款（或租金、工程款等），需分别计算资金占用利息时，可实现一次性的计算，并分别生成明细。

使用步骤：

1. 在config文件夹中，打开config.xlsx，选择利息类型（1年期/5年期），一年按多少天计算（360天/365天）

   ![image-20230303150930979](C:\Users\taoye\AppData\Roaming\Typora\typora-user-images\image-20230303150930979.png)

   2.在data文件夹中，打开data_lpr.xlsx，更新LPR数据（目前更新到2023年2月20日）。

   ![image-20230303151017436](C:\Users\taoye\AppData\Roaming\Typora\typora-user-images\image-20230303151017436.png)

   3. 在data文件夹中，打开data.xlsx文件，输入待计算数据。

      ![image-20230303151100879](C:\Users\taoye\AppData\Roaming\Typora\typora-user-images\image-20230303151100879.png)

***注：以上步骤不要修改数据格式，不要修改表头，不要留空值，严格按照已有数据的格式填写。***

4. 双击main.exe运行。（启动较慢，请耐心等待）

   ![image-20230303153214475](C:\Users\taoye\AppData\Roaming\Typora\typora-user-images\image-20230303153214475.png)

5. 结果保存在根目录下res.xlsx中

![image-20230303151248286](C:\Users\taoye\AppData\Roaming\Typora\typora-user-images\image-20230303151248286.png)