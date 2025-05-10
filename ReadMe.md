## Here are the installation instructions
# install libraries
```
pip install gymnasium torch matplotlib ipython
```



## Here is how you can run the code to see win_rates
Note that the training was actually done in ipynb notebooks on google colab and kaggle, but we converted to python files for more modularity of code.


# Against win-block player
```
python dynamic_test_model.py --opponent random
```
# Against random player
```
python dynamic_test_model.py --opponent wb
```
# Against minimax
```
python dynamic_test_model.py --opponent minimax
```
# Against heuristic player
```
python dynamic_test_model.py --opponent heuristic
```


## Here is how you can see a sample game

# Against win-block player
```
python dynamic_view_model.py --opponent random
```
# Against random player
```
python dynamic_view_model.py --opponent wb
```
# Against minimax
```
python dynamic_view_model.py --opponent minimax
```
# Against heuristic player
```
python dynamic_view_model.py --opponent heuristic
```