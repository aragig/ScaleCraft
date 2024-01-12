# ScaleCraft

画像をリサイズするPythonパッケージ


![ScaleCraft](./logo.png)

## インストール
    
```zsh
pip3 install git+https://github.com/aragig/ScaleCraft
```


## 使い方
```python
from ScaleCraft import ScaleCraft


ScaleCraft(input_path).scale(0.5).saveJPEG(85, output_path)
# or
ScaleCraft(input_path).resize(400, 300).saveJPEG(85, output_path)
```
