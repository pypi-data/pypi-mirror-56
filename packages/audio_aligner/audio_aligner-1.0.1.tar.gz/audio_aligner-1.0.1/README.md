## 音频对齐工具
## python版
### 安装
`pip install audio_aligner`

### command-line
##### 初始化
``` python
import tf_audio_manager  
res = tf_audio_manager.AudioAligner('119.23.204.245','9073')
```
##### 上传
``` python
res.upload('/Users/duyining/Desktop/chinese_test.zip')
```
##### 查看可操作文件列表
``` python
res.list()
```
##### 检查单个文件的状态
``` python
res.check_status('1574081890.2423242')
```
##### 中文ctm
``` python
res.chinese_thread('1574081890.2423242') 
```
##### 英文ctm
``` python
res.english_thread('1574081890.2423242')  
```
##### 装换成功
``` python
res.check_status('1574081890.2423242')
```
##### 保存结果到本地
``` python
res.download('1574081890.2423242','/Users/duyining/desktop/file.txt')
```

