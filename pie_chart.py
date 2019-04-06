import matplotlib.pyplot as plt
import numpy as np

def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{p:.2f}%\n({v:d})'.format(p=pct,v=val)
        return my_autopct
            
def draw_pie_chart1(reviews):
    # Pie chart,
    labels = 'Positive', 'Negative'
    clrs= '#00ff00', '#ff0000'
    sizes = [reviews[0],reviews[1]]
    explode = (0.1, 0)
    fig1, ax1 = plt.subplots()

    ax1.pie(sizes,colors=clrs, explode=explode, labels=labels, autopct=make_autopct(sizes),
            shadow=True, startangle=90)
    ax1.axis('equal')
    plt.show()

def draw_pie_chart2(reviews):
    labels = 'Positive', 'Negative', 'Neutral'
    clrs= '#00ff00', '#ff0000', '#4286f4'
    sizes = [reviews[6],reviews[7],reviews[11]]
    explode = (0.1, 0, 0)
    fig2, ax2 = plt.subplots()
    ax2.pie(sizes,colors=clrs, explode=explode, labels=labels, autopct=make_autopct(sizes),
            shadow=True, startangle=90)
    ax2.axis('equal')
    plt.show()
    pos=(reviews[0],reviews[6])
    neg=(reviews[1],reviews[7])
    neut=(reviews[0],reviews[11])

    N = 2
    ind = np.arange(N)
    width = 0.35
    plt.ylabel('Reviews count')
    plt.title('comparison of  document count (polarity)')
    plt.xticks(ind, ('Without Star Rating','With Star Rating'))

    #StackedChart
    
    p1 = plt.bar(ind, pos, width, color='#00ff00' )
    p2 = plt.bar(ind, neut, width,color='#4286f4',
                 bottom=pos)
    p3 = plt.bar(ind, neg, width,color='#ff0000',
                 bottom=neut)

    plt.legend((p1[0], p2[0], p3[0]), ('Positive', 'Neutral','Negative'))

    
    #NormalChart

    #tot=(reviews[0]+reviews[1],reviews[6]+reviews[7]+reviews[11])
   # p1 = plt.bar(ind, tot, width, color='#4286f4')
    

    plt.show()