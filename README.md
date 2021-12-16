# BJ Game
HangGao-project

It's the source code and data of my BJ(There are a total of 5 "size" options (25, 30, 35, 40, 50))

__All experiments are based on the environment under python__

__How to run the code?__

Open your terminal, type the command "python" and your file name. For example, if you try to run the file "nn.py", type the command "python nn.py".

__Requirement__:

Torch, Matplotlib(Type the command "pip install torch". Type the command "pip install matplotlib". (Make sure that the two data packages "torch" and "matplotlib" are installed on your computer))

__Sturcture__:
__In order to make the program run successfully, please put all 6 ".py" files under the same directory on your computer__



__To run:__

__1.__ If you try to run the interactive domain program, just run the code "final_bj_nn.py". (When you want to use "tree-nn" mode, it is recommended to choose size 30.)

__2.__ If you try to run the computer experiments for tree search, just run the code "bj_exp.py".(This program is used to create two histograms for each problem size.Because there are 5 "sizes", 10 images will eventually be generated)

__3.__ If you try to run the computer experiments for tree+NN search, just run the code "bj_nn_exp.py". (This program is only used to create two histograms)

__4.__ If you try to run the computer experiments for Neural Network and see the “learning curve” of training and testing error during gradient descent, just run the code "nn.py"

__5.__ "exist_data.py" is used to store the test-data and train-data. For each data, there are 500 examples in it.(I have done 500 experiments for each data set in advance, and store all the data in a list, and use it as the return value of a function. It can be called directly when you want use it) (for this code, you do not need to run it)

__6.__ "data.py" is used to generate all examples in the training set and test set for the neural network(when you run it, at the end of the program, the screen will display the size of the data set and all the contents of the data set. And this data set will also be returned as the return value of a function)

__Important!!!: please put all 6 ".py" files under the same directory on your computer__




