# Data Files

+ best-emojis.json
  + a json of the emojis we use for classification
+ best-twitter-data-eggplant.txt
  + a txt file with tweets with 1000 tweets for each emoji in best-emojis. This
    one includes eggplant and sweat emoji data, which we probably won't use
    cause they're a little too sexual in nature
+ best-twitter-data.txt
  + a txt file with tweets w 1000 tweets for each emoji in best-emojis. No
    eggplant or sweat
+ emojifier-mapping.json
  + a mapping made with the script we wrote, not the script written from the
    reddit bot. Contains a "before" and "after" list of emojis
+ emoji-mappings.json
  + mapping made by the reddit bot
+ twitter-data.txt
  + Twitter data for the top 15 or so emojis from emojitrackers, 100 tweets per
    emoji. Used mostly to test how good twitter tweets would be as training data
+ twitter-mapping.json
  + emoji mapping made from twitter-data.txt
+ updated-comments.txt
  + Reddit comments from r/emojipasta scraped by the reddit bot