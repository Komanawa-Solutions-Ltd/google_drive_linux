"""
created matt_dumont
on: 7/10/23
"""
import datetime
from copy import deepcopy
import sys
from PyQt6 import QtGui, QtWidgets, QtCore
from utils.base_functions import check_shortcode, bad_shortcode_char


class AddUser(QtWidgets.QWidget):
    submitClicked = QtCore.pyqtSignal(list)

    def __init__(self, existing_users):
        super().__init__()
        for u in existing_users:
            assert type(u) == str
            assert '@' in u
            assert u == u.lower()
        self.existing_users = deepcopy(existing_users)

        self.resize(100, 100)
        # frame box
        vert = QtWidgets.QVBoxLayout()

        # set font stats
        self.font = QtGui.QFont()
        self.sheetstyle = f"color: black; "

        label = QtWidgets.QLabel('User Email Address')
        label.setFont(self.font)
        label.setStyleSheet(self.sheetstyle)
        vert.addWidget(label)
        self.answers = t = QtWidgets.QLineEdit('')
        vert.addWidget(t)
        label = QtWidgets.QLabel('User Short Code')
        label.setFont(self.font)
        label.setStyleSheet(self.sheetstyle)
        vert.addWidget(label)
        label = QtWidgets.QLabel(
            f'note: shortcode cannot contain any of the following characters: ({bad_shortcode_char})')
        label.setFont(self.font)
        label.setStyleSheet(self.sheetstyle)
        vert.addWidget(label)
        self.shortcode = t = QtWidgets.QLineEdit('')
        vert.addWidget(t)
        # save/cancel buttons
        save = QtWidgets.QPushButton('Add User')
        save.clicked.connect(self.save)
        cancel = QtWidgets.QPushButton('Cancel')
        cancel.clicked.connect(self.close)
        horiz = QtWidgets.QHBoxLayout()
        horiz.addWidget(save)
        horiz.addWidget(cancel)
        vert.addLayout(horiz)
        self.setLayout(vert)
        self.show()

    def save(self):
        email = self.answers.text().strip().lower()
        shortcode = self.shortcode.text().strip().lower()
        problem = False
        mssage = ''
        if '@' not in email:
            problem = True
            mssage += 'Email address must contain an @ symbol\n'

        if email in self.existing_users:
            problem = True
            mssage += 'Email address already exists\n'

        success, message = check_shortcode(shortcode)
        if not success:
            problem = True
            mssage += message + '\n'

        if problem:
            mbox = QtWidgets.QMessageBox()
            mbox.setText(mssage)
            mbox.setFont(self.font)
            mbox.setStyleSheet(self.sheetstyle)
            mbox.exec()
            return

        self.submitClicked.emit([True, email, shortcode])
        self.close()


class ChangeShortcode(QtWidgets.QWidget):
    submitClicked = QtCore.pyqtSignal(list)

    def __init__(self, user, current_shortcode):
        super().__init__()
        self.user = user
        self.resize(100, 100)
        # frame box
        vert = QtWidgets.QVBoxLayout()

        # set font stats
        self.font = QtGui.QFont()
        self.sheetstyle = f"color: black; "

        label = QtWidgets.QLabel(f'Change Shortcode for User:{user}')
        label.setFont(self.font)
        label.setStyleSheet(self.sheetstyle)
        vert.addWidget(label)
        label = QtWidgets.QLabel(f'Current shortcode:{current_shortcode}')
        label.setFont(self.font)
        label.setStyleSheet(self.sheetstyle)
        vert.addWidget(label)
        label = QtWidgets.QLabel(
            f'note: shortcode cannot contain any of the following characters: ({bad_shortcode_char})')
        label.setFont(self.font)
        label.setStyleSheet(self.sheetstyle)
        vert.addWidget(label)
        self.shortcode = t = QtWidgets.QLineEdit('')
        vert.addWidget(t)
        # save/cancel buttons
        save = QtWidgets.QPushButton('Change Shortcode')
        save.clicked.connect(self.save)
        cancel = QtWidgets.QPushButton('Cancel')
        cancel.clicked.connect(self.close)
        horiz = QtWidgets.QHBoxLayout()
        horiz.addWidget(save)
        horiz.addWidget(cancel)
        vert.addLayout(horiz)
        self.setLayout(vert)
        self.show()

    def save(self):
        shortcode = self.shortcode.text().strip().lower()
        problem = False
        mssage = ''
        success, message = check_shortcode(shortcode)
        if not success:
            problem = True
            mssage += message + '\n'

        if problem:
            mbox = QtWidgets.QMessageBox()
            mbox.setText(mssage)
            mbox.setFont(self.font)
            mbox.setStyleSheet(self.sheetstyle)
            mbox.exec()
            return

        self.submitClicked.emit([True, self.user, shortcode])
        self.close()


def launch_add_user(existing_users):
    app = QtWidgets.QApplication(sys.argv)
    win = AddUser(existing_users)
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    existing_users = ['test@test']
    launch_add_user(existing_users)
    print(f'{existing_users=}')
