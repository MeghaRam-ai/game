# Game

#### Two approaches used 
1. Random Selection
2. RNN

#### To run the model and notebooks, first install necessary packages

 ```bash 
   $ pip install -r requirements.txt
   ```
#### To start streamlit application

1. Open terminal and go to the location frontend and excecute the following command
```bash
  $ streamlit run frontend/page.py
  ```


## Explanation of the project

First approach `Random Selection` is the best if we have to limit within the given dataset.
For this, I have created a funciton called `regenerate` which takes time duration of the expected game as input and generate sequence of norm and corresponding action.

In the Streamlit application, Give the time duration in the edit field and press enter to get the sequence.


Second approach `RNN` has been chosen considering the fact that we have sequnce of data(1D) and `RNN` is the best option if the order of sequence matters.
But the limitation is that, label/action is not indicated for the sequence. 
