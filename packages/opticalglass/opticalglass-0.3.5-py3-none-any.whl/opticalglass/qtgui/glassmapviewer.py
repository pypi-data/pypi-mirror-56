#!/usr/bin/env python3
# Copyright © 2018 Michael J. Hayford
# -*- coding: utf-8 -*-
""" desktop application for viewing glass catalog data

.. Created on Wed Jan  3 12:50:03 2018

.. codeauthor: Michael J. Hayford
"""

import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout,
                             QVBoxLayout, QSizePolicy, QGroupBox, QCheckBox,
                             QTableWidget, QTableWidgetItem, QRadioButton)
from PyQt5.QtCore import Qt as qt

from matplotlib.backends.backend_qt5agg \
     import (FigureCanvasQTAgg as FigureCanvas,
             NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure
from matplotlib.patches import Polygon

import opticalglass.glassfactory as gf
import opticalglass.glasspolygons as gp

pickTableHeader = ["Catalog", "Glass", "Nd", "Vd", "P C,d"]
pickTableFormat = ["s", "s", "7.5f", "5.2f", "6.4f"]


def rgb2mpl(rgb):
    if len(rgb) == 3:
        return [rgb[0]/255., rgb[1]/255., rgb[2]/255., 1.0]
    elif len(rgb) == 4:
        return [rgb[0]/255., rgb[1]/255., rgb[2]/255., rgb[3]/255.]


class GlassMapViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Glass Map Viewer'
        self.left = 50
        self.top = 150
        self.width = 1100
        self.height = 650
        self.dataSets = gf.GlassMapModel()
        self.displayDataSets = [True, True, True, True]
        self.display_ref_index = True
        self.initUI()

    def initUI(self):
        self._main = QWidget()
        self.setCentralWidget(self._main)
        layout = QHBoxLayout(self._main)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.gmt = self.createTable()
        self.gm = PlotCanvas(self, width=5, height=4)
        self.addToolBar(qt.BottomToolBarArea,
                        NavigationToolbar(self.gm, self))
        layout.addWidget(self.gm)

        rightBar = QVBoxLayout()
        layout.addLayout(rightBar)

        plotTypeGroup = self.createPlotTypeBox()
        rightBar.addWidget(plotTypeGroup)

        catalogGroup = self.createCatalogGroupBox()
        rightBar.addWidget(catalogGroup)

        rightBar.addWidget(self.gmt)

    def createPlotTypeBox(self):
        groupBox = QGroupBox("Plot Type", self)

        index_btn = QRadioButton("Refractive Index")
        index_btn.setChecked(True)
        index_btn.toggled.connect(lambda:
                                  self.on_plot_type_toggled(index_btn))
        partial_btn = QRadioButton("Partial Dispersion")
        partial_btn.toggled.connect(lambda:
                                    self.on_plot_type_toggled(partial_btn))

        vbox = QVBoxLayout()
        vbox.addWidget(index_btn)
        vbox.addWidget(partial_btn)

        groupBox.setLayout(vbox)

        return groupBox

    def on_plot_type_toggled(self, button):
        if button.text() == "Refractive Index":
            if button.isChecked() is True:
                self.display_ref_index = True

        if button.text() == "Partial Dispersion":
            if button.isChecked() is True:
                self.display_ref_index = False

        self.gm.display_ref_index = self.display_ref_index
        self.gm.update_data()
        self.gm.plot()

    def createCatalogGroupBox(self):
        groupBox = QGroupBox("Glass Catalogs", self)

        cdgm_checkBox = QCheckBox("&CDGM")
        cdgm_checkBox.setChecked(True)
        cdgm_checkBox.stateChanged.connect(self.cdgm_check)
        hoya_checkBox = QCheckBox("&Hoya")
        hoya_checkBox.setChecked(True)
        hoya_checkBox.stateChanged.connect(self.hoya_check)
        ohara_checkBox = QCheckBox("&Ohara")
        ohara_checkBox.setChecked(True)
        ohara_checkBox.stateChanged.connect(self.ohara_check)
        schott_checkBox = QCheckBox("&Schott")
        schott_checkBox.setChecked(True)
        schott_checkBox.stateChanged.connect(self.schott_check)

        vbox = QVBoxLayout()
        vbox.addWidget(cdgm_checkBox)
        vbox.addWidget(hoya_checkBox)
        vbox.addWidget(ohara_checkBox)
        vbox.addWidget(schott_checkBox)

        groupBox.setLayout(vbox)

        return groupBox

    def createTable(self):
        table = PickTable()
        return table

    def cdgm_check(self, state):
        checked = state == qt.Checked
        self.gm.displayDataSets[gf.CDGM] = checked
        self.gm.updateVisibility(gf.CDGM, checked)

    def hoya_check(self, state):
        checked = state == qt.Checked
        self.gm.displayDataSets[gf.Hoya] = checked
        self.gm.updateVisibility(gf.Hoya, checked)

    def ohara_check(self, state):
        checked = state == qt.Checked
        self.gm.displayDataSets[gf.Ohara] = checked
        self.gm.updateVisibility(gf.Ohara, checked)

    def schott_check(self, state):
        checked = state == qt.Checked
        self.gm.displayDataSets[gf.Schott] = checked
        self.gm.updateVisibility(gf.Schott, checked)


class PickTable(QTableWidget):
    def __init__(self):
        super().__init__(16, len(pickTableHeader))
        self.rowFill = 16
        self.setHorizontalHeaderLabels(pickTableHeader)
        for i, w in enumerate([52, 96, 61, 48, 60]):
            self.setColumnWidth(i, w)
        self.setAlternatingRowColors(True)
        self.setMinimumWidth(285)
        self.setMaximumWidth(335)

    def setRowCount(self, count):
        if count > self.rowFill:
            super().setRowCount(count)

    def resizeEvent(self, event):
        super(QTableWidget, self).resizeEvent(event)
        rowsToFill = int(self.height()/self.rowHeight(0))
        if rowsToFill > self.rowFill:
            self.rowFill = rowsToFill
            if rowsToFill > self.rowCount():
                super().setRowCount(rowsToFill)


class PlotCanvas(FigureCanvas):
    dsc = [(56/255, 142/255, 142/255),  # sgi teal
           (113/255, 113/255, 198/255),  # sgi slateblue
           (102/255, 205/255, 0),  # chartreuse 3
           (255/255, 114/255, 86/255)]  # coral 1

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # fig = Figure(figsize=(width, height), dpi=dpi)
        fig = Figure()
        self.axes = fig.add_subplot(111)
        self.rawData = []
        self.data = parent.dataSets
        self.displayDataSets = parent.displayDataSets
        self.pickTable = parent.gmt
        self.display_ref_index = parent.display_ref_index
        self.needsClear = True
        self.pickRow = 0

        self.update_data()

        super().__init__(fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)

        FigureCanvas.updateGeometry(self)
        self.plot()

    def get_display_label(self):
        if self.display_ref_index is True:
            return 'Glass Map'
        else:
            return 'Partial Dispersion'

    def update_data(self):
        self.rawData = []
        for i, display in enumerate(self.displayDataSets):
            n, v, p, lbl = self.data.get_data_at(i)
            dsLabel = self.data.get_data_set_label_at(i)
            self.rawData.append([dsLabel, (n, v, p, lbl)])

    def plot(self):
        self.axes.cla()
        xi = 1
        if self.display_ref_index is True:
            yi = 0
            self.draw_glass_polygons()
        else:
            yi = 2
        self.axes.set_title(self.get_display_label())
        for i, display in enumerate(self.displayDataSets):
            self.axes.plot(self.rawData[i][1][xi], self.rawData[i][1][yi],
                           linestyle='None', marker='o', markersize=5,
                           color=self.dsc[i], alpha=0.75, gid=i, picker=5,
                           label=self.rawData[i][0], visible=display)

        self.figure.canvas.mpl_connect('pick_event', self.on_pick)
        self.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.axes.invert_xaxis()
        self.axes.grid()
        self.axes.legend()
        self.draw()

    def draw_glass_polygons(self):
        for glass, poly in gp.polygons.items():
            rgb = gp.rgb[glass]
            p = Polygon(poly, closed=True, fc=rgb2mpl(rgb), ec='black',
                        linewidth=1.0)
            self.axes.add_artist(p)

    def clearPickTable(self):
        self.pickTable.clearContents()
        self.pickRow = 0
        self.needsClear = False

    def on_press(self, event):
        if self.needsClear:
            # If needsClear is still set, there have been no pick events so
            #  this is a click in an empty region of the plot.
            #  Clear the pick table
            self.clearPickTable()
        else:
            # on_press event happens after on_pick events. Set needsClear for
            #  next on_pick, i.e. a new selection, to handle
            self.needsClear = True

    def on_pick(self, event):
        if self.needsClear:
            self.clearPickTable()
        line = event.artist
        id = line.get_gid()
        if self.displayDataSets[id]:
            ind = event.ind
            dsLabel = self.rawData[id][0]
            n, v, p, lbl = self.rawData[id][1]
            self.pickTable.setRowCount(self.pickRow+len(ind))
            for k in ind:
                glass = (dsLabel, lbl[k], n[k], v[k], p[k])
                for j in range(len(pickTableHeader)):
                    item = QTableWidgetItem(format(glass[j],
                                                   pickTableFormat[j]))
                    self.pickTable.setItem(self.pickRow, j, item)
                self.pickRow += 1

    def updateVisibility(self, indx, state):
        self.axes.lines[indx].set_visible(state)
        self.draw()


def main():
    qtapp = QApplication(sys.argv)
    qtwnd = GlassMapViewer()
    qtwnd.show()
    return qtapp.exec_()


if __name__ == '__main__':
    sys.exit(main())
