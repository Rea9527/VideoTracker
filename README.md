# 视频标注及追踪

## 1. 环境
**追踪部分**：需安装OpenCV2

**标注及预处理**：需安装Python3以及PIL等库

## 2. 运行
**追踪部分**：安装配置好OpenCV2后，执行以下命令

`g++ -L CV2库路径 -I CV2头文件路径 main.cpp ./KCF/kcftracker.cpp ./KCF/fhog.cpp -o main.o`

**标注及预处理**：直接`python3 preprocessing.py`

## 3. 文件
`/KCF`: KCF Tracker核心代码
`main.cpp`: 视频追踪主函数

`Preprocessing.py`: 视频标注及预处理代码

## 4. 说明

**注意**：对于要追踪的视频，应确保视频的移动速度足够慢，否则结果会有较大误差！

本次追踪，由于视频比较多，故要对所有视频进行批处理。这就需要将不同的视频依次放在名为0，1，2...的文件夹下，便于生成下面提到的images.txt、region.txt以及多视频自动连续追踪。



**追踪部分**

运行后输入要追踪的视频总数

输入文件说明：

`images.txt`: 包含要追踪视频的所有图片帧的路径，如下：
<center><img src="/Users/ReaChan/Desktop/Screen Shot 2017-07-09 at 21.19.13.png" width=450px /></center>

`region.txt`: 追踪视频第一帧所选区域的四个顶点的宽高信息，如下：
<center><img src="/Users/ReaChan/Desktop/Screen Shot 2017-07-09 at 21.21.25.png" width=450px /></center>

输出文件说明：

`output.txt`：依次存储所有视频的每一帧的追踪结果，格式如下：
<center><img src="/Users/ReaChan/Desktop/Screen Shot 2017-07-09 at 21.28.26.png" width=450px /></center>


---

**标注及预处理部分**

对于文件路径，直接看代码即可，有注释。

函数说明：

`frameNameProcessing()`: 自动生成images.txt

`regionProcessing()`: 标注，运行后，会依次对所有视频的第一帧进行标注，在弹出的图片中选中4个点即可

`downsample()`: 处理后的图片尺寸较大，不便于跑CNN，故需下采样

`classify()`: 用于提取训练集和测试集，并生成train\_data.txt和test_data.txt
