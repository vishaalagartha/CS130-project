import json, praw

class DataCrawler:
    def __init__(self, json={}):
        self.reddit = praw.Reddit(client_id='Cyqg1DNvQYLqyg',
            client_secret='KT9QupQ_yyqFlBkmi5PUOQBaiWY',
            user_agent='Comment Extraction (by /u/vagartha)')
        self.subreddit = self.reddit.subreddit('nba')

    '''
    Gets comments within a comment
    '''
    def getSubComments(self, comment, allComments, verbose=True, depth=0):
        if depth>5:
            return
        allComments.append(comment)
        if not hasattr(comment, 'replies'):
            replies = comment.comments()
            if verbose: print('fetching (' + str(len(allComments)) + ' comments fetched total)')
        else:
            replies = comment.replies
        for child in replies:
            self.getSubComments(child, allComments, verbose=verbose, depth=depth+1)

    '''
    Get all comments under a submission
    '''
    def getAllComments(self, submission, verbose=True):
        comments = submission.comments
        commentsList = []
        for comment in comments:
            self.getSubComments(comment, commentsList, verbose=verbose)
        return commentsList

    def fetchComments(self):
        print('Fetching comments...')
        for submission in self.subreddit.top():
            for comment in self.getAllComments(submission):
                if hasattr(comment, 'body'):
                    text += comment.body

d = DataCrawler()
d.fetchComments()
