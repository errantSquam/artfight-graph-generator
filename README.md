To install Python requirements: ``pip install -r /path/to/requirements.txt``

Hello! This is very simple source code for generating a pretty graph of your Artfight characters. 

It's mostly manual and requires you to set up a .csv file with the following setup:
| Day | Character 1 | Character 2 |
| --- | ----------- | ----------- |
| 0 | | |
| 1 | 1 | |
...and so on.


Number of attacks per day is cumulative, so you don't have to do a re-count every time.

You may also add your own custom markers/portraits if you wish, otherwise the marker will default to a circle.

I'd love to implement scraping functionalities, but Artfight doesn't have an official API and I'm not sure if the servers can handle it. You'd also need a backend setup which is a bit more work.

Example:

![image](https://file.garden/ZovllhPbE2hYNtBE/output.png)

## IMPORTANT

The license requires you to **credit and keep the code open source** if you do decide to fork this repo, so please respect that! 

And if you're using this on Artfight, credit to me (ErrantSquam) would be appreciated too :]

