import os
import numpy as np
import matplotlib.transforms as mtransforms
import matplotlib.lines as lines
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import matplotlib.text as mtext


class StraightLine(lines.Line2D):
    def __init__(self, *args, **kwargs):
        # we'll update the position when the line data is set
        self.text = mtext.Text(0, 0, '')
        lines.Line2D.__init__(self, *args, **kwargs)

        # we can't access the label attr until *after* the line is
        # inited
        self.text.set_text(self.get_label())

    def set_figure(self, figure):
        self.text.set_figure(figure)
        lines.Line2D.set_figure(self, figure)

    def set_axes(self, axes):
        self.text.set_axes(axes)
        lines.Line2D.set_axes(self, axes)

    def set_transform(self, transform):
        # 2 pixel offset
        texttrans = transform + mtransforms.Affine2D().translate(2, 2)
        self.text.set_transform(texttrans)
        lines.Line2D.set_transform(self, transform)

    def set_data(self, x, y):
        if len(x):
            self.text.set_position((x[-1], y[-1]))

        lines.Line2D.set_data(self, x, y)

    def draw(self, renderer):
        # draw my label at the end of the line with 2 pixel offset
        lines.Line2D.draw(self, renderer)
        self.text.draw(renderer)


class PlotLoss(object):
    """Documentation for PlotLoss

    """

    def __init__(self,
                 xscale=None,
                 yscale=None,
                 fontsize=14,
                 xlabel='# epoch',
                 ylabel='loss',
                 title=None,
                 xticks=None,
                 yticks=None,
                 xtickspace=1,
                 xtickformat=None,
                 ytickformat=None):
        super(PlotLoss, self).__init__()
        self.xscale = xscale
        self.yscale = yscale
        self.fontsize = fontsize
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        self.xtickspace = xtickspace
        self.xticks = xticks
        self.yticks = yticks
        self.xtickformat = xtickformat
        self.ytickformat = ytickformat

    def __call__(self, loss, label=None, color=None):
        """
        """
        n_records = len(loss)
        if not hasattr(self, 'fig'):
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(
                111,
                xscale=self.xscale,
                yscale=self.yscale)
            self.ax.spines["top"].set_visible(False)
            self.ax.spines["bottom"].set_visible(True)
            self.ax.spines["right"].set_visible(False)
            self.ax.spines["left"].set_visible(False)
            self.ax.get_xaxis().tick_bottom()
            self.ax.get_yaxis().tick_left()
            if self.xlabel is not None:
                self.ax.set_xlabel(self.xlabel, fontsize=self.fontsize)
            if self.ylabel is not None:
                self.ax.set_ylabel(self.ylabel, fontsize=self.fontsize)
            if self.title is not None:
                self.ax.set_title(self.title, fontsize=self.fontsize)
        if self.yticks is None:
            if self.yscale == 'log':
                yticks = np.logspace(-4, -1, num=5)
            elif self.yscale == 'plain':
                yticks = np.arange(0, 1.1 * max(loss), 5)
            self.ax.set_yticklabels(yticks, {'fontsize': self.fontsize})
            self.ax.set_yticks(yticks)

        self.xticks = range(0, n_records, 1)
        self.ax.set_xticks(self.xticks[::self.xtickspace])
        self.ax.set_xticklabels(
            self.xticks[::self.xtickspace], {'fontsize': 14})
        for yt in yticks:
            plt.plot(self.xticks, [yt] * len(self.xticks),
                     "--", lw=1.0, color='black', alpha=0.7)
        if self.ytickformat == 'sci':
            plt.gca().yaxis.set_major_formatter(tck.FormatStrFormatter('%.0e'))
        self.ax.plot(range(0, n_records, 1), loss,
                     linewidth=2, color=color)
        self.ax.text(n_records - 1, loss[-1], label,
                     fontsize=self.fontsize, color=color,
                     transform=self.ax.transData)
        plt.show()

    def savefig(self, name, path,
                format='eps',
                transparent=True,
                pad_inches=0.05):
        """
        """

        conf = {'facecolor': 'w',
                'edgecolor': 'w',
                'format': format,
                'transparent': transparent,
                'bbox_inches': 'tight',
                'pad_inches': pad_inches,
                'frameon': None}
        self.fig.savefig(os.path.join(path, name), **conf)
