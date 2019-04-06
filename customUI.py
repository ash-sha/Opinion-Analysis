import wx,os
import maxentevaluator,naivebayesevaluator
import extract_data
import pie_chart
import random
import matplotlib.pyplot as plt

class ExamplePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.isBrowsedDataset=False

        self.logger1 = wx.TextCtrl(self, pos=(20,180), size=(600,580), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.logger2 = wx.TextCtrl(self, pos=(620,180), size=(600,580), style=wx.TE_MULTILINE | wx.TE_READONLY)

        # Search Query Text Control
        self.search_quote = wx.StaticText(self, label="Search:", pos=(20, 30))
        self.editname = wx.TextCtrl(self, value="Query?", pos=(20, 50), size=(340,-1))

         # Check button
        self.check_button =wx.Button(self, label="Check", pos=(370, 49))
        self.Bind(wx.EVT_BUTTON, self.onClick_check,self.check_button)

        # Classifier Type Radio Buttons
        radioList = ['Max Entropy','Naive Bayes']
        self.rb = wx.RadioBox(self, label="Classifier Type", pos=(20, 90), choices=radioList,  majorDimension=3,
                         style=wx.RA_SPECIFY_COLS)
    
    def onClick_check(self,event):
    	self.logger1.Clear()
        self.logger2.Clear()
        query_string=self.editname.GetValue()
        classifier_type=self.rb.GetSelection()
        self.logger1.AppendText("Query = \'"+query_string+"\'\n")
        self.logger2.AppendText("Query = \'"+query_string+"\'\n")

        if classifier_type==1:
        	self.logger1.AppendText("Classifier type = Naive Bayes\n")
        	result=naivebayesevaluator.main(1)
        	self.logger1.AppendText("\n"+result[0])
        	self.logger1.AppendText("\nAccuracy for Positives: %.2f%%" % result[1])
        	self.logger1.AppendText("\nAccuracy for Negatives: %.2f%%" % result[2])
        	self.logger1.AppendText("\nAccuracy for (Positives|Negatives): %.2f%%" % result[3])
        	self.logger1.AppendText("\nCorrelation for (Positives|Negatives): %.2f%%" % result[4])
        	self.logger1.AppendText("\n\n")
        	

        	reviews = extract_data.get(query_string,0)
        	self.logger1.AppendText("Positives: " + str(reviews[0])+" ("+str(reviews[2])+"%)")
        	self.logger1.AppendText("\nNegatives: " + str(reviews[1])+" ("+str(reviews[3])+"%)")
        	self.logger2.AppendText("Changed to Positives: " + str(reviews[6])+" ("+str(reviews[8])+"%)")
        	self.logger2.AppendText("\nChanged to Negatives: " + str(reviews[7])+" ("+str(reviews[9])+"%)")
        	self.logger2.AppendText("\nChanged to Neutrals: " + str(reviews[11])+" ("+str(reviews[12])+"%)")
        	self.logger1.AppendText("\n\n")
        	self.logger2.AppendText("\n\n")
        	for tweet in reviews[5]:
        		self.logger1.AppendText(tweet[1]+"\n\n")

        	for tweet in reviews[10]:
        		self.logger2.AppendText(tweet[1]+"\n\n")
                # self.logger2.AppendText(tweet[1].text+"\n\n")
       	
       	elif classifier_type==0:
        	self.logger1.AppendText("Classifier type = Max Entropy\n")
            # self.logger2.AppendText("Classifier type = Max Entropy\n")
        	result=maxentevaluator.main()
        	self.logger1.AppendText("\n"+result[0])
        	self.logger1.AppendText("\nAccuracy for Positives: %.2f%%" % result[1])
        	self.logger1.AppendText("\nAccuracy for Negatives: %.2f%%" % result[2])
        	self.logger1.AppendText("\nAccuracy for (Positives|Negatives): %.2f%%" % result[3])
        	self.logger1.AppendText("\nCorrelation for (Positives|Negatives): %.2f%%" % result[4])
        	self.logger1.AppendText("\n\n")
            

        	reviews = extract_data.get(query_string,1)
        	self.logger1.AppendText("Positives: " + str(reviews[0])+" ("+str(reviews[2])+"%)")
        	self.logger1.AppendText("\nNegatives: " + str(reviews[1])+" ("+str(reviews[3])+"%)")
        	self.logger2.AppendText("Changed to Positives: " + str(reviews[6])+" ("+str(reviews[8])+"%)")
        	self.logger2.AppendText("\nChanged to Negatives: " + str(reviews[7])+" ("+str(reviews[9])+"%)")
        	self.logger2.AppendText("\nChanged to Neutrals: " + str(reviews[11])+" ("+str(reviews[12])+"%)")
        	self.logger1.AppendText("\n\n")
        	self.logger2.AppendText("\n\n")
        	for tweet in reviews[5]:
        		self.logger1.AppendText(tweet[1]+"\n\n")
        	for tweet in reviews[10]:
        		self.logger2.AppendText(tweet[1]+"\n\n")

	pie_chart.draw_pie_chart1(reviews)
	pie_chart.draw_pie_chart2(reviews)


app = wx.App(False)
frame = wx.Frame(None,wx.ID_ANY, "SentimentAnalysis",size=(1290,700))
panel = ExamplePanel(frame)
frame.Show()
app.MainLoop()
