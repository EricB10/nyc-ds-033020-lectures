# Create Figure and Subplots
fig, axes = plt.subplots(2,2, figsize=(10,6), sharex=False, sharey=False, dpi=120)
axes[0][0].plot(x,y, color='b' )
axes[0][0].set_title('Ax: 1')

axes[0][1].scatter(x2,y2, color='r', facecolor='none' )
axes[0][1].set_title('Ax: 2' )

axes[1][0].plot(x,y, color='b' )
axes[1][0].scatter(x2,y2, color='r', marker='o', facecolor='none' )

axes[1][0].set_title('Ax: 3' )
axes[1][1].plot(x,y, color='b' )

ax2 = axes[1][1].twinx()
ax2.scatter(x2,y2, color='r', marker='o', facecolor='none' )
axes[1][1].set_title('Ax: 4' )

fig.suptitle('Four Subplots in One Figure', fontsize=16)  
fig.savefig('answer_guide')