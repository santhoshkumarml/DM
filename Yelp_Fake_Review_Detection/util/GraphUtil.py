'''
Created on Jan 12, 2015

@author: santhosh
'''
import networkx
from datetime import datetime,timedelta
import re
import SIAUtil

class SuperGraph(networkx.Graph):
    def __init__(self, parentUserIdToUserDict=dict(),parentBusinessIdToBusinessDict=dict(), parent_reviews= dict()):
        super(SuperGraph, self).__init__()
        self.userIdToUserDict = parentUserIdToUserDict
        self.businessIdToBusinessDict = parentBusinessIdToBusinessDict
        self.reviewIdToReviewDict = parent_reviews
    
    
    def addNodesAndEdge(self, usr, bnss, review):
        self.userIdToUserDict[usr.getId()] = usr
        self.businessIdToBusinessDict[bnss.getId()] = bnss
        self.reviewIdToReviewDict[review.getId()] = review
        super(SuperGraph, self).add_node((usr.getId(),SIAUtil.USER))
        super(SuperGraph, self).add_node((bnss.getId(),SIAUtil.PRODUCT))
        super(SuperGraph, self).add_edge((usr.getId(),SIAUtil.USER),\
                                              (bnss.getId(),SIAUtil.PRODUCT),\
                                               attr_dict={SIAUtil.REVIEW_EDGE_DICT_CONST: review.getId()})
    
    def getUser(self, userId):
        return self.userIdToUserDict[userId]
    
    def getBusiness(self, businessId):
        return self.businessIdToBusinessDict[businessId]
        
    def getReview(self,usrId, bnssId):
        return self.reviewIdToReviewDict[self.get_edge_data((usrId,SIAUtil.USER), (bnssId,SIAUtil.PRODUCT))[SIAUtil.REVIEW_EDGE_DICT_CONST]]
    
    @staticmethod
    def createGraph(userIdToUserDict,bnssIdToBusinessDict, parent_reviews):
        graph = SuperGraph()
        for reviewKey in parent_reviews.iterkeys():
            review = parent_reviews[reviewKey]
            graph.addNodesAndEdge(userIdToUserDict[review.getUserId()],\
                                         bnssIdToBusinessDict[review.getBusinessID()],\
                                         review)
        return graph

class TemporalGraph(networkx.Graph):
    
    def __init__(self, parentUserIdToUserDict=dict(),parentBusinessIdToBusinessDict=dict(), parent_reviews= dict()):
        super(TemporalGraph, self).__init__()
        self.userIdToUserDict = parentUserIdToUserDict
        self.businessIdToBusinessDict = parentBusinessIdToBusinessDict
        self.reviewIdToReviewDict = parent_reviews
    
    def addNodesAndEdge(self, usr, bnss, review):
        self.userIdToUserDict[usr.getId()] = usr
        self.businessIdToBusinessDict[bnss.getId()] = bnss
        self.reviewIdToReviewDict[review.getId()] = review
        super(TemporalGraph, self).add_node((usr.getId(),SIAUtil.USER))
        super(TemporalGraph, self).add_node((bnss.getId(),SIAUtil.PRODUCT))
        super(TemporalGraph, self).add_edge((usr.getId(),SIAUtil.USER),\
                                              (bnss.getId(),SIAUtil.PRODUCT),\
                                               attr_dict={SIAUtil.REVIEW_EDGE_DICT_CONST: review.getId()})
            
    def getUserCount(self):
        return len(set([node_id for (node_id, node_type) in self.nodes() if node_type == SIAUtil.USER]))
    
    def getUserIds(self):
        return [node_id for (node_id, node_type) in self.nodes() if node_type == SIAUtil.USER]
    
    def getBusinessIds(self):
        return [node_id for (node_id, node_type) in self.nodes() if node_type == SIAUtil.PRODUCT]

    def getBusinessCount(self):
        return len(set([node_id for (node_id, node_type) in self.nodes() if node_type == SIAUtil.PRODUCT]))
    
    def getReviewIds(self):
        return [self.get_edge_data(*edge)[SIAUtil.REVIEW_EDGE_DICT_CONST] for edge in self.edges()]
    
    def getReviewCount(self):
        return len(set([self.get_edge_data(*edge)[SIAUtil.REVIEW_EDGE_DICT_CONST] for edge in self.edges()]))
        
    def getUser(self, userId):
        return self.userIdToUserDict[userId]
    
    def getBusiness(self, businessId):
        return self.businessIdToBusinessDict[businessId]
        
    def getReview(self,usrId, bnssId):
        return self.reviewIdToReviewDict[self.get_edge_data((usrId,SIAUtil.USER), (bnssId,SIAUtil.PRODUCT))[SIAUtil.REVIEW_EDGE_DICT_CONST]]

    @staticmethod
    def createTemporalGraph(userIdToUserDict,businessIdToBusinessDict, parent_reviews,\
                          timeSplit ='1-D', initializePriors=True):
        if not re.match('[0-9]+-[DMY]', timeSplit):
            print 'Time Increment does not follow the correct Pattern - Time Increment Set to 1 Day'
            timeSplit ='1-D'

        numeric = int(timeSplit.split('-')[0])
        incrementStr = timeSplit.split('-')[1]
        dayIncrement = 1
        if incrementStr=='D':
            dayIncrement = numeric
        elif incrementStr=='M':
            dayIncrement = numeric*30
        else:
            dayIncrement = numeric*365
        
        all_reviews = [SIAUtil.getDateForReview(r)\
                 for r in parent_reviews.values() ]
        minDate =  min(all_reviews)
        maxDate =  max(all_reviews)

        cross_time_graphs = dict()
        time_key = 0
    
        while time_key < ((maxDate-minDate+timedelta(dayIncrement))/dayIncrement).days:
            cross_time_graphs[time_key] = TemporalGraph()
            time_key+=1
        
        for reviewKey in parent_reviews.iterkeys():
            review = parent_reviews[reviewKey]
            reviewDate = SIAUtil.getDateForReview(review)
            timeDeltaKey = ((reviewDate-minDate)/dayIncrement).days
            temporalGraph = cross_time_graphs[timeDeltaKey]
            temporalGraph.addNodesAndEdge(userIdToUserDict[review.getUserId()],\
                                         businessIdToBusinessDict[review.getBusinessID()],\
                                         review)
        return cross_time_graphs